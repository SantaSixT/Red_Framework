import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from core.reporter import add_finding

# On simule un navigateur légitime
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

async def fetch_page(session, url):
    """Télécharge le contenu HTML d'une page."""
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                html = await response.text()
                return html
    except Exception:
        pass
    return None

async def extract_links(html, base_url):
    """Analyse le HTML et extrait tous les liens appartenant au même domaine."""
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    base_domain = urlparse(base_url).netloc

    for a_tag in soup.find_all('a', href=True):
        href = a_tag.get('href')
        
        # --- CORRECTION PYLANCE ---
        # On s'assure que href existe et qu'il est strictement une chaîne de caractères (str)
        if not href or not isinstance(href, str):
            continue
            
        # On transforme les liens relatifs (/contact) en liens absolus (http://site.com/contact)
        full_url = urljoin(base_url, href)
        
        # On vérifie qu'on reste sur la cible (on ne veut pas scanner tout Internet !)
        if urlparse(full_url).netloc == base_domain:
            # On enlève les ancres (#) pour ne pas scanner la même page 10 fois
            clean_url = full_url.split('#')[0]
            links.add(clean_url)
            
    return links

async def async_spider(start_url, max_depth, concurrency):
    print(f"[*] Lancement du Spider sur {start_url} (Profondeur max: {max_depth})")
    
    visited = set()
    to_visit = {start_url}
    
    headers = {'User-Agent': USER_AGENT}
    connector = aiohttp.TCPConnector(limit=concurrency, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        for depth in range(max_depth + 1):
            if not to_visit:
                break
                
            print(f"[*] --- Exploration Profondeur {depth} ({len(to_visit)} URLs en file d'attente) ---")
            
            # On prépare les tâches pour toutes les URLs du niveau actuel
            tasks = [fetch_page(session, url) for url in to_visit]
            html_results = await asyncio.gather(*tasks)
            
            # On marque les URLs actuelles comme visitées
            visited.update(to_visit)
            next_urls = set()
            
            # On extrait les nouveaux liens de chaque page téléchargée
            for html in html_results:
                if html:
                    new_links = await extract_links(html, start_url)
                    next_urls.update(new_links)
            
            # On garde seulement les liens qu'on n'a pas encore visités
            to_visit = next_urls - visited
            
            # --- SAUVEGARDE V2 ---
            for url in visited:
                add_finding("Web Spider", start_url, f"Page cartographiée : **{url}**")
                
    print(f"\n[+] Spider terminé. {len(visited)} pages uniques cartographiées et sauvegardées dans le rapport.")

def run_spider(args):
    """Wrapper appelé par arsenal.py"""
    parsed = urlparse(args.url)
    if not parsed.scheme:
        print("[-] Erreur : URL invalide. Utilisez http:// ou https://")
        return
        
    try:
        asyncio.run(async_spider(args.url, args.depth, args.threads))
    except KeyboardInterrupt:
        print("\n[-] Spider arrêté par l'auditeur.")