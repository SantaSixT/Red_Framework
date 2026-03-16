# ⚔️ Red_Framework (Arsenal)

Un framework d'automatisation Red Team développé en Python, orienté opérations asynchrones, OSINT et post-exploitation. Conçu pour la vitesse, la modularité et la furtivité.

> ⚠️ **Avertissement Légal :** Cet outil a été développé à des fins d'éducation en cybersécurité (DevSecOps Lab) et pour une utilisation lors d'audits Red Team autorisés. L'utilisation de cet outil contre des cibles sans consentement écrit est illégale.

## 🛠️ Installation

```powershell
# Cloner le dépôt
git clone [https://github.com/votre-nom/Red_Framework.git](https://github.com/votre-nom/Red_Framework.git)
cd Red_Framework

# Installer les dépendances
pip install -r requirements.txt

```
## 🚀 Utilisation des Modules
Le framework est piloté par le routeur principal arsenal.py. Utilisez l'argument -h sur n'importe quel module pour voir les options détaillées.

1. Génération de Dictionnaire (wordlist)
Forge une liste de mots de passe mutés (Leet Speak, suffixes d'années) à partir de mots-clés ciblés, optimisée pour l'entreprise auditée.

```powershell
python arsenal.py wordlist -k "entreprise, admin, dev"
```

2. Énumération Web Asynchrone (enum)
Découverte agressive et asynchrone de répertoires et fichiers cachés. Supporte l'ajout d'extensions à la volée pour trouver des fichiers de sauvegarde sensibles.

```powershell
python arsenal.py enum -u [http://cible.com](http://cible.com) -w custom_wordlist.txt -t 50 -e .bak,.txt,.php
```

3. Reconnaissance OSINT de Sous-domaines (subdomain)
Découverte furtive et passive de sous-domaines en interrogeant l'API publique des logs de Certificate Transparency (crt.sh). N'envoie aucun paquet à la cible.

```powershell
python arsenal.py subdomain -d cible.com
```

4. Brute-Force HTTP POST (brute)
Attaque asynchrone par force brute sur des formulaires de connexion web standards.

```powershell
python arsenal.py brute -u [http://cible.com/login.php](http://cible.com/login.php) -user "admin" -w custom_wordlist.txt -t 20
```

5. Scanner de Ports TCP Furtif (scan)
Cartographie asynchrone des services exposés (TCP Full Connect). Utilise une base de données de signatures intégrée (core/ports_db.py) pour le Service Fingerprinting.

```powershell
python arsenal.py scan -T 192.168.1.10 -s 1 -e 1000 -t 200
```

6. Serveur Command & Control (c2)
Serveur d'écoute local permettant d'intercepter les connexions entrantes (Reverse Shells) lors de la phase de post-exploitation.

```powershell
python arsenal.py c2 -l 0.0.0.0 -p 4444
```

## 🏗️Architecture
* arsenal.py : Routeur CLI principal.

* core/ : Configurations globales, gestion des secrets, bases de données de signatures.

* modules/ : Scripts d'attaque autonomes (Enum, Brute, Scan, etc.).

---

Amélioration
1.  **L'Usine à Payloads (Obfuscation) :** Créer un module `payload_gen.py` qui prend une commande (ex: `whoami`) et génère une version encodée (Base64, Hex) ou un "One-Liner" PowerShell obscurci. L'objectif est de comprendre comment les attaquants cachent leur code source pour échapper aux règles statiques des EDR et des WAF (Web Application Firewalls).
2.  **Le "Banner Grabber" (Vulnérabilités) :** Améliorer notre scanner de ports réseau. Actuellement, il devine le service (ex: "Port 22 = SSH"). Nous pouvons lui apprendre à capturer la "Bannière", c'est-à-dire lire la vraie réponse du serveur pour extraire la version exacte du logiciel (ex: `OpenSSH 7.2p2`), ce qui permet ensuite de chercher les exploits associés (CVE).
3.  **L'Extracteur de Métadonnées (Ingénierie Sociale) :** Un outil qui télécharge un PDF public depuis un site cible et lit les métadonnées cachées (EXIF) pour y trouver le nom complet du créateur, son système d'exploitation et sa version d'Adobe/Word. Le point de départ parfait pour une attaque de Phishing.