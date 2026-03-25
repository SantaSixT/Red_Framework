import asyncio
import aiohttp
from core.reporter import add_finding

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Red_Framework/1.0"

async def check_vhost(session, ip, domain, word, baseline_size, baseline_status, semaphore):
    """Teste un sous-domaine spécifique en modifiant le header Host."""
    vhost = f"{word}.{domain}"
    headers = {
        "Host": vhost,
        "User-Agent": USER_AGENT
    }
    
    async with semaphore:
        try:
            # L'objet Timeout correct
            timeout = aiohttp.ClientTimeout(total=5)
            # On tape sur l'IP, mais on prétend être le VHost
            async with session.get(f"http://{ip}", headers=headers, allow_redirects=False, timeout=timeout) as resp:
                content = await resp.read()
                size = len(content)
                status = resp.status
                
                # Si la taille ou le statut est différent de la page par défaut, on a trouvé quelque chose !
                # On tolère une petite variation de taille (ex: un timestamp qui change sur la page)
                if abs(size - baseline_size) > 50 or status != baseline_status:
                    print(f"[\033[92m+\033[0m] VHost découvert : \033[1m{vhost}\033[0m (Status: {status}, Taille: {size})")
                    add_finding("VHost Hunter", ip, f"VHost trouvé: **{vhost}** (Status: {status}, Taille: {size})")
                    return 1
        except Exception:
            pass
    return 0

async def async_vhost_hunt(ip, domain, wordlist_path, threads):
    print(f"[*] Démarrage du VHost Hunter sur {ip} (Domaine cible: {domain})")
    
    # 1. Obtenir la baseline (la réponse par défaut du serveur)
    baseline_size = 0
    baseline_status = 0
    try:
        # CORRECTION PYLANCE ICI : Création de l'objet Timeout pour la baseline
        timeout_baseline = aiohttp.ClientTimeout(total=5)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{ip}", headers={"Host": domain, "User-Agent": USER_AGENT}, timeout=timeout_baseline) as resp:
                content = await resp.read()
                baseline_size = len(content)
                baseline_status = resp.status
        print(f"[*] Baseline établie : Status {baseline_status}, Taille {baseline_size} octets.")
    except Exception as e:
        print(f"[-] Impossible de joindre l'IP pour la baseline : {e}")
        return

    # 2. Charger le dictionnaire
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Dictionnaire introuvable : {wordlist_path}")
        return

    # 3. Lancer l'attaque asynchrone
    semaphore = asyncio.Semaphore(threads)
    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_vhost(session, ip, domain, word, baseline_size, baseline_status, semaphore) for word in words]
        results = await asyncio.gather(*tasks)

    # Bilan
    trouves = sum(results)
    print("\n-------------------------------------------------")
    if trouves == 0:
        print("[\033[93m-\033[0m] Aucun Virtual Host caché trouvé.")
    else:
        print(f"[\033[92m+\033[0m] \033[1m{trouves} VHost(s)\033[0m découvert(s) !")
    print("-------------------------------------------------")

def run_vhost_hunter(args):
    try:
        asyncio.run(async_vhost_hunt(args.ip, args.domain, args.wordlist, args.threads))
    except KeyboardInterrupt:
        print("\n[-] VHost Hunter interrompu.")