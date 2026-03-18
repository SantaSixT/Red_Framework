import os

# Chemin vers notre liste téléchargée par défaut
DEFAULT_PASS_LIST = "wordlists/pass_top10k.txt"

def generate_mutations(keyword):
    """
    Génère des mutations prédictibles basées sur le comportement humain.
    """
    results = set()
    
    # 1. Mutations de base (Casse)
    bases = [keyword.lower(), keyword.capitalize(), keyword.upper()]
    results.update(bases)

    # 2. Leetspeak (Substitution de caractères)
    for base in bases:
        leet = base.replace('a', '@').replace('A', '@') \
                   .replace('e', '3').replace('E', '3') \
                   .replace('i', '1').replace('I', '1') \
                   .replace('o', '0').replace('O', '0')
        results.add(leet)

    # 3. Suffixes prédictibles (Années en cours, caractères spéciaux)
    suffixes = ['123', '2024', '2025', '!', '?', '2024!', '2025!','2026','2026!']
    
    final_results = set(results)
    for word in results:
        for suffix in suffixes:
            final_results.add(f"{word}{suffix}")

    return final_results

def run_wordlist(args):
    """
    Point d'entrée du module, appelé par arsenal.py
    """
    print(f"[*] Démarrage de la forge de mots de passe hybride...")
    
    # Nettoyage des entrées utilisateurs (Secure Coding)
    # Supporte une liste de mots séparés par des virgules
    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
    
    if not keywords:
        print("[-] Erreur : Aucun mot-clé valide fourni.")
        return

    # On utilise l'argument de sortie, sinon custom_wordlist.txt par défaut
    output_file = getattr(args, 'output', "custom_wordlist.txt")
    all_passwords = set()

    # Application des mutations pour chaque mot-clé
    for kw in keywords:
        all_passwords.update(generate_mutations(kw))
        
    print(f"[\033[94m*\033[0m] {len(all_passwords)} mutations générées intelligemment pour {len(keywords)} mot(s)-clé(s).")

    # ==========================================
    # FUSION : Ajout des mots de passe par défaut
    # ==========================================
    if os.path.exists(DEFAULT_PASS_LIST):
        try:
            with open(DEFAULT_PASS_LIST, 'r', encoding='utf-8', errors='ignore') as f:
                default_passes = [line.strip() for line in f if line.strip()]
            
            # L'utilisation d'un 'set' (all_passwords) empêche automatiquement les doublons !
            all_passwords.update(default_passes)
            print(f"[\033[94m*\033[0m] {len(default_passes)} mots de passe par défaut ajoutés depuis la base SecLists.")
        except Exception as e:
            print(f"[-] Erreur lors de la lecture de {DEFAULT_PASS_LIST}: {e}")
    else:
        print(f"[-] Base {DEFAULT_PASS_LIST} introuvable. Tapez 'python arsenal.py update' pour la télécharger.")

    # Sauvegarde sécurisée sur le disque
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for pwd in sorted(all_passwords):
                f.write(f"{pwd}\n")
        
        print(f"[\033[92m+\033[0m] Succès : {len(all_passwords)} mots de passe au total.")
        print(f"[\033[92m+\033[0m] Fichier sauvegardé sous : \033[1m{output_file}\033[0m")
    except IOError as e:
        print(f"[-] Erreur lors de l'écriture du fichier : {e}")