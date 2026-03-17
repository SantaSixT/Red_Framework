---

# ⚔️ Red_Framework (Giga-Arsenal V4)

Un framework d'automatisation Red Team "Enterprise-Grade" développé en Python. Cette version **V4 (Ghost Update)** transforme l'outil en un écosystème récursif capable de découvrir, identifier et auditer des infrastructures entières avec une discrétion renforcée.

⚠️ **Avertissement Légal :** Cet outil est strictement réservé à un usage légal dans le cadre d'audits de cybersécurité autorisés ou de laboratoires DevSecOps. L'auteur décline toute responsabilité en cas d'usage malveillant.

---

## 🛠️ Installation & Dépendances

```powershell
# Cloner et entrer dans le répertoire
git clone https://github.com/votre-nom/Red_Framework.git
cd Red_Framework

# Installer les nouvelles dépendances (dnspython, aiohttp_socks, beautifulsoup4, ldap3)
pip install -r requirements.txt

```

---

## 🚀 Guide des Modules (Arsenal V4)

L'Arsenal est piloté par un routeur central asynchrone. Utilisez `python arsenal.py <module> -h` pour le détail des options.

### 📡 1. Reconnaissance Réseau & Sous-domaines

* **`scan`** : Scanner de ports TCP asynchrone (CVE & Bannières).
* **`sub`** : **(Nouveau)** Énumérateur DNS de sous-domaines ultra-rapide.
* *Option `--auto-scan*` : Lance automatiquement un scan de ports sur chaque nouvelle cible découverte.


* **`smb`** : Test de "Null Session" (Port 445) et énumération de partages.
* **`ldap`** : Inquisiteur Active Directory (Port 389) via Anonymous Bind.

### 🌐 2. Audit Web & Intelligence CMS

* **`spider`** : Crawler récursif avec **détection automatique de CMS** intégrée (WordPress, Joomla, etc.). Supporte désormais l'option `--proxy`.
* **`cms`** : **(Nouveau)** Moteur de fingerprinting dédié pour identifier les technologies web via signatures.
* **`brute-web`** : **(Nouveau)** Moteur de brute-force HTTP POST "maison" avec gestion personnalisée des champs et messages d'échec.
* **`secrets`** : Sniper de fichiers sensibles (`.git`, `.env`, `.aws/credentials`).
* **`headers`** : Analyseur de vulnérabilités de configuration (CORS, CSP, Security Headers).

### ☁️ 3. Cloud & Furtivité

* **`s3`** : Chasseur de Buckets AWS S3 via permutations de noms d'entreprise.
* **`Option --proxy`** : **(Global)** Disponible sur les modules Web pour router le trafic via **Tor** (`socks5://127.0.0.1:9050`) ou tout autre proxy SOCKS5/HTTP.

### 🔑 4. Exploitation & Post-Exploitation

* **`crack`** : Casseur de hashes (MD5, SHA1, SHA256).
* **`payload`** : Générateur d'obfuscation PowerShell.
* **`c2`** : Serveur de commande et contrôle asynchrone.

### 📖 5. Intelligence & Reporting

* **`notes`** : **(Nouveau)** Visionneuse de rapport intégrée au terminal. Affiche `arsenal_report.md` avec stylisation couleur.
* **`wordlist`** : Générateur de dictionnaires par mutation.

---

## 📂 Structure de la V4

```text
Red_Framework/
├── arsenal.py          # Routeur principal
├── core/
│   ├── proxy_manager.py # Gestionnaire de furtivité (SOCKS5/Tor)
│   ├── reporter.py      # Moteur Markdown & Visionneuse de notes
│   └── [..]
└── modules/
    ├── sub_enum.py      # Énumération DNS récursive
    ├── cms_detect.py    # Fingerprinting intelligent
    ├── brute_generic.py # Moteur brute-force maison
    └── [..]

```

---

# 📖 Aide-Mémoire des Commandes - Red_Framework

### 📡 1. Reconnaissance & Infrastructure (Élargir la cible)

| Commande | Action |
| --- | --- |
| `python arsenal.py sub -d <domaine> -w <wordlist> [--auto-scan]` | **Énumération DNS :** Trouve les sous-domaines. L'option `--auto-scan` lance un scan de ports immédiat sur chaque découverte. |
| `python arsenal.py scan -T <IP>` | **Scanner de Ports :** Scan TCP asynchrone, Banner Grabbing et recherche automatique de CVE. |
| `python arsenal.py s3 -n <nom_entreprise>` | **S3 Hunter :** Cherche des buckets AWS S3 mal configurés basés sur le nom de l'entreprise. |

### 🌐 2. Audit Web & Intelligence (Creuser la faille)

| Commande | Action |
| --- | --- |
| `python arsenal.py spider -u <URL> -d <profondeur> [--proxy <url>]` | **Web Crawler :** Cartographie récursive. Lance automatiquement le détecteur de CMS au démarrage. Supporte Tor/SOCKS5. |
| `python arsenal.py cms -u <URL>` | **CMS Detect :** Identifie WordPress, Joomla, Drupal, etc. via signatures. |
| `python arsenal.py secrets -u <URL>` | **Secret Sniper :** Cherche les dossiers `.git`, `.env`, backups et fichiers de configuration exposés. |
| `python arsenal.py headers -u <URL>` | **Header Analyzer :** Analyse les en-têtes de sécurité (CORS, CSP, X-Frame, etc.). |
| `python arsenal.py brute-web -u <URL> -U <user> -w <wordlist>` | **Custom Brute :** Brute-force de formulaires HTTP POST avec détection de message d'échec sur mesure. |

### 🔑 3. Exploitation & Interne (Prendre la main)

| Commande | Action |
| --- | --- |
| `python arsenal.py crack -s <hash> -w <wordlist>` | **Hash Cracker :** Casse les hashes MD5, SHA1, SHA256 hors-ligne. |
| `python arsenal.py smb -T <IP>` | **SMB Ghost :** Test de Null Session et énumération des partages Windows (Port 445). |
| `python arsenal.py ldap -T <IP>` | **LDAP Inquisitor :** Extraction d'infos Active Directory via Anonymous Bind (Port 389). |
| `python arsenal.py payload` | **Payload Gen :** Génère des charges utiles obfusquées pour l'évasion d'antivirus. |
| `python arsenal.py c2` | **C2 Server :** Active le serveur de Command & Control pour réceptionner les Reverse Shells. |

### 📖 4. Reporting & Outils (Finaliser l'audit)

| Commande | Action |
| --- | --- |
| `python arsenal.py notes` | **Note Viewer :** Affiche le rapport `arsenal_report.md` stylisé directement dans le terminal. |
| `python arsenal.py wordlist -k <mots_clés>` | **Mutation Gen :** Génère des listes de mots de passe par mutation de mots-clés. |

---

Alors, pour la suite de ton Giga-Outil, est-ce qu'on s'occupe de faire de toi un **expert du reporting (Export HTML/PDF)** ou on renforce ton **contrôle sur les machines cibles (C2 Multitâche)** ?