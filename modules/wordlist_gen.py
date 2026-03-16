import os

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
    print(f"[*] Démarrage de la forge de mots de passe...")
    
    # Nettoyage des entrées utilisateurs (Secure Coding)
    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
    
    if not keywords:
        print("[-] Erreur : Aucun mot-clé valide fourni.")
        return

    output_file = "custom_wordlist.txt"
    all_passwords = set()

    # Application des mutations pour chaque mot-clé
    for kw in keywords:
        all_passwords.update(generate_mutations(kw))

    # Sauvegarde sécurisée sur le disque
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for pwd in sorted(all_passwords):
                f.write(f"{pwd}\n")
        
        print(f"[+] Succès : {len(all_passwords)} mots de passe générés.")
        print(f"[+] Fichier sauvegardé sous : {output_file}")
    except IOError as e:
        print(f"[-] Erreur lors de l'écriture du fichier : {e}")