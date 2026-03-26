# 📜 Changelog - Red_Framework

Toutes les modifications notables apportées à ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/), et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [V7.0 Ultimate] - 2026-03-26

### 🚀 Ajouté
- **Module `intruder`** : Fuzzer asynchrone surpuissant clonant le comportement du Burp Suite Intruder. Permet l'injection de payloads via le marqueur `§FUZZ§` dans des requêtes HTTP brutes.
- **Module `decoder`** : Outil natif d'encodage/décodage à la volée (Base64, URL, Hex, HTML) pour préparer les payloads sans quitter le terminal.
- **Module `nuke`** : Lance-roquettes asynchrone ciblant les paramètres d'URL pour détecter les vulnérabilités RCE et LFI critiques.
- **Module `catch`** : Écouteur de Reverse Shell intelligent intégrant une stabilisation automatique du terminal (Auto-PTY).

### 🔄 Modifié
- Refonte de l'architecture de lancement dans `arsenal.py` : utilisation de `set_defaults(func=...)` pour un routage dynamique et propre des modules.
- Uniformisation des imports et sécurisation des chemins avec des fichiers `__init__.py` dans les répertoires `core/` et `modules/`.

### 🗑️ Supprimé
- **Dépendance `rich`** : Retrait complet de la librairie visuelle pour garantir une portabilité 100% native sur n'importe quel environnement Linux (sans nécessiter de `pip install` additionnel pour l'interface).

### 🐛 Corrigé
- Résolution du bug critique de sensibilité à la casse (Windows vs Linux) sur le fichier `shell_catcher.py` qui bloquait l'importation lors des `git pull`.

---

## [V6.0 Enterprise] - 2026-03-24

### 🚀 Ajouté
- **Système "Auto-Pilot" (Wordlists)** : Résolveur intelligent en cascade. Les modules cherchent d'abord une wordlist locale personnalisée avant de basculer silencieusement sur les standards SecLists dans `wordlists/`.
- **Module `api-hunter`** : Traque asynchrone des endpoints d'API (Swagger, OpenAPI) et des routes non documentées.
- **Module `vhost`** : Fuzzer de Virtual Hosts détectant les sous-domaines cachés sur une adresse IP unique en analysant les variations de taille/statut des réponses HTTP.
- **Bouclier Anti-Bannissement** : Implémentation de `core/waf.py` pour la détection dynamique des pare-feux applicatifs (WAF) avant de lancer un fuzzing massif.

### 🔄 Modifié
- Optimisation du module `brute-web` pour inclure la gestion des cookies de session et la fixation de session pour contourner certains CAPTCHAs.

---

## [V5.0 Core Edition] - 2026-03-18

### 🚀 Ajouté
- **Moteur Asynchrone Global** : Transition du framework vers `asyncio` et `aiohttp` pour des performances réseau extrêmes.
- **Module `update`** : Gestionnaire de ressources permettant le téléchargement automatique des dépôts SecLists essentiels.
- **Générateur HTML** : Export automatique des découvertes (findings) vers un dashboard HTML interactif et professionnel.
- Modules de base opérationnels : `sub` (hybride OSINT/DNS), `enum`, `spider`, `crack` (State Management), `scan`, `c2` (Multi-sessions), `payload`, `cms`, `secrets`, `headers`, `smb`, `s3`, `ldap`, `js-sniper`, `docker`.

### ⚙️ Architecture
- Séparation stricte du code en `core/` (moteur, proxy, WAF, utils) et `modules/` (logique offensive).