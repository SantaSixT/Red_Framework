import hashlib
import os
from core.reporter import add_finding
from core.utils import resolve_wordlist
from core.session import save_state, get_state, clear_state  # <--- Ajout des imports de session

def run_crack(args):
    target_hash = args.hash.lower()
    algo = getattr(args, 'algo', 'md5').lower()
    
    print(f"[*] Démarrage du cracking hors-ligne")
    print(f"[*] Cible : {target_hash} (Algo: {algo.upper()})")
    
    wordlists_to_try = []
    if args.wordlist == "auto":
        if os.path.exists("custom_wordlist.txt"):
            wordlists_to_try.append("custom_wordlist.txt")
        wordlists_to_try.append("pass_top10k.txt")
    else:
        wordlists_to_try.append(args.wordlist)

    # ==========================================
    # GESTION DE LA REPRISE SUR ERREUR
    # ==========================================
    start_index = 0
    resume_wl = None
    state = get_state("crack", target_hash)
    
    if state:
        print(f"\n[\033[93m!\033[0m] SESSION PRÉCÉDENTE DÉTECTÉE !")
        print(f"    Dictionnaire : {state['wordlist']}")
        print(f"    Progression  : Mot n° {state['index']}")
        
        rep = input("    Voulez-vous reprendre là où vous vous étiez arrêté ? (O/n) : ")
        if rep.lower() != 'n':
            start_index = state['index']
            resume_wl = state['wordlist']
            print("[\033[92m+\033[0m] Reprise de l'attaque en cours...")
        else:
            print("[*] Nouvelle attaque ignorée, on recommence à zéro.")
            clear_state("crack", target_hash)

    # --- LECTURE ET CASSAGE ---
    skip_wordlists = (resume_wl is not None)

    for wl_name in wordlists_to_try:
        # Si on reprend, on ignore les dictionnaires qui ont déjà été passés
        if skip_wordlists:
            if wl_name != resume_wl:
                continue
            else:
                skip_wordlists = False # On a trouvé le dictionnaire, on arrête d'ignorer

        real_path = resolve_wordlist(wl_name)
        if not real_path:
            continue
            
        print(f"[*] Analyse en cours avec l'arsenal : \033[1m{wl_name}\033[0m ...")
        
        try:
            with open(real_path, 'r', encoding='utf-8', errors='ignore') as f:
                for index, line in enumerate(f):
                    
                    # On "avance rapide" jusqu'à l'index sauvegardé
                    if index < start_index:
                        continue
                    
                    # SAUVEGARDE SILENCIEUSE EN ARRIÈRE-PLAN
                    # Tous les 50 000 mots, on met à jour le fichier .red_session
                    if index > 0 and index % 50000 == 0:
                        save_state("crack", target_hash, index, wl_name)

                    word = line.strip()
                    if not word: continue
                    
                    # Hashage
                    if algo == 'md5': hashed_word = hashlib.md5(word.encode()).hexdigest()
                    elif algo == 'sha1': hashed_word = hashlib.sha1(word.encode()).hexdigest()
                    elif algo == 'sha256': hashed_word = hashlib.sha256(word.encode()).hexdigest()
                    else: return
                    
                    # Vérification
                    if hashed_word == target_hash:
                        print(f"\n[\033[92m+\033[0m] BINGO ! Hash cassé !")
                        print(f"[\033[92m+\033[0m] Mot de passe en clair : \033[1m{word}\033[0m")
                        add_finding("Hash Cracker", target_hash, f"Mot de passe cassé : **{word}**")
                        
                        # LE MOT DE PASSE EST TROUVÉ : On nettoie la session !
                        clear_state("crack", target_hash)
                        return 
                        
            # Si le dictionnaire entier a été lu sans succès, on remet l'index à 0 pour le dictionnaire suivant
            start_index = 0 
            
        except Exception as e:
            print(f"[-] Erreur de lecture sur {wl_name} : {e}")
            
    # Si la boucle se termine sans succès
    clear_state("crack", target_hash)
    print("\n[-] Échec : Le mot de passe a résisté à toutes nos listes.")