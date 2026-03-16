import requests
import json

def run_subdomains(args):
    domain = args.domain.strip()
    print(f"[*] Démarrage de la reconnaissance OSINT (crt.sh) pour : {domain}")
    
    # URL de l'API avec le joker % pour chercher les sous-domaines
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    
    try:
        # On se fait passer pour un navigateur standard
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=45)
        
        if response.status_code != 200:
            print(f"[-] Erreur de l'API crt.sh (Code: {response.status_code}). Réessayez plus tard.")
            return
            
        data = response.json()
        subdomains = set() # Un 'set' en Python élimine automatiquement les doublons
        
        # Parsing du JSON renvoyé par crt.sh
        for entry in data:
            name_value = entry.get('name_value', '')
            # Certains certificats contiennent plusieurs domaines séparés par des retours à la ligne
            for sub in name_value.split('\n'):
                # On nettoie les certificats "Wildcard" (ex: *.domaine.com)
                clean_sub = sub.strip().replace('*.', '')
                if clean_sub.endswith(domain):
                    subdomains.add(clean_sub)
                    
        print(f"[+] Succès : {len(subdomains)} sous-domaines uniques découverts.\n")
        
        # Affichage trié par ordre alphabétique
        for sub in sorted(subdomains):
            print(f"    -> {sub}")
            
    except requests.exceptions.RequestException as e:
        print(f"[-] Erreur de connexion au service OSINT : {e}")
    except json.JSONDecodeError:
        print("[-] Erreur : L'API n'a pas renvoyé de données valides. (Surcharge possible de crt.sh)")