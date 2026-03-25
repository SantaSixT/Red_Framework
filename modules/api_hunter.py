import asyncio
import aiohttp
import os
from urllib.parse import urlparse
from core.reporter import add_finding
from core.waf import detect_waf

# Liste "Auto-Pilot" des cibles les plus juteuses pour une API
COMMON_API_PATHS = [
    "swagger.json", "api/swagger.json", "swagger-ui.html", "api-docs", 
    "v1/api-docs", "v2/api-docs", "openapi.json", "api/openapi.json",
    "graphql", "api/graphql", "api/v1/users", "api/v1/admin",
    "docs", "api/docs"
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Red_Framework/1.0"

async def check_api_endpoint(session, base_url, path, semaphore):
    """Vérifie un endpoint d'API et analyse sa réponse."""
    clean_path = path.strip().lstrip('/')
    url = f"{base_url}/{clean_path}"
    
    async with semaphore:
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            # On utilise une méthode GET classique pour la découverte
            async with session.get(url, allow_redirects=False, timeout=timeout) as response:
                status = response.status
                content_type = response.headers.get('Content-Type', '').lower()
                
                if status in [200, 401, 403]:
                    # Analyse du contenu pour voir si c'est un Swagger/OpenAPI
                    is_swagger = False
                    if "application/json" in content_type:
                        try:
                            # On lit un petit bout de la réponse pour ne pas saturer la RAM
                            text = await response.text()
                            if "swagger" in text[:500].lower() or "openapi" in text[:500].lower():
                                is_swagger = True
                        except Exception:
                            pass
                    
                    # Affichage et formatage des découvertes
                    if is_swagger:
                        print(f"[\033[91m!\033[0m] \033[1mJACKPOT API (Swagger/OpenAPI)\033[0m : {url}")
                        add_finding("API Hunter", base_url, f"🚨 Documentation d'API exposée : **{url}**")
                    elif status == 200:
                        print(f"[\033[92m+\033[0m] {status} - Endpoint actif : {url} (Type: {content_type})")
                        add_finding("API Hunter", base_url, f"Endpoint Actif ({status}) : **{url}**")
                    else:
                        print(f"[\033[93m*\033[0m] {status} - Endpoint restreint : {url}")
                        add_finding("API Hunter", base_url, f"Endpoint Restreint ({status}) : **{url}**")
                        
                    return 1
        except Exception:
            pass
    return 0

async def async_api_hunt(target, wordlist_path, threads):
    """Moteur asynchrone du chasseur d'API."""
    parsed_url = urlparse(target)
    if not parsed_url.scheme:
        print("[-] Erreur : URL invalide. Utilisez le format http://")
        return

    # Chargement des chemins (Auto-Pilot ou fichier custom)
    paths_to_test = []
    if wordlist_path.lower() == "auto":
        print("[\033[94m*\033[0m] Mode Auto-Pilot : Chasse aux documentations Swagger/OpenAPI.")
        paths_to_test = COMMON_API_PATHS
    else:
        try:
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                paths_to_test = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[-] Erreur : Dictionnaire '{wordlist_path}' introuvable.")
            return

    print(f"[*] Traque d'API sur {target} ({len(paths_to_test)} cibles) avec {threads} threads...")
    
    semaphore = asyncio.Semaphore(threads)
    headers = {'User-Agent': USER_AGENT, 'Accept': 'application/json'}
    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        tasks = [check_api_endpoint(session, target, path, semaphore) for path in paths_to_test]
        results = await asyncio.gather(*tasks)

    fichiers_trouves = sum(results)
    print("\n-------------------------------------------------")
    if fichiers_trouves == 0:
        print("[\033[93m-\033[0m] Bilan : Aucun endpoint d'API ou Swagger exposé n'a été trouvé.")
    else:
        print(f"[\033[92m+\033[0m] Bilan : \033[1m{fichiers_trouves} endpoint(s)\033[0m d'API découvert(s) !")
    print("-------------------------------------------------")

def run_api_hunter(args):
    """Wrapper pour arsenal.py"""
    
    # 1. PRE-FLIGHT CHECK : DÉTECTION DE WAF
    has_waf, reason = asyncio.run(detect_waf(args.url))
    if has_waf:
        print(f"\n[\033[93m!\033[0m] \033[1mATTENTION : WAF DÉTECTÉ SUR L'API !\033[0m")
        print(f"    -> Raison : {reason}")
        choix = input("[?] Lancer la traque quand même ? (o/N) : ")
        if choix.lower() != 'o':
            print("[-] Annulation.")
            return

    # 2. LANCEMENT
    try:
        asyncio.run(async_api_hunt(args.url, args.wordlist, args.threads))
    except KeyboardInterrupt:
        print("\n[-] Traque d'API interrompue par l'utilisateur.")