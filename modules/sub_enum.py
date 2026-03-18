import asyncio
import aiohttp
import dns.resolver
import os 
from aiohttp import ClientTimeout
from modules.port_scan import async_scan
from core.utils import resolve_wordlist
from core.reporter import add_finding

async def fetch_crtsh(domain):
    """Reconnaissance OSINT (Passive) via crt.sh en asynchrone."""
    print(f"[*] Phase 1 : Reconnaissance OSINT (Certificats SSL) pour {domain}...")
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    subs = set()
    
    # --- CORRECTION PYLANCE ICI ---
    osint_timeout = ClientTimeout(total=20)
    
    try:
        async with aiohttp.ClientSession() as session:
            # On se fait passer pour un navigateur pour éviter les blocages
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            # Utilisation de l'objet osint_timeout
            async with session.get(url, headers=headers, timeout=osint_timeout) as resp:
                if resp.status == 200:
                    try:
                        data = await resp.json()
                        for entry in data:
                            name_value = entry.get('name_value', '')
                            for sub in name_value.split('\n'):
                                clean_sub = sub.strip().replace('*.', '')
                                # On s'assure que c'est bien un sous-domaine de notre cible
                                if clean_sub.endswith(domain) and clean_sub != domain:
                                    subs.add(clean_sub)
                    except:
                        pass
    except Exception as e:
        print(f"[-] Avertissement OSINT : Impossible de joindre crt.sh ({e})")
        
    print(f"[\033[92m+\033[0m] OSINT terminé : {len(subs)} sous-domaines potentiels trouvés dans les registres publics.")
    return subs

async def check_subdomain(target, results, auto_scan, semaphore):
    """Tente de résoudre un sous-domaine (Actif) et lance un scan si demandé."""
    async with semaphore:
        try:
            loop = asyncio.get_event_loop()
            answers = await loop.run_in_executor(None, dns.resolver.resolve, target, 'A')
            
            if answers:
                ips = [str(ip) for ip in answers]
                print(f"[\033[92m+\033[0m] VIVANT : \033[1m{target}\033[0m -> {', '.join(ips)}")
                results.append((target, ips))
                add_finding("Subdomain Enum", target, f"Résolution DNS active vers : {', '.join(ips)}")
                
                # --- AUTO-SCAN SI ACTIVÉ ---
                if auto_scan:
                    print(f"    [\033[94m*\033[0m] Lancement automatique du scan de ports sur {target}...")
                    # Scan rapide des 1000 premiers ports
                    await async_scan(target, 1, 1000, 50) 
                    
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout, Exception):
            pass

async def start_sub_enum(domain, wordlist_path, threads, auto_scan):
    print(f"\n\033[1m=== ÉNUMÉRATION HYBRIDE DES SOUS-DOMAINES ===\033[0m")
    
    # --- 1. PHASE OSINT (Passif) ---
    osint_targets = await fetch_crtsh(domain)
    
    # --- 2. PHASE DICTIONNAIRES (Mode Auto-Pilot) ---
    print(f"\n[*] Phase 2 : Préparation de l'armurerie DNS (Brute-Force)...")
    wordlists_to_load = []
    
    if wordlist_path == "auto":
        print("    [\033[94m*\033[0m] Mode Auto-Pilot : Fusion des dictionnaires en cours...")
        if os.path.exists("custom_wordlist.txt"):
            wordlists_to_load.append("custom_wordlist.txt")
        wordlists_to_load.append("subs_top5000.txt")
    else:
        wordlists_to_load.append(wordlist_path)

    brute_prefixes = set()
    for wl_name in wordlists_to_load:
        real_path = resolve_wordlist(wl_name)
        if not real_path: continue
            
        try:
            with open(real_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if line.strip(): brute_prefixes.add(line.strip())
        except Exception as e:
            print(f"[-] Erreur de lecture sur {wl_name} : {e}")

    # --- 3. FUSION MASSIVE ---
    all_targets = set(osint_targets) # On commence avec les trouvailles OSINT
    for prefix in brute_prefixes:
        all_targets.add(f"{prefix}.{domain}") # On ajoute nos générations brutes
        
    if not all_targets:
        print("[-] Aucune cible à tester. Arrêt.")
        return
        
    print(f"[*] Phase 3 : Vérification DNS (Résolution) sur \033[1m{len(all_targets)}\033[0m cibles combinées...")
    if auto_scan:
        print("    [\033[91m!\033[0m] Le mode AUTO-SCAN est activé. C'est parti pour le bruit.")

    # --- 4. EXÉCUTION ASYNCHRONE ---
    results = []
    semaphore = asyncio.Semaphore(threads)
    tasks = [check_subdomain(target, results, auto_scan, semaphore) for target in all_targets]
    
    await asyncio.gather(*tasks)
    
    print(f"\n[+] Mission accomplie. \033[1m{len(results)}\033[0m sous-domaines confirmés en ligne.")

def run_sub_enum(args):
    """Wrapper pour arsenal.py"""
    auto = getattr(args, 'auto_scan', False)
    asyncio.run(start_sub_enum(args.domain, args.wordlist, args.threads, auto))