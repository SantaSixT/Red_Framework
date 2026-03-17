import argparse
import sys
import os

# Imports des modules du Framework
from core.config import load_secure_config
from modules.wordlist_gen import run_wordlist
from modules.enum_web import run_enum
from modules.osint_subdomains import run_subdomains
from modules.brute_http import run_brute
from modules.port_scan import run_scan
from modules.c2_server import run_c2
from modules.payload_gen import run_payload

# ==========================================
# GESTION DES COULEURS (UI)
# ==========================================
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Affiche la bannière ASCII du framework"""
    # LE CORRECTIF EST ICI : rf""" au lieu de f"""
    banner = rf"""{Colors.RED}{Colors.BOLD}
    ___                                __ 
   /   |  ______________  ____  ____ _/ / 
  / /| | / ___/ ___/ _ \/ __ \/ __ `/ /  
 / ___ |/ /  (__  )  __/ / / / /_/ / /   
/_/  |_/_/  /____/\___/_/ /_/\__,_/_/    
                                         
{Colors.CYAN}:: Framework d'Automatisation Red Team ::{Colors.RESET}
{Colors.YELLOW}>> Usage autorisé en laboratoire DevSecOps uniquement <<{Colors.RESET}
"""
    print(banner)


def main():
    load_secure_config() 
    
    # 1. Configuration du Parseur Principal
    parser = argparse.ArgumentParser(
        description="Arsenal Red Team - Framework de Pentest Custom",
        epilog="DevSecOps Lab - Usage autorisé uniquement"
    )
    
    # 2. Définition des Sous-Commandes
    subparsers = parser.add_subparsers(title="Modules disponibles", dest="module", required=True)

    # --- Module: Enum ---
    parser_enum = subparsers.add_parser("enum", help="Énumération web des répertoires et fichiers")
    parser_enum.add_argument("-u", "--url", required=True)
    parser_enum.add_argument("-w", "--wordlist", required=True)
    parser_enum.add_argument("-t", "--threads", type=int, default=20)
    parser_enum.add_argument("-e", "--extensions", type=str, default="", help="Extensions (ex: .bak,.php)")
    parser_enum.set_defaults(func=run_enum)
    
    # --- Module: Brute-Force ---
    parser_brute = subparsers.add_parser("brute", help="Brute-Force de formulaire HTTP POST")
    parser_brute.add_argument("-u", "--url", required=True, help="URL du formulaire de login")
    parser_brute.add_argument("-user", "--username", required=True, help="Nom d'utilisateur à cibler")
    parser_brute.add_argument("-w", "--wordlist", required=True, help="Dictionnaire de mots de passe")
    parser_brute.add_argument("-t", "--threads", type=int, default=10)
    parser_brute.set_defaults(func=run_brute)

    # --- Module: Wordlist ---
    parser_wordlist = subparsers.add_parser("wordlist", help="Génération de dictionnaire ciblé")
    parser_wordlist.add_argument("-k", "--keywords", required=True, help="Mots-clés (séparés par des virgules)")
    parser_wordlist.set_defaults(func=run_wordlist)

    # --- Module: Subdomain OSINT ---
    parser_subdomain = subparsers.add_parser("subdomain", help="Reconnaissance OSINT de sous-domaines via crt.sh")
    parser_subdomain.add_argument("-d", "--domain", required=True, help="Domaine cible (ex: defcon.org)")
    parser_subdomain.set_defaults(func=run_subdomains)

    # --- Module: Port Scanner ---
    parser_scan = subparsers.add_parser("scan", help="Scan furtif de ports TCP avec Banner Grabbing")
    parser_scan.add_argument("-T", "--target", required=True, help="IP ou Domaine cible")
    parser_scan.add_argument("-s", "--start", type=int, default=1, help="Port de début (défaut: 1)")
    parser_scan.add_argument("-e", "--end", type=int, default=1024, help="Port de fin (défaut: 1024)")
    parser_scan.add_argument("-t", "--threads", type=int, default=100, help="Nombre de sockets simultanés")
    parser_scan.set_defaults(func=run_scan)

    # --- Module: C2 Server ---
    parser_c2 = subparsers.add_parser("c2", help="Démarre le serveur d'écoute pour les Reverse Shells")
    parser_c2.add_argument("-l", "--listen", type=str, default="0.0.0.0", help="IP d'écoute")
    parser_c2.add_argument("-p", "--port", type=int, default=4444, help="Port d'écoute (défaut: 4444)")
    parser_c2.set_defaults(func=run_c2)

    # --- Module: Payload Generator ---
    parser_payload = subparsers.add_parser("payload", help="Génère un payload obfusqué pour l'évasion d'AV/EDR")
    group = parser_payload.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--cmd", type=str, help="Commande système en clair (ex: 'whoami')")
    group.add_argument("--revshell", type=str, help="Génère un agent pointant vers IP:PORT (ex: 127.0.0.1:4444)")
    parser_payload.set_defaults(func=run_payload)
    
    # 3. Exécution finale
    args = parser.parse_args()
    
    # Affichage de la bannière avant d'exécuter la fonction du module
    print_banner()
    args.func(args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Note: Cette erreur s'affichera maintenant en rouge grâce à la classe Colors !
        print(f"\n{Colors.RED}[-] Arrêt global du framework par l'auditeur.{Colors.RESET}")
        sys.exit(0)