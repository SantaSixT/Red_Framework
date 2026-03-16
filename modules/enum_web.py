import asyncio
import aiohttp
import sys
from urllib.parse import urlparse

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

async def check_url(session, target_url, path, semaphore):
    """Vérifie un chemin spécifique de manière asynchrone."""
    # Nettoyage pour éviter les doubles slashes si le path commence par un /
    clean_path = path.strip().lstrip('/')
    url = f"{target_url}/{clean_path}"
    
    async with semaphore:
        try:
            async with session.get(url, allow_redirects=False, timeout=5) as response:
                status = response.status
                if status != 404:
                    print(f"[+] {status} - {url}")
        except asyncio.TimeoutError:
            pass
        except aiohttp.ClientError:
            pass

async def async_main(target, wordlist_path, concurrency, extensions=""):
    """Cœur asynchrone de l'énumérateur, maintenant avec support des extensions."""
    parsed_url = urlparse(target)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("[-] Erreur : URL invalide. Utilisez le format http:// ou https://")
        return

    try:
        with open(wordlist_path, 'r', encoding='utf-8') as f:
            base_paths = f.readlines()
    except FileNotFoundError:
        print(f"[-] Erreur : Dictionnaire '{wordlist_path}' introuvable.")
        return

    # ==========================================
    # LOGIQUE DE MUTATION (Extensions)
    # ==========================================
    paths_to_test = []
    # On sépare les extensions fournies par des virgules et on les nettoie
    ext_list = [e.strip() for e in extensions.split(',')] if extensions else []
    
    for path in base_paths:
        clean_path = path.strip()
        if not clean_path:
            continue
            
        # 1. On ajoute le mot de base (ex: "admin")
        paths_to_test.append(clean_path)
        
        # 2. On ajoute les variantes avec extensions (ex: "admin.bak")
        for ext in ext_list:
            if ext:
                paths_to_test.append(f"{clean_path}{ext}")

    print(f"[*] Démarrage de l'énumération sur {target} avec {concurrency} threads...")
    print(f"[*] Total des chemins à tester (mots de base + extensions) : {len(paths_to_test)}")
    
    semaphore = asyncio.Semaphore(concurrency)
    headers = {'User-Agent': USER_AGENT}
    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        tasks = [check_url(session, target, path, semaphore) for path in paths_to_test]
        await asyncio.gather(*tasks)

def run_enum(args):
    """
    Fonction d'interface (Wrapper) appelée par arsenal.py.
    Elle fait le pont entre le monde synchrone (CLI) et asynchrone (Réseau).
    """
    try:
        # Pratique de Dev Défensif : getattr() permet de ne pas crasher si 
        # arsenal.py n'a pas encore été mis à jour avec l'argument --extensions
        exts = getattr(args, 'extensions', '')
        asyncio.run(async_main(args.url, args.wordlist, args.threads, exts))
    except KeyboardInterrupt:
        print("\n[-] Énumération interrompue par l'utilisateur.")