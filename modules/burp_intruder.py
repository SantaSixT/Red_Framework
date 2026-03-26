import asyncio
import aiohttp
import os
from core.reporter import add_finding

async def send_fuzzed_request(session, method, url, headers, body, payload, baseline, semaphore):
    """Envoie une requête avec le payload injecté à la place de §FUZZ§."""
    # Remplacement magique dans tous les composants de la requête
    f_url = url.replace("§FUZZ§", payload)
    f_body = body.replace("§FUZZ§", payload) if body else ""
    f_headers = {k: v.replace("§FUZZ§", payload) for k, v in headers.items()}
    
    async with semaphore:
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.request(method, f_url, headers=f_headers, data=f_body, timeout=timeout, allow_redirects=False) as resp:
                content = await resp.read()
                status = resp.status
                size = len(content)
                
                # On compare avec la baseline (la requête sans payload)
                # Si le statut ou la taille change significativement, on affiche !
                if status != baseline['status'] or abs(size - baseline['size']) > 30:
                    print(f"[\033[92m+\033[0m] Payload: \033[1m{payload:<20}\033[0m | Status: \033[93m{status}\033[0m | Taille: {size}")
                    add_finding("Intruder", f_url, f"Anomalie avec le payload **{payload}** (Status: {status}, Taille: {size})")
                    return 1
        except Exception:
            pass
    return 0

def parse_raw_request(filepath, scheme="http", port=80):
    """Parse un fichier texte contenant une requête HTTP brute style Burp Suite."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read().replace('\r\n', '\n') # Normalisation des retours à la ligne
        
    parts = raw.split('\n\n', 1)
    header_block = parts[0]
    body = parts[1] if len(parts) > 1 else ""
    
    lines = header_block.split('\n')
    method, path, _ = lines[0].split(' ', 2)
    
    headers = {}
    for line in lines[1:]:
        if ':' in line:
            k, v = line.split(':', 1)
            headers[k.strip()] = v.strip()
            
    host = headers.get('Host', '127.0.0.1')
    url = f"{scheme}://{host}:{port}{path}"
    
    return method, url, headers, body

async def async_intruder(req_file, wordlist, threads, scheme, port):
    print(f"[*] Analyse de la requête brute : {req_file}")
    
    try:
        method, url, headers, body = parse_raw_request(req_file, scheme, port)
    except Exception as e:
        print(f"[-] Erreur lors du parsing de la requête : {e}")
        return

    # Vérification que le marqueur est bien présent
    if "§FUZZ§" not in url and "§FUZZ§" not in body and not any("§FUZZ§" in v for v in headers.values()):
        print("[-] Erreur : Le marqueur '§FUZZ§' n'a pas été trouvé dans la requête (URL, Headers ou Body).")
        return

    try:
        with open(wordlist, 'r', encoding='utf-8') as f:
            payloads = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[-] Erreur de dictionnaire : {e}")
        return

    print(f"[*] Démarrage de l'Intruder ({len(payloads)} payloads) sur la cible...")

    semaphore = asyncio.Semaphore(threads)
    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        # 1. Établir la Baseline (On remplace FUZZ par une chaîne vide pour voir la réponse par défaut)
        print("[*] Calcul de la Baseline (réponse par défaut)...")
        baseline = {'status': 0, 'size': 0}
        timeout = aiohttp.ClientTimeout(total=5)
        try:
            b_url = url.replace("§FUZZ§", "")
            b_body = body.replace("§FUZZ§", "")
            b_headers = {k: v.replace("§FUZZ§", "") for k, v in headers.items()}
            
            async with session.request(method, b_url, headers=b_headers, data=b_body, timeout=timeout, allow_redirects=False) as resp:
                baseline['status'] = resp.status
                baseline['size'] = len(await resp.read())
            print(f"[*] Baseline établie -> Status: {baseline['status']}, Taille: {baseline['size']}")
        except Exception as e:
            print(f"[-] Impossible d'établir la Baseline : {e}")
            return

        # 2. Lancer l'attaque asynchrone
        print("\n[*] --- DÉBUT DU FUZZING ---")
        tasks = [send_fuzzed_request(session, method, url, headers, body, p, baseline, semaphore) for p in payloads]
        results = await asyncio.gather(*tasks)

    print("\n-------------------------------------------------")
    print(f"[*] Intruder terminé. {sum(results)} anomalies détectées.")
    print("-------------------------------------------------")

def run_intruder(args):
    try:
        asyncio.run(async_intruder(args.request, args.wordlist, args.threads, args.scheme, args.port))
    except KeyboardInterrupt:
        print("\n[-] Intruder interrompu.")