import asyncio
import socket
import aiohttp
import urllib.parse
from core.ports_db import TOP_PORTS
from core.reporter import add_finding

async def check_cve(banner_text, session):
    """
    Module V2 : Recherche la bannière sur l'API publique NVD (NIST).
    """
    clean_text = banner_text.replace('-', ' ').replace('_', ' ').replace('/', ' ')
    words = clean_text.split()
    
    if len(words) < 2:
        return ""
        
    search_term = f"{words[0]} {words[1]}"
    encoded_term = urllib.parse.quote(search_term)
    
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={encoded_term}&resultsPerPage=3"
    
    try:
        async with session.get(url, timeout=4) as resp:
            if resp.status == 200:
                data = await resp.json()
                vulns = data.get("vulnerabilities", [])
                
                if not vulns:
                    return " | 🛡️ CVE: Aucune faille publique majeure trouvée"
                
                cve_list = [v["cve"]["id"] for v in vulns]
                return f" | ☠️  CVEs: {', '.join(cve_list)}"
            else:
                return " | ⚠️ API NVD: Limite de requêtes atteinte"
    except Exception:
        return ""

async def scan_port(ip, port, semaphore, timeout, session):
    """Tente un Full Connect, capture la bannière, et cherche les CVEs."""
    async with semaphore:
        try:
            fut = asyncio.open_connection(ip, port)
            reader, writer = await asyncio.wait_for(fut, timeout=timeout)
            
            service_name = TOP_PORTS.get(port, "Service Inconnu")
            banner_info = ""
            
            # --- BANNER GRABBING ---
            try:
                if port in [80, 443, 8000, 8080, 8443]:
                    writer.write(b"HEAD / HTTP/1.0\r\n\r\n")
                    await writer.drain()
                    
                data = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                
                if data:
                    clean_banner = data.decode('utf-8', errors='ignore').split('\n')[0].strip()
                    if clean_banner:
                        banner_info = f" | Info: {clean_banner[:30]}..."
                        # --- V2 : RECHERCHE CVE AUTOMATIQUE ---
                        cve_info = await check_cve(clean_banner, session)
                        banner_info += cve_info
                        
            except Exception:
                pass
            
            # Affichage console
            print(f"[+] Port {port:<5}/TCP | État: OUVERT | Service: {service_name}{banner_info}")
            
            # ==========================================
            # INTÉGRATION V2 : SAUVEGARDE AU RAPPORT
            # ==========================================
            add_finding("Scanner TCP", ip, f"Port **{port}/TCP** ouvert ({service_name}){banner_info}")
            
            writer.close()
            await writer.wait_closed()
            return port
            
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            pass 
        except Exception:
            pass
            
        return None

async def async_scan(target, start_port, end_port, concurrency):
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[-] Erreur : Impossible de résoudre la cible '{target}'")
        return

    print(f"[*] Démarrage du scan V2 (Avec Résolution CVE) sur {ip} (Ports {start_port} à {end_port})")
    print(f"[*] Concurrence: {concurrency} threads.")
    print(f"[*] Attention : Requêtes envoyées à l'API NVD (NIST). Limite publique : 5 req/30sec.")
    
    semaphore = asyncio.Semaphore(concurrency)
    tasks = []
    
    async with aiohttp.ClientSession() as session:
        for port in range(start_port, end_port + 1):
            tasks.append(scan_port(ip, port, semaphore, 1.5, session))
            
        results = await asyncio.gather(*tasks)
    
    open_ports = [p for p in results if p is not None]
    print(f"\n[*] Scan terminé. {len(open_ports)} port(s) ouvert(s) trouvé(s).")

def run_scan(args):
    """Wrapper appelé par arsenal.py"""
    if args.start < 1 or args.end > 65535 or args.start > args.end:
        print("[-] Erreur : La plage de ports doit être comprise entre 1 et 65535.")
        return
    try:
        asyncio.run(async_scan(args.target, args.start, args.end, args.threads))
    except KeyboardInterrupt:
        print("\n[-] Scan réseau annulé par l'auditeur.")