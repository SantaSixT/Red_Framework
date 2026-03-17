import asyncio
import socket

# ==========================================
# IMPORT DE LA BASE DE CONNAISSANCE (Data)
# ==========================================
from core.ports_db import TOP_PORTS

async def scan_port(ip, port, semaphore, timeout=1.5):
    """
    Tente un TCP Full Connect, identifie le service probable,
    et tente une capture de bannière (Banner Grabbing) pour la version.
    """
    async with semaphore:
        try:
            fut = asyncio.open_connection(ip, port)
            reader, writer = await asyncio.wait_for(fut, timeout=timeout)
            
            service_name = TOP_PORTS.get(port, "Service Inconnu")
            banner_info = "" # Par défaut, la bannière est vide
            
            # ==========================================
            # DÉBUT DU BANNER GRABBING (Red Team Active)
            # ==========================================
            try:
                # Si c'est un port web, le serveur attend qu'on lui parle en premier.
                # On envoie une requête HTTP très basique (HEAD demande juste les infos, pas la page)
                if port in [80, 443, 8000, 8080, 8443]:
                    writer.write(b"HEAD / HTTP/1.0\r\n\r\n")
                    await writer.drain()
                    
                # On écoute la réponse du serveur avec un timeout très court (1 seconde)
                # pour ne pas ralentir le scan global.
                data = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                
                if data:
                    # On nettoie la réponse brute : on décode, on prend la 1ère ligne, on vire les espaces
                    clean_banner = data.decode('utf-8', errors='ignore').split('\n')[0].strip()
                    # On garde seulement 60 caractères pour garder le terminal propre
                    if clean_banner:
                        banner_info = f" | Info: {clean_banner[:60]}"
                        
            except Exception:
                # Si le timeout expire ou que le serveur ne dit rien, on ignore en silence
                pass
            # ==========================================
            
            print(f"[+] Port {port:<5}/TCP | État: OUVERT | Service: {service_name}{banner_info}")
            
            writer.close()
            await writer.wait_closed()
            return port
            
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            pass 
        except Exception:
            pass
            
        return None

async def async_scan(target, start_port, end_port, concurrency):
    # Validation et résolution DNS (ex: transforme "example.com" en adresse IP)
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[-] Erreur : Impossible de résoudre la cible '{target}'")
        return

    print(f"[*] Démarrage du scan TCP sur {ip} (Ports {start_port} à {end_port})")
    print(f"[*] Concurrence: {concurrency} threads.")
    
    semaphore = asyncio.Semaphore(concurrency)
    tasks = []
    
    # Création des tâches pour chaque port de la plage demandée
    for port in range(start_port, end_port + 1):
        tasks.append(scan_port(ip, port, semaphore))
        
    # Exécution massive
    results = await asyncio.gather(*tasks)
    
    # Nettoyage des résultats (on retire les 'None')
    open_ports = [p for p in results if p is not None]
    print(f"\n[*] Scan terminé. {len(open_ports)} port(s) ouvert(s) trouvé(s).")

def run_scan(args):
    """Wrapper appelé par le framework arsenal.py"""
    if args.start < 1 or args.end > 65535 or args.start > args.end:
        print("[-] Erreur : La plage de ports doit être comprise entre 1 et 65535.")
        return
        
    try:
        asyncio.run(async_scan(args.target, args.start, args.end, args.threads))
    except KeyboardInterrupt:
        print("\n[-] Scan réseau annulé par l'auditeur.")