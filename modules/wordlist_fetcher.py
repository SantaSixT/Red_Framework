import os
import aiohttp
import asyncio

# Le répertoire où tout sera stocké dans ton framework
DEST_DIR = "wordlists"

# L'arsenal complet à télécharger d'un coup
WORDLISTS_DB = {
    # Mots de passe
    "pass_top10k.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt",
    "pass_fasttrack.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/fasttrack.txt",
    
    # Sous-domaines (pour ton module 'sub')
    "subs_top5000.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
    "subs_110k.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-110000.txt",
    
    # Enumération Web (Dossiers et fichiers)
    "web_common.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt",
    "web_raft_small.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/raft-small-words.txt",
    
    # Fuzzing & Payloads (Bonus pour plus tard)
    "fuzz_lfi.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/LFI/LFI-gracefulsecurity-linux.txt",
    "fuzz_xss.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/XSS/XSS-Bypass-Strings-BruteLogic.txt"
}

async def download_file(session, url, dest_path, name):
    try:
        async with session.get(url, timeout=15) as response:
            if response.status == 200:
                content = await response.read()
                with open(dest_path, "wb") as f:
                    f.write(content)
                size_kb = len(content) // 1024
                print(f"[\033[92m+\033[0m] Téléchargé : {name:<20} ({size_kb} KB)")
            else:
                print(f"[-] Erreur {response.status} pour {name}")
    except Exception as e:
        print(f"[-] Échec du téléchargement de {name} : {e}")

async def fetch_all_wordlists():
    print("[*] Initialisation de l'arsenal de dictionnaires...")
    
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        print(f"[*] Création du répertoire local : ./{DEST_DIR}/")

    tasks = []
    
    async with aiohttp.ClientSession() as session:
        for name, url in WORDLISTS_DB.items():
            dest_path = os.path.join(DEST_DIR, name)
            
            # On ignore si le fichier est déjà là
            if os.path.exists(dest_path):
                print(f"[\033[94m*\033[0m] Déjà présent : {name}")
                continue
            
            tasks.append(download_file(session, url, dest_path, name))
        
        if tasks:
            print(f"[*] Téléchargement de {len(tasks)} fichiers en cours (Asynchrone)...")
            await asyncio.gather(*tasks)
            print("\n[\033[92m+\033[0m] Base de données de dictionnaires mise à jour avec succès !")
        else:
            print("\n[\033[92m+\033[0m] Vos dictionnaires sont déjà tous à jour. Prêt pour l'audit.")

def run_update(args):
    """Wrapper pour arsenal.py"""
    asyncio.run(fetch_all_wordlists())