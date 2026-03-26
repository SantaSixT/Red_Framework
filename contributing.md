# 🤝 Contribuer au Red_Framework

Vous souhaitez forger une nouvelle arme pour l'arsenal ? Voici les règles d'or pour garder le framework propre, rapide et asynchrone.

## 🏗️ Comment créer un nouveau module ?

1. **Créer le fichier :** Ajoutez votre script dans le dossier `modules/` (ex: `nouveau_module.py`). *Utilisez exclusivement des minuscules et des underscores.*
2. **La fonction principale :** Votre module doit posséder une fonction d'entrée qui accepte l'objet `args` d'Argparse.
   ```python
   def run_nouveau_module(args):
       print(f"Lancement sur l'URL : {args.url}")
   ```
3. **Déclarer dans `arsenal.py` :**
   * Importez votre module en haut du fichier : 
     `from modules.nouveau_module import run_nouveau_module`
   * Ajoutez le *subparser* avec vos arguments :
     ```python
     p_new = subparsers.add_parser("new", help="Description de l'outil")
     p_new.add_argument("-u", "--url", required=True)
     p_new.set_defaults(func=run_nouveau_module) # Ligne cruciale !
     ```

## ⚡ Bonnes Pratiques
* **Asynchrone d'abord :** Pour tout ce qui touche au réseau, utilisez `aiohttp` et `asyncio`. Bannissez la librairie standard `requests` qui bloque les threads.
* **Discrétion :** Prévoyez toujours des *Timeouts* courts (ex: 5 secondes) et passez toujours par la fonction de détection WAF (`core/waf.py`) avant de lancer un brute-force.
* **Couleurs :** Utilisez la classe `Colors` native pour vos affichages dans le terminal afin de garder une cohérence visuelle.

---