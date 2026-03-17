# ⚔️ Red_Framework (Arsenal V3)

Un framework d'automatisation Red Team "Enterprise-Grade" développé en Python. Cette V3 transforme l'outil en une plateforme complète de détection de vulnérabilités, de reconnaissance Cloud et d'audit de configuration.

> ⚠️ **Avertissement Légal :** Cet outil est strictement réservé à un usage légal dans le cadre d'audits de cybersécurité autorisés ou de laboratoires DevSecOps. L'auteur décline toute responsabilité en cas d'usage malveillant.

---

## 🛠️ Installation & Dépendances

```powershell
# Cloner et entrer dans le répertoire
git clone [https://github.com/votre-nom/Red_Framework.git](https://github.com/votre-nom/Red_Framework.git)
cd Red_Framework

# Installer les dépendances (pysmb, aiohttp, bs4, ldap3, requests)
pip install -r requirements.txt

```

---

## 🚀 Guide des Modules (Arsenal V3)

L'Arsenal est désormais divisé en 5 piliers stratégiques. Utilisez `python arsenal.py <module> -h` pour le détail de chaque commande.

### 📡 1. Reconnaissance Réseau & Interne

* **`scan`** : Scanner de ports TCP asynchrone avec détection de bannières et recherche automatique de CVE via l'API du NIST.
* **`smb`** : Test de "Null Session" sur le port 445 pour énumérer les partages Windows non sécurisés.
* **`ldap`** : **(Nouveau)** Inquisiteur AD. Tente un "Anonymous Bind" sur le port 389 pour extraire les contextes de nommage de l'annuaire.

### 🌐 2. Audit & Cartographie Web

* **`spider`** : Crawler récursif (Toile) qui extrait tous les liens d'un domaine pour cartographier la surface d'attaque.
* **`enum`** : Brute-force de répertoires et fichiers avec support d'extensions personnalisées.
* **`secrets`** : **(Nouveau)** Sniper de fichiers sensibles. Cherche spécifiquement `.git`, `.env`, `config.php.bak`, etc.
* **`headers`** : **(Nouveau)** Analyseur de sécurité HTTP. Détecte les politiques CORS permissives et l'absence de CSP/X-Frame-Options.

### ☁️ 3. Cloud & Infrastructure

* **`s3`** : **(Nouveau)** Chasseur de Buckets AWS S3. Génère des permutations basées sur le nom de l'entreprise et vérifie les accès publics (Listable/Open).

### 🔑 4. Exploitation & Post-Exploitation

* **`crack`** : Casseur de hashes hors-ligne (MD5, SHA1, SHA256) utilisant vos dictionnaires personnalisés.
* **`brute`** : Brute-force de formulaires de connexion HTTP POST.
* **`payload`** : Générateur d'obfuscation PowerShell pour l'évasion d'AV/EDR.
* **`c2`** : Serveur de commande et contrôle pour réceptionner les Reverse Shells.

### 📖 5. Intelligence & Reporting

* **`wordlist`** : Générateur de dictionnaires ciblés par mutation de mots-clés.
* **`Report Automatique`** : Toutes les découvertes critiques sont consignées en temps réel dans `arsenal_report.md` au format Markdown.

---

## 📂 Structure du Projet

```text
Red_Framework/
├── arsenal.py          # Routeur principal (CLI)
├── arsenal_report.md   # Rapport d'audit généré automatiquement
├── requirements.txt    # Liste des dépendances
├── core/
│   ├── config.py       # Configuration sécurisée
│   ├── ports_db.py     # Base de données des services
│   └── reporter.py     # Cerveau du reporting Markdown
└── modules/            # Scripts d'attaque et de scan (V3)
    ├── ad_inquisitor.py
    ├── s3_scanner.py
    ├── secret_sniper.py
    ├── vuln_headers.py
    └── [..]

```

---

## 📈 Exemples de Commandes Rapides

```powershell
# Scanner une cible et identifier les failles connues
python arsenal.py scan -T 10.10.10.50

# Chasser les Buckets S3 d'une entreprise
python arsenal.py s3 -n nomentreprise

# Vérifier si un serveur Web expose son dossier .git
python arsenal.py secrets -u [http://cible.com](http://cible.com)

# Analyser la configuration de sécurité d'un site
python arsenal.py headers -u [https://site-audit.fr](https://site-audit.fr)

