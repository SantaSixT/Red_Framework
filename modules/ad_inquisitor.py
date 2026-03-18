from ldap3 import Server, Connection, ALL, ANONYMOUS
from core.reporter import add_finding

def run_ldap(args):
    target = args.target
    print(f"[*] Inquisition LDAP sur {target}...")
    
    try:
        # On définit le serveur et la connexion anonyme
        server = Server(target, get_info=ALL, connect_timeout=5)
        conn = Connection(server, user="", password="", authentication=ANONYMOUS, auto_bind=True)
        
        print(f"[\033[92m+\033[0m] BINGO ! Connexion LDAP Anonyme réussie sur {target}")
        
        # Extraction des infos de base (Naming Contexts)
        naming_contexts = server.info.naming_contexts
        finding_detail = f"LDAP Anonymous Bind ouvert. Contextes trouvés : {', '.join(naming_contexts)}"
        
        print(f"[*] Contextes de nommage : {naming_contexts}")
        add_finding("LDAP Inquisitor", target, finding_detail)
        
        conn.unbind()
        
    except Exception as e:
        print(f"[-] LDAP sécurisé ou inaccessible : {str(e)}")
        
