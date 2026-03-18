---

# ⚔️ Red_Framework (Giga-Arsenal V5)

Un framework d'automatisation Red Team "Enterprise-Grade" développé en Python. Cette version **V5 (Enterprise Update)** transforme l'outil en un écosystème autonome, asynchrone et intelligent, intégrant un mode "Auto-Pilot" pour la gestion des dictionnaires et un C2 Multi-Sessions.

⚠️ **Avertissement Légal :** Cet outil est strictement réservé à un usage légal dans le cadre d'audits de cybersécurité autorisés ou de laboratoires DevSecOps. L'auteur décline toute responsabilité en cas d'usage malveillant.

---

## 🛠️ Installation & Dépendances

```powershell
# Cloner et entrer dans le répertoire
git clone [https://github.com/votre-nom/Red_Framework.git](https://github.com/votre-nom/Red_Framework.git)
cd Red_Framework

# Installer les dépendances (aiohttp, dnspython, beautifulsoup4, markdown, etc.)
pip install -r requirements.txt

# Initialiser l'arsenal (Télécharge les wordlists SecLists par défaut)
python arsenal.py update
```

---

## 🧠 Philosophie de la V5

1. **Auto-Pilot (Cascade) :** Les modules offensifs (`brute-web`, `crack`, `sub`) n'ont plus besoin qu'on leur spécifie un dictionnaire. Ils utilisent par défaut une cascade intelligente : ils testent d'abord vos listes sur-mesure, puis basculent silencieusement sur les standards de l'industrie (SecLists).
2. **Reconnaissance Hybride :** Fusion des techniques passives (OSINT via API) et actives (Brute-force asynchrone) pour une couverture maximale.
3. **Reporting Centralisé :** Vos découvertes sont formatées en temps réel et exportables en un clic au format HTML/PDF professionnel.

---

## 📂 Architecture du Framework

```text
Red_Framework/
├── arsenal.py          # Routeur principal (Point d'entrée unique)
├── core/               # Le Cerveau
│   ├── utils.py        # Résolveur intelligent de wordlists
│   ├── reporter.py     # Moteur d'auto-documentation Markdown
│   └── proxy_manager.py# Gestionnaire de furtivité (Tor/SOCKS5)
├── modules/            # L'Armurerie (Modules offensifs asynchrones)
├── wordlists/          # Les Munitions (Téléchargées via 'update' & générées)
└── reports/            # Les Trophées (Rapports .md et .html générés)
```

---

## 📖 Aide-Mémoire des Commandes (Cheatsheet)

L'Arsenal est piloté par un routeur central asynchrone. Utilisez `python arsenal.py <module> -h` pour le détail des options.

### 📡 1. Reconnaissance & Infrastructure (Élargir la cible)

| Commande | Action |
| --- | --- |
| `python arsenal.py sub -d <domaine> [--auto-scan]` | **Hybride Enum :** Reconnaissance OSINT (`crt.sh`) + Brute-force DNS. L'option `--auto-scan` lance un scan de ports sur les cibles vivantes. |
| `python arsenal.py scan -T <IP>` | **Scanner de Ports :** Scan TCP asynchrone, Banner Grabbing et recherche automatique de CVE. |
| `python arsenal.py s3 -n <nom_entreprise>` | **S3 Hunter :** Cherche des buckets AWS S3 mal configurés basés sur le nom de l'entreprise. |

### 🌐 2. Audit Web & Intelligence (Creuser la faille)

| Commande | Action |
| --- | --- |
| `python arsenal.py spider -u <URL> -d <profondeur>` | **Web Crawler :** Cartographie récursive. Lance automatiquement le détecteur de CMS au démarrage. Supporte `--proxy`. |
| `python arsenal.py cms -u <URL>` | **CMS Detect :** Identifie WordPress, Joomla, Drupal, etc. via signatures. |
| `python arsenal.py secrets -u <URL>` | **Secret Sniper :** Cherche les dossiers `.git`, `.env`, backups et fichiers de configuration exposés. |
| `python arsenal.py headers -u <URL>` | **Header Analyzer :** Analyse les en-têtes de sécurité (CORS, CSP, X-Frame, etc.). |
| `python arsenal.py brute-web -u <URL> -U <user>` | **Custom Brute :** Brute-force HTTP POST asynchrone (Early Exit). Utilise l'Auto-Pilot pour les dictionnaires par défaut. |

### 🔑 3. Exploitation & Interne (Prendre la main)

| Commande | Action |
| --- | --- |
| `python arsenal.py crack --hash <hash>` | **Hash Cracker :** Casse les hashes MD5, SHA1, SHA256 hors-ligne en mode Cascade (Auto-Pilot). |
| `python arsenal.py smb -T <IP>` | **SMB Ghost :** Test de Null Session et énumération des partages Windows (Port 445). |
| `python arsenal.py ldap -T <IP>` | **LDAP Inquisitor :** Extraction d'infos Active Directory via Anonymous Bind (Port 389). |
| `python arsenal.py payload -c <cmd> / --revshell` | **Payload Gen :** Génère des charges utiles obfusquées pour l'évasion d'antivirus. |
| `python arsenal.py c2 -p <port>` | **C2 Server :** Serveur Multi-Sessions en arrière-plan. Supporte Upload/Download et reconnaissance automatique des cibles. |

### 🛠️ 4. Ressources & Reporting (Gérer l'arsenal)

| Commande | Action |
| --- | --- |
| `python arsenal.py update` | **Resource Fetcher :** Télécharge instantanément les standards SecLists (Top Passwords, Users, Subs) en local. |
| `python arsenal.py wordlist -k <mots_clés>` | **Mutation Gen :** Forgera un dictionnaire hybride (Cible + SecLists) dans le répertoire courant. |
| `python arsenal.py notes` | **Note Viewer :** Affiche le rapport brut d'audit actuel dans le terminal. |
| `python arsenal.py export` | **Report Generator :** Exporte vos découvertes dans un magnifique Dashboard HTML "Dark Mode" (prêt pour PDF) situé dans `reports/`. |

---