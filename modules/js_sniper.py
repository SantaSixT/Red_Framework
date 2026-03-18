import asyncio
import aiohttp
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from core.reporter import add_finding

# ==========================================
# DICTIONNAIRE DES REGEX (L'Arsenal du Sniper)
# ==========================================
REGEX_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "Stripe Standard API": r"sk_live_[0-9a-zA-Z]{24}",
    "Stripe Restricted API": r"rk_live_[0-9a-zA-Z]{24}",
    "Generic Token/Secret": r"(?i)(?:secret|token|api_key|password)[\s=:\"']{1,5}([a-zA-Z0-9\-_]{16,})",
    "Hidden API Endpoints": r"(?<=[\"'])(/api/v[0-9]/[a-zA-Z0-9_\-\/]+)(?=[\"'])" # Cherche les routes type /api/v1/users
}

async def fetch_content(session, url):
    """Télécharge le contenu d'une URL de manière asynchrone."""
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return await response.text()
    except Exception:
        pass
    return None

def analyze_js(js_content, js_url):
    """Passe le code JS à la moulinette des Regex."""
    found_something = False
    
    for name, pattern in REGEX_PATTERNS.items():
        matches = set(re.findall(pattern, js_content))
        if matches:
            found_something = True
            print(f"\n[\033[91m!\033[0m] {name} trouvé(e) dans \033[96m{js_url}\033[0m :")
            for match in matches:
                print(f"    -> \033[1m{match}\033[0m")
                add_finding("JS Sniper", js_url, f"{name} : **{match}**")
                
    if not found_something:
        print(f"[-] Rien d'intéressant dans {js_url.split('/')[-1]}")

async def start_sniper(target_url, threads):
    print(f"[*] Démarrage du JS Sniper sur : {target_url}")
    
    js_urls = set()
    
    async with aiohttp.ClientSession() as session:
        # 1. Si on vise une page HTML, on extrait tous ses scripts JS
        if not target_url.endswith('.js'):
            print("[*] Analyse de la page HTML pour trouver les fichiers JavaScript...")
            html = await fetch_content(session, target_url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                scripts = soup.find_all('script')
                for script in scripts:
                    src = script.get('src')
                    # CORRECTION PYLANCE : On s'assure que src est bien du texte
                    if src and isinstance(src, str):
                        # Reconstruit l'URL complète si c'est un chemin relatif
                        full_url = urljoin(target_url, src)
                        js_urls.add(full_url)
        else:
            # On vise directement un fichier JS
            js_urls.add(target_url)

        if not js_urls:
            print("[-] Aucun fichier JavaScript trouvé sur cette cible.")
            return
            
        print(f"[\033[92m+\033[0m] \033[1m{len(js_urls)}\033[0m fichiers JavaScript mis en joue. Lancement de l'analyse...")
        
        # 2. Téléchargement et analyse asynchrone des fichiers JS
        semaphore = asyncio.Semaphore(threads)
        
        async def process_js(url):
            async with semaphore:
                content = await fetch_content(session, url)
                if content:
                    analyze_js(content, url)
                    
        tasks = [process_js(url) for url in js_urls]
        await asyncio.gather(*tasks)

    print("\n[*] Mission du JS Sniper terminée.")

def run_js_sniper(args):
    """Wrapper pour arsenal.py"""
    asyncio.run(start_sniper(args.url, args.threads))