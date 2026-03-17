import hashlib
from core.reporter import add_finding

def run_crack(args):
    target_hash = args.hash.lower()
    algo = args.algo.lower()
    wordlist_path = args.wordlist
    
    print(f"[*] Démarrage du cracking hors-ligne")
    print(f"[*] Cible : {target_hash} (Algo: {algo.upper()})")
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if not word:
                    continue
                
                # Calcul du hash du mot testé
                if algo == 'md5':
                    hashed_word = hashlib.md5(word.encode()).hexdigest()
                elif algo == 'sha1':
                    hashed_word = hashlib.sha1(word.encode()).hexdigest()
                elif algo == 'sha256':
                    hashed_word = hashlib.sha256(word.encode()).hexdigest()
                else:
                    print("[-] Algorithme non supporté.")
                    return
                
                # Vérification
                if hashed_word == target_hash:
                    print(f"\n[\033[92m+\033[0m] BINGO ! Hash cassé !")
                    print(f"[\033[92m+\033[0m] Mot de passe en clair : {word}")
                    
                    # SAUVEGARDE AUTOMATIQUE DANS LE RAPPORT MARKDOWN
                    add_finding("Hash Cracker", target_hash, f"Mot de passe cassé avec succès : **{word}**")
                    return
                    
        print("\n[-] Échec : Le mot de passe n'est pas dans ce dictionnaire.")
        
    except FileNotFoundError:
        print(f"[-] Erreur : Le dictionnaire '{wordlist_path}' est introuvable.")