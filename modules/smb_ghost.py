import socket
from smb.SMBConnection import SMBConnection
from core.reporter import add_finding

def check_null_session(target_ip):
    """
    Tente de se connecter au serveur SMB (Port 445) avec une session nulle
    (anonyme) et d'énumérer les partages réseau disponibles.
    """
    print(f"[*] Frappe à la porte SMB de {target_ip} (Port 445)...")
    
    # Configuration d'une connexion anonyme (Nom d'utilisateur vide, mot de passe vide)
    # L'ID client 'ArsenalGhost' est arbitraire (c'est le nom de notre machine simulée)
    conn = SMBConnection("", "", "ArsenalGhost", target_ip, use_ntlm_v2=True, is_direct_tcp=True)
    
    try:
        # Tentative de connexion (timeout court pour ne pas bloquer)
        connected = conn.connect(target_ip, 445, timeout=5)
        
        if connected:
            print(f"[\033[92m+\033[0m] BINGO ! Session Nulle acceptée par {target_ip} !")
            
            # Si on est connecté, on demande la liste des dossiers partagés
            shares = conn.listShares()
            share_names = []
            
            print("[*] Partages réseau découverts :")
            for share in shares:
                # On ignore les partages cachés par défaut (qui finissent par $) sauf IPC$ qui est utile
                name = share.name
                if not name.endswith('$') or name == 'IPC$':
                    print(f"    - \\\\{target_ip}\\{name}")
                    share_names.append(name)
            
            # --- SAUVEGARDE V2 ---
            if share_names:
                shares_str = ", ".join(share_names)
                add_finding("Fantôme SMB", target_ip, f"Session Nulle Vulnérable ! Partages trouvés : **{shares_str}**")
            else:
                add_finding("Fantôme SMB", target_ip, "Session Nulle Vulnérable, mais aucun partage lisible.")
                
            conn.close()
            return True
        else:
            print("[-] Échec : Le serveur refuse les sessions anonymes (Sécurisé).")
            return False
            
    except (socket.error, socket.timeout):
        print(f"[-] Erreur : Impossible de joindre le port 445 sur {target_ip}. Le serveur est-il allumé ?")
    except Exception as e:
        print(f"[-] Erreur inattendue SMB : {str(e)}")
    
    return False

def run_smb(args):
    """Wrapper appelé par arsenal.py"""
    try:
        # Résolution DNS (si l'utilisateur a tapé un nom de domaine au lieu d'une IP)
        target_ip = socket.gethostbyname(args.target)
        check_null_session(target_ip)
    except socket.gaierror:
        print(f"[-] Erreur : Impossible de résoudre la cible '{args.target}'")
    except KeyboardInterrupt:
        print("\n[-] Opération annulée par l'auditeur.")