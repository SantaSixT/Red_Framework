import argparse
import sys
import os
from core.config import load_secure_config
from modules.wordlist_gen import run_wordlist
from modules.enum_web import run_enum
from modules.osint_subdomains import run_subdomains
from modules.brute_http import run_brute

def main():
    load_secure_config() 
    
    parser = argparse.ArgumentParser(
        description="Arsenal Red Team - Framework de Pentest Custom",
        epilog="DevSecOps Lab - Usage autorisé uniquement"
    )
    
    subparsers = parser.add_subparsers(title="Modules disponibles", dest="module", required=True)

    # --- Module: Enum (inchangé) ---
    parser_enum = subparsers.add_parser("enum", help="Énumération web des répertoires et fichiers")
    parser_enum.add_argument("-u", "--url", required=True)
    parser_enum.add_argument("-w", "--wordlist", required=True)
    parser_enum.add_argument("-t", "--threads", type=int, default=20)
    parser_enum.add_argument("-e", "--extensions", type=str, default="", help="Extensions à ajouter (ex: .bak,.php)") # NOUVEAU
    parser_enum.set_defaults(func=run_enum)
    
    # --- Module: Brute-Force (NOUVEAU) ---
    parser_brute = subparsers.add_parser("brute", help="Brute-Force de formulaire HTTP POST")
    parser_brute.add_argument("-u", "--url", required=True, help="URL du formulaire de login")
    parser_brute.add_argument("-user", "--username", required=True, help="Nom d'utilisateur à cibler")
    parser_wordlist_brute = parser_brute.add_argument("-w", "--wordlist", required=True, help="Dictionnaire de mots de passe")
    parser_brute.add_argument("-t", "--threads", type=int, default=10)
    parser_brute.set_defaults(func=run_brute)

    # --- Module: Wordlist (inchangé) ---
    parser_wordlist = subparsers.add_parser("wordlist", help="Génération de dictionnaire ciblé")
    parser_wordlist.add_argument("-k", "--keywords", required=True, help="Mots-clés séparés par des virgules")
    parser_wordlist.set_defaults(func=run_wordlist)

    # --- Module: Subdomain (NOUVEAU) ---
    parser_subdomain = subparsers.add_parser("subdomain", help="Reconnaissance OSINT de sous-domaines via crt.sh")
    parser_subdomain.add_argument("-d", "--domain", required=True, help="Domaine cible (ex: defcon.org)")
    parser_subdomain.set_defaults(func=run_subdomains)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Arrêt global du framework.")
        sys.exit(0)