import requests
from core.reporter import add_finding

def check_s3_bucket(bucket_name):
    """Vérifie si un bucket S3 existe et s'il est public."""
    # URL standard d'un bucket AWS S3
    url = f"https://{bucket_name}.s3.amazonaws.com"
    
    try:
        response = requests.get(url, timeout=5)
        
        # 404 = Le bucket n'existe pas
        if response.status_code == 404:
            return
        
        # 200 = BINGO ! Le bucket est public et on peut lister les fichiers
        if response.status_code == 200:
            print(f"[\033[91m!\033[0m] ALERTE : Bucket S3 PUBLIC trouvé : {url}")
            add_finding("S3 Scanner", bucket_name, f"Bucket S3 ouvert et listable : **{url}**")
            
        # 403 = Le bucket existe mais l'accès est refusé (Sécurisé)
        elif response.status_code == 403:
            print(f"[\033[94m*\033[0m] Bucket trouvé (Privé) : {bucket_name}")
            
    except Exception:
        pass

def run_s3(args):
    company = args.name.lower()
    print(f"[*] Chasse au Cloud pour la cible : {company}")
    
    # Liste de suffixes courants pour les buckets d'entreprise
    suffixes = [
        "", "-dev", "-prod", "-backup", "-staging", "-data", "-test", 
        "-public", "-private", "-sql", "-files", "-logs", "-archive"
    ]
    
    for suffix in suffixes:
        bucket_name = f"{company}{suffix}"
        check_s3_bucket(bucket_name)

    print("[*] Fin du scan S3.")