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
from modules.hash_crack import run_crack
from modules.web_spider import run_spider
from modules.smb_ghost import run_smb
from modules.s3_scanner import run_s3
from modules.ad_inquisitor import run_ldap
from modules.secret_sniper import run_secrets
from modules.vuln_headers import run_headers
from modules.brute_generic import run_brute_custom
from core.reporter import show_notes
from modules.cms_detect import run_cms
from modules.sub_enum import run_sub_enum
from modules.report_export import generate_html
from modules.wordlist_fetcher import run_update

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
    p_c2 = subparsers.add_parser("c2", help="Serveur de Command & Control avancé (Multi-Sessions, Upload/Download)")
    p_c2.add_argument("-p", "--port", type=int, default=4444, help="Port d'écoute (défaut: 4444)")
    p_c2.set_defaults(func=run_c2)

    
# --- Module: Payload Generator ---
    parser_payload = subparsers.add_parser("payload", help="Génère un payload obfusqué pour l'évasion d'AV/EDR")
    group = parser_payload.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--cmd", type=str, help="Commande système en clair (ex: 'whoami')")
    group.add_argument("--revshell", type=str, help="Génère un agent pointant vers IP:PORT (ex: 127.0.0.1:4444)")
    parser_payload.set_defaults(func=run_payload)

# --- Module: Hash Cracker (Offline) ---
    parser_crack = subparsers.add_parser("crack", help="Casseur de hash hors-ligne (MD5, SHA1, SHA256)")
    parser_crack.add_argument("--hash", required=True, help="Le hash à casser (ex: 5f4dcc...)")
    parser_crack.add_argument("--algo", choices=['md5', 'sha1', 'sha256'], default='md5', help="Algorithme (défaut: md5)")
    parser_crack.add_argument("-w", "--wordlist", required=True, help="Chemin vers le dictionnaire")
    parser_crack.set_defaults(func=run_crack)

# 1. On crée le sous-parser pour le spider (Vérifie bien le nom ici !)
    parser_spider = subparsers.add_parser("spider", help="Cartographie récursive d'un site web")
    
    # 2. On lui ajoute ses arguments (C'est ici que tu avais l'erreur)
    parser_spider.add_argument("-u", "--url", required=True, help="URL de départ")
    parser_spider.add_argument("-d", "--depth", type=int, default=2, help="Profondeur")
    parser_spider.add_argument("-t", "--threads", type=int, default=10, help="Threads")
    
    # --- AJOUT DE L'OPTION PROXY ---
    parser_spider.add_argument("--proxy", help="Proxy (ex: socks5://127.0.0.1:9050)")
    
    parser_spider.set_defaults(func=run_spider)

# --- Module: Fantôme SMB (Null Session) ---
    parser_smb = subparsers.add_parser("smb", help="Traque les partages Windows (Null Session) sur le port 445")
    parser_smb.add_argument("-T", "--target", required=True, help="IP ou nom d'hôte du serveur Windows cible")
    parser_smb.set_defaults(func=run_smb)

# --- Module: S3 Scanner ---
    parser_s3 = subparsers.add_parser("s3", help="Recherche de Buckets AWS S3 mal configurés")
    parser_s3.add_argument("-n", "--name", required=True, help="Nom de l'entreprise (ex: tesla)")
    parser_s3.set_defaults(func=run_s3)

# --- Module: LDAP ---
    p_ldap = subparsers.add_parser("ldap", help="Vérifie l'Anonymous Bind LDAP (Port 389)")
    p_ldap.add_argument("-T", "--target", required=True)
    p_ldap.set_defaults(func=run_ldap)

    # --- Module: Secrets ---
    p_sec = subparsers.add_parser("secrets", help="Cherche des fichiers sensibles (.git, .env...)")
    p_sec.add_argument("-u", "--url", required=True)
    p_sec.set_defaults(func=run_secrets)

    # --- Module: Headers ---
    p_head = subparsers.add_parser("headers", help="Analyse les en-têtes de sécurité HTTP")
    p_head.add_argument("-u", "--url", required=True)
    p_head.set_defaults(func=run_headers)

# --- Module: Brute Force Maison ---
    p_brute = subparsers.add_parser("brute-web", help="Moteur de brute force HTTP POST sur-mesure")
    p_brute.add_argument("-u", "--url", required=True, help="URL du formulaire (ex: http://site.com/login)")
    p_brute.add_argument("-U", "--user", required=True, help="Nom d'utilisateur à cibler")
    p_brute.add_argument("-w", "--wordlist", required=True, help="Chemin du dictionnaire")
    p_brute.add_argument("--user-field", default="username", help="Nom du champ utilisateur (HTML name)")
    p_brute.add_argument("--pass-field", default="password", help="Nom du champ mot de passe (HTML name)")
    p_brute.add_argument("--fail", default="Invalid", help="Message d'erreur en cas d'échec (ex: 'Mauvais mot de passe')")
    p_brute.add_argument("-t", "--threads", type=int, default=10, help="Nombre de tentatives simultanées")
    p_brute.set_defaults(func=run_brute_custom)

# --- Module: Viewer de Notes ---
    p_notes = subparsers.add_parser("notes", help="Affiche le rapport d'audit actuel dans le terminal")
    p_notes.set_defaults(func=lambda args: show_notes())

# --- Module: CMS Detector ---
    p_cms = subparsers.add_parser("cms", help="Identifie le CMS utilisé (WordPress, Joomla, etc.)")
    p_cms.add_argument("-u", "--url", required=True, help="URL cible")
    p_cms.set_defaults(func=run_cms)

# --- Module: Subdomain Scanner ---
    p_sub = subparsers.add_parser("sub", help="Énumération DNS de sous-domaines")
    p_sub.add_argument("-d", "--domain", required=True, help="Domaine racine")
    p_sub.add_argument("-w", "--wordlist", required=True, help="Dictionnaire")
    p_sub.add_argument("-t", "--threads", type=int, default=50, help="Threads DNS")
    
    # AJOUT DU FLAG AUTO-SCAN
    p_sub.add_argument("--auto-scan", action="store_true", help="Lance un scan de ports sur chaque sous-domaine trouvé")
    
    p_sub.set_defaults(func=run_sub_enum)

# --- Module: Gestionnaire de Ressources ---
    p_update = subparsers.add_parser("update", help="Télécharge et met à jour toutes les wordlists dans le framework")
    p_update.set_defaults(func=run_update)

# --- Module: Export HTML/PDF ---
    p_export = subparsers.add_parser("export", help="Génère un rapport HTML interactif à partir de vos notes")
    p_export.set_defaults(func=generate_html)



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