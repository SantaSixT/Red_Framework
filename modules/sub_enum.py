import asyncio
import dns.resolver
from core.reporter import add_finding
from modules.port_scan import async_scan  # <--- On importe le moteur du scanner

async def check_subdomain(domain, sub, results, auto_scan):
    """Tente de résoudre un sous-domaine et lance un scan si demandé."""
    target = f"{sub}.{domain}"
    try:
        loop = asyncio.get_event_loop()
        answers = await loop.run_in_executor(None, dns.resolver.resolve, target, 'A')
        
        if answers:
            ips = [str(ip) for ip in answers]
            print(f"[\033[92m+\033[0m] Trouvé : \033[1m{target}\033[0m -> {', '.join(ips)}")
            results.append((target, ips))
            
            # --- AUTO-SCAN SI ACTIVÉ ---
            if auto_scan:
                print(f"    [\033[94m*\033[0m] Lancement automatique du scan de ports sur {target}...")
                # On scanne les ports les plus courants (Top 20) pour aller vite
                await async_scan(target, 1, 1000, 50) 
                
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout, Exception):
        pass

async def start_sub_enum(domain, wordlist_path, threads, auto_scan):
    print(f"[*] Énumération des sous-domaines pour : {domain}")
    if auto_scan:
        print(f"[*] Mode AUTO-SCAN activé (Ports 1-1000).")
        
    results = []
    
    try:
        with open(wordlist_path, 'r') as f:
            subs = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Erreur : Dictionnaire {wordlist_path} introuvable.")
        return

    # On utilise un Sémaphore pour ne pas saturer le DNS
    semaphore = asyncio.Semaphore(threads)
    
    async def wrapped_check(sub):
        async with semaphore:
            await check_subdomain(domain, sub, results, auto_scan)

    tasks = [wrapped_check(sub) for sub in subs]
    await asyncio.gather(*tasks)

    # ... (reste de la fonction identique pour le rapport) ...

def run_sub_enum(args):
    """Wrapper pour arsenal.py"""
    # On récupère l'option auto-scan
    auto = getattr(args, 'auto_scan', False)
    asyncio.run(start_sub_enum(args.domain, args.wordlist, args.threads, auto))