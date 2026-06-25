# 🎯 Playbook : Compromission Active Directory Complète

> **Scénario type HTB :** D'un accès réseau anonyme jusqu'au `Domain Admin`.
> **Contexte :** Box AD type "Forest", "Active", "Sauna". DC exposé, aucun credential initial.

⚠️ **Cadre légal :** Lab autorisé / CTF uniquement.

---

## 🗺️ Vue d'ensemble de la Kill Chain

```
[1] Recon Réseau ──► [2] Enum Anonyme ──► [3] User Discovery
                                                  │
                                                  ▼
[6] Domain Admin ◄── [5] Lateral Move ◄── [4] AD Kill Chain (adkill)
```

---

## Phase 1 : Reconnaissance Réseau

On cartographie d'abord les services du DC. Les ports clés AD : `88` (Kerberos), `389/636` (LDAP), `445` (SMB), `5985` (WinRM).

```bash
python arsenal.py scan -T 10.10.10.100 -s 1 -e 10000
```

**Points d'intérêt à confirmer :**
- Port `88` ouvert → c'est bien un Domain Controller, Kerberos exploitable.
- Port `445` → énumération SMB / Null Session possible.
- Port `5985` → vecteur d'accès final (Evil-WinRM) si on obtient des creds.

> 🧠 **Pourquoi :** sans le port 88, pas d'AS-REP/Kerberoast. Sa présence valide toute notre stratégie `adkill`.

---

## Phase 2 : Énumération Anonyme

Avant d'attaquer Kerberos, on tente le butin gratuit : Null Sessions SMB et LDAP anonyme.

```bash
python arsenal.py smb -T 10.10.10.100
python arsenal.py ldap -T 10.10.10.100
```

**Ce qu'on cherche :**
- Partages lisibles en anonyme (`Replication`, `SYSVOL` → fichiers `Groups.xml` / GPP passwords).
- Le **nom de domaine** exact (ex: `corp.htb`) requis pour Kerberos.
- Une éventuelle politique de mots de passe (utile pour le spraying sans lock-out).

> 🧠 **Pourquoi :** le naming context LDAP nous donne le FQDN du domaine, indispensable pour les requêtes Kerberos de la phase 4.

---

## Phase 3 : Découverte des Utilisateurs

Kerberos nous permet d'énumérer les comptes valides **sans authentification** (l'erreur `KDC_ERR_PREAUTH_REQUIRED` confirme un user existant).

Si tu n'as pas de liste, génère-la ou utilise SecLists :

```bash
# Option A : wordlist de noms communs
python arsenal.py wordlist -k corp,admin,it,hr -o wordlists/users.txt

# Option B : SecLists (déjà présent sous Parrot)
# /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt
```

> 🧠 **Pourquoi :** une liste d'users valides maximise le rendement des phases AS-REP Roasting et Spraying qui suivent.

---

## Phase 4 : L'Assaut — AD Kill Chain (`adkill`)

Le cœur de l'attaque. On lance l'orchestrateur réactif : il valide les users via Kerberos, traque l'**AS-REP Roasting** (comptes sans pré-auth), bascule en **Kerberoast** dès qu'on a un credential, puis **crack en cascade** automatiquement.

```bash
python arsenal.py adkill -d corp.htb --dc-ip 10.10.10.100 \
    -U wordlists/users.txt \
    -w /usr/share/wordlists/rockyou.txt
```

**Déroulé attendu (système d'observers) :**
1. Énumération → liste des comptes valides.
2. AS-REP Roasting → hash `$krb5asrep$` des comptes vulnérables.
3. Crack auto (rockyou) → si succès, le credential alimente le LootStore.
4. Le credential validé **déclenche automatiquement** le Kerberoast (hash `$krb5tgs$` des comptes de service).
5. Crack auto du TGS → potentiel compte privilégié.

### Variante : Password Spraying

Si l'énumération donne des users mais aucun hash cracké, on tente un mot de passe unique (1 essai/compte → pas de lock-out) :

```bash
python arsenal.py adkill -d corp.htb --dc-ip 10.10.10.100 \
    -U wordlists/users.txt --spray 'Welcome2026!'
```

> 🧠 **Pourquoi :** l'AS-REP roasting ne dépend d'aucun credential, c'est souvent le premier point d'entrée. Le Kerberoast, lui, exige un compte valide — d'où l'enchaînement réactif.

---

## Phase 5 : Mouvement Latéral

Un credential en poche, on valide l'accès et on cherche le chemin vers les privilèges élevés.

```bash
# Vérifier l'accès distant (WinRM) avec le credential obtenu
# Evil-WinRM reste la référence pour ce vecteur :
evil-winrm -i 10.10.10.100 -u svc_user -p 'PasswordCracké'
```

**Sur la cible, on collecte pour BloodHound :**
- Relations ACL, sessions, appartenances de groupes.
- On cherche les chemins : `GenericAll`, `WriteDACL`, `DCSync`.

> 🧠 **Pourquoi :** un simple compte de service kerberoastable a souvent des droits délégués menant directement au domaine (chemin BloodHound).

---

## Phase 6 : Élévation vers Domain Admin

Selon le chemin identifié :

| Vecteur trouvé | Technique d'exploitation |
| :--- | :--- |
| Membre de `Account Operators` | Reset de mot de passe d'un compte privilégié |
| Droit `DCSync` (`Replicating Directory Changes`) | Extraction du hash `krbtgt` / Administrator |
| `GenericAll` sur un groupe | Auto-ajout au groupe `Domain Admins` |
| GPP Password (SYSVOL) | Déchiffrement du `cpassword` |

Une fois le hash `Administrator` obtenu → **Pass-the-Hash** pour l'accès final.

```bash
# Casser un hash NTLM récupéré via DCSync (offline)
python arsenal.py crack --hash <hash_ntlm> --algo ntlm
```

---

## Phase 7 : Capitalisation & Reporting

Tout le butin (creds, hashes, users) est centralisé dans le LootStore. On génère le rapport final.

```bash
python arsenal.py export
```

> 🧠 **Pourquoi :** la traçabilité (preuves, timestamps) est ce qui distingue un audit pro d'un simple "rooting" de box.

---

## ✅ Checklist Récapitulative

- [ ] DC identifié (port 88 ouvert)
- [ ] Domaine FQDN récupéré (LDAP/SMB)
- [ ] Liste d'users valides constituée
- [ ] AS-REP Roasting tenté (`adkill`)
- [ ] Kerberoast déclenché post-credential
- [ ] Spraying si lock-out policy permissive
- [ ] BloodHound pour le chemin d'attaque
- [ ] Hash Administrator / krbtgt obtenu
- [ ] Rapport exporté