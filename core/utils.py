import os

def resolve_wordlist(wordlist_name):
    """
    Cherche intelligemment le dictionnaire.
    Priorité 1 : Dossier courant (listes générées sur mesure).
    Priorité 2 : Dossier 'wordlists/' (listes téléchargées par SecLists).
    """
    # 1. Vérifie si le fichier existe tel quel (chemin absolu ou dossier courant)
    if os.path.exists(wordlist_name):
        return wordlist_name
        
    # 2. Vérifie dans le dossier de téléchargement par défaut
    default_path = os.path.join("wordlists", wordlist_name)
    if os.path.exists(default_path):
        return default_path
        
    print(f"[-] Erreur : Le dictionnaire '{wordlist_name}' est introuvable.")
    return None