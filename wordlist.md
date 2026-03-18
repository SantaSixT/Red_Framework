# 🧠 Système de Dictionnaires (Wordlists) - Red_Framework

Le framework intègre un écosystème de gestion de dictionnaires conçu pour l'agilité. Fini la gestion manuelle des chemins de fichiers lors des audits : l'outil télécharge, génère et résout les chemins automatiquement.

## ⚙️ Architecture

Le cœur du système repose sur le résolveur intelligent situé dans `core/utils.py`.
Lorsqu'un module (comme `brute-web`, `sub`, ou `crack`) demande une wordlist, le framework effectue une recherche en deux temps :
1. **Priorité 1 :** Il cherche dans le répertoire courant (idéal pour les listes générées spécifiquement pour la cible).
2. **Priorité 2 :** Si introuvable, il cherche automatiquement dans le dossier `wordlists/` (où sont stockées les listes SecLists standards).

---

## 📥 1. Téléchargement des standards (SecLists)

Au début d'un audit ou lors d'une nouvelle installation, peuplez votre arsenal avec les standards de l'industrie (Top 10k passwords, Top Users, Subdomains).

**Commande :**
`python arsenal.py update`

**Action :** Télécharge de manière asynchrone les fichiers essentiels depuis le dépôt GitHub SecLists et les stocke dans le dossier `./wordlists/`. Les fichiers inexistants (Erreurs 404) sont ignorés avec élégance.

---

## 🛠️ 2. Génération Hybride (Intelligence)

Les attaques par force brute modernes requièrent des listes chirurgicales. Le framework peut générer des mots de passe mutés (Leetspeak, ajout d'années, caractères spéciaux) basés sur un ou plusieurs mots-clés, et les fusionner avec la liste des mots de passe les plus communs.

**Commande :**
`python arsenal.py wordlist -k "entreprise,admin" -o custom_wordlist.txt`

**Action :**
1. Génère les mutations pour "entreprise" et "admin" (ex: `Entreprise2026!`, `@dmin123`).
2. Injecte automatiquement les mots de passe du fichier `wordlists/pass_top10k.txt` (s'il a été téléchargé via `update`).
3. Trie, dé-doublonne et sauvegarde le tout dans `custom_wordlist.txt`.

---

## 🚀 3. Utilisation Transparente (QoL)

Grâce au résolveur, appelez directement vos listes par leur nom, sans vous soucier des chemins relatifs ou absolus.

**Exemples de commandes fluides :**

* **Casser un Hash avec une liste téléchargée :**
    `python arsenal.py crack -s <hash> -w pass_top10k.txt`
* **Brute-force Web avec votre liste générée :**
    `python arsenal.py brute-web -u http://cible.com/login -U users_top.txt -w custom_wordlist.txt`
* **Énumération de sous-domaines :**
    `python arsenal.py sub -d cible.com -w subs_top5000.txt`