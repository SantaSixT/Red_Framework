import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from core.reporter import add_finding
from core.proxy_manager import get_connector # <--- Import du manager
from modules.cms_detect import detect_cms # <--- Import

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
        
        if not href or not isinstance(href, str):
            continue
            
        full_url = urljoin(base_url, href)
        
        if urlparse(full_url).netloc == base_domain:
            clean_url = full_url.split('#')[0]
            links.add(clean_url)
            
    return links

async def async_spider(start_url, max_depth, concurrency, proxy=None): # <--- Argument proxy ajouté
    await detect_cms(start_url)
    print(f"[*] Lancement du Spider sur {start_url} (Profondeur max: {max_depth})")
    if proxy:
        print(f"[\033[94m*\033[0m] Mode Furtif activé via : {proxy}")
    
    visited = set()
    to_visit = {start_url}
    
    headers = {'User-Agent': USER_AGENT}
    
    # On utilise ton ProxyManager pour obtenir le bon connecteur
    # Si proxy est None, get_connector renverra un TCPConnector standard ou None
    connector = get_connector(proxy)
    if not connector:
        connector = aiohttp.TCPConnector(limit=concurrency, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        for depth in range(max_depth + 1):
            if not to_visit:
                break
                
            print(f"[*] --- Exploration Profondeur {depth} ({len(to_visit)} URLs en file d'attente) ---")
            
            tasks = [fetch_page(session, url) for url in to_visit]
            html_results = await asyncio.gather(*tasks)
            
            visited.update(to_visit)
            next_urls = set()
            
            for html in html_results:
                if html:
                    new_links = await extract_links(html, start_url)
                    next_urls.update(new_links)
            
            to_visit = next_urls - visited
            
            # Sauvegarde des nouvelles découvertes
            for url in visited:
                add_finding("Web Spider", start_url, f"Page cartographiée : **{url}**")
                
    print(f"\n[+] Spider terminé. {len(visited)} pages uniques cartographiées.")

def run_spider(args):
    """Wrapper appelé par arsenal.py"""
    parsed = urlparse(args.url)
    if not parsed.scheme:
        print("[-] Erreur : URL invalide. Utilisez http:// ou https://")
        return
        
    try:
        # On passe args.proxy récupéré depuis la CLI
        proxy_url = getattr(args, 'proxy', None)
        asyncio.run(async_spider(args.url, args.depth, args.threads, proxy_url))
    except KeyboardInterrupt:
        print("\n[-] Spider arrêté par l'auditeur.")