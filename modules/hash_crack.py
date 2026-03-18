import hashlib
import os
from core.reporter import add_finding
from core.utils import resolve_wordlist

def run_crack(args):
    target_hash = args.hash.lower()
    algo = getattr(args, 'algo', 'md5').lower()
    
    print(f"[*] Démarrage du cracking hors-ligne")
    print(f"[*] Cible : {target_hash} (Algo: {algo.upper()})")
    
    # --- MODE CASCADE (AUTO-PILOT) ---
    wordlists_to_try = []
    
    if args.wordlist == "auto":
        print("[\033[94m*\033[0m] Mode Auto-Pilot activé : Lancement de la cascade de dictionnaires.")
        # Priorité 1 : Le dictionnaire généré sur mesure (rapide et ciblé)
        if os.path.exists("custom_wordlist.txt"):
            wordlists_to_try.append("custom_wordlist.txt")
        
        # Priorité 2 : Le dictionnaire général (SecLists)
        wordlists_to_try.append("pass_top10k.txt")
        # Tu pourras ajouter "pass_fasttrack.txt" ici quand tu l'auras téléchargé !
    else:
        # Si l'utilisateur a spécifié une liste précise, on n'utilise que celle-là
        wordlists_to_try.append(args.wordlist)

    # --- LECTURE ET CASSAGE ---
    for wl_name in wordlists_to_try:
        real_path = resolve_wordlist(wl_name)
        if not real_path:
            continue # Si un dico manque, on passe au suivant sans crasher
            
        print(f"[*] Analyse en cours avec l'arsenal : \033[1m{wl_name}\033[0m ...")
        
        try:
            with open(real_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
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
                        return # On arrête tout dès qu'on a trouvé
                        
        except Exception as e:
            print(f"[-] Erreur de lecture sur {wl_name} : {e}")
            
    # Si la boucle se termine sans avoir fait de "return"
    print("\n[-] Échec : Le mot de passe a résisté à toutes nos listes.")