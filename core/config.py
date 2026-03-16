import os

def load_secure_config():
    """
    Blue Team Practice : Charge les secrets depuis le fichier .env
    sans jamais les coder en dur dans l'application.
    """
    # 1. On trouve le chemin absolu vers le fichier .env
    # __file__ est core/config.py, donc on remonte d'un dossier
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, '.env')

    # 2. Si le fichier .env existe, on le lit
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # On ignore les lignes vides et les commentaires
                if line and not line.startswith('#'):
                    # On sépare la clé de la valeur au premier "="
                    if '=' in line:
                        key, value = line.split('=', 1)
                        # On injecte dans l'environnement du script
                        os.environ[key.strip()] = value.strip()
    
    # 3. (Optionnel) Retourner un dictionnaire des clés critiques pour vérification
    # Parfait pour alerter l'utilisateur s'il manque une clé API avant de lancer une attaque
    return {
        "shodan_key": os.environ.get("SHODAN_API_KEY"),
        "github_token": os.environ.get("GITHUB_TOKEN")
    }