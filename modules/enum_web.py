import asyncio
import aiohttp
import sys
from urllib.parse import urlparse

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

async def check_url(session, target_url, path, semaphore):
    """Vérifie un chemin spécifique de manière asynchrone."""
    url = f"{target_url}/{path.strip()}"
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

async def async_main(target, wordlist_path, concurrency):
    """Cœur asynchrone de l'énumérateur."""
    parsed_url = urlparse(target)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("[-] Erreur : URL invalide. Utilisez le format http:// ou https://")
        return

    print(f"[*] Démarrage de l'énumération sur {target} avec {concurrency} threads...")
    semaphore = asyncio.Semaphore(concurrency)
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as f:
            paths = f.readlines()
    except FileNotFoundError:
        print(f"[-] Erreur : Dictionnaire '{wordlist_path}' introuvable.")
        return

    headers = {'User-Agent': USER_AGENT}
    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        tasks = [check_url(session, target, path, semaphore) for path in paths]
        await asyncio.gather(*tasks)

def run_enum(args):
    """
    Fonction d'interface (Wrapper) appelée par arsenal.py.
    Elle fait le pont entre le monde synchrone (CLI) et asynchrone (Réseau).
    """
    try:
        asyncio.run(async_main(args.url, args.wordlist, args.threads))
    except KeyboardInterrupt:
        print("\n[-] Énumération interrompue par l'utilisateur.")