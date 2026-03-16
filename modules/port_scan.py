import asyncio
import socket

# ==========================================
# IMPORT DE LA BASE DE CONNAISSANCE (Data)
# ==========================================
from core.ports_db import TOP_PORTS

async def scan_port(ip, port, semaphore, timeout=1.5):
    """
    Tente de réaliser un TCP Full Connect sur un port spécifique
    et identifie le service probable via la base de données centrale.
    """
    async with semaphore:
        try:
            # asyncio.open_connection gère la création du socket TCP en arrière-plan
            fut = asyncio.open_connection(ip, port)
            
            # DevSecOps : On impose un timeout strict (1.5s par défaut). 
            # Si le pare-feu cible "Drop" (ignore) le paquet, on n'attend pas indéfiniment.
            reader, writer = await asyncio.wait_for(fut, timeout=timeout)
            
            # Résolution du nom du service via notre glossaire externe
            service_name = TOP_PORTS.get(port, "Service Inconnu")
            
            # Affichage enrichi pour l'auditeur
            print(f"[+] Port {port:<5}/TCP | État: OUVERT | Service: {service_name}")
            
            # DevSecOps (Blue Team Practice) : On referme la porte proprement.
            # Cela envoie un paquet FIN (Finish) pour libérer les ressources du serveur cible.
            writer.close()
            await writer.wait_closed()
            
            return port
            
        except asyncio.TimeoutError:
            pass # Le port est probablement filtré par un pare-feu (Drop)
        except ConnectionRefusedError:
            pass # Le port est fermé, le serveur a répondu activement (RST)
        except OSError:
            pass # Erreur système (ex: route réseau introuvable)
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