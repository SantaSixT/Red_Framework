```markdown
# 🚑 Dépannage & Erreurs Fréquentes (Troubleshooting)

Ce guide recense les erreurs les plus courantes lors de l'installation ou de l'exécution du Red_Framework, et comment les résoudre en quelques secondes.

### ❌ Erreur : `ModuleNotFoundError: No module named 'rich'` (ou aiohttp)
**Cause :** Vous n'avez pas activé votre environnement virtuel, ou vous avez oublié d'installer les dépendances.
**Solution :**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### ❌ Erreur : `ModuleNotFoundError: No module named 'modules.shell_catcher'`
**Cause :** Problème de sensibilité à la casse (Majuscule/Minuscule) très fréquent lors d'un `git pull` entre Windows et Linux. Windows tolère `Shell_catcher.py`, Linux le rejette.
**Solution (Sur le Linux ciblé) :**
Allez dans le dossier `modules/` et forcez le renommage en minuscules :
```bash
mv Shell_catcher.py shell_catcher.py
```

### ❌ Erreur : Le script fige ou crash avec `Too many open files`
**Cause :** Les modules asynchrones (comme le `scan` ou l'`intruder`) ouvrent des milliers de sockets. Votre système Linux limite ce nombre par défaut (souvent à 1024).
**Solution :** Augmentez la limite de votre terminal avant de lancer l'arsenal :
```bash
ulimit -n 65535
```
```

---