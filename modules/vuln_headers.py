import requests
from core.reporter import add_finding

def run_headers(args):
    url = args.url
    print(f"[*] Analyse des en-têtes de sécurité pour {url}...")
    
    try:
        resp = requests.get(url, timeout=5)
        headers = resp.headers
        findings = []

        # Check CORS
        cors = headers.get('Access-Control-Allow-Origin', '')
        if cors == '*':
            findings.append("CORS trop permissif (Wildcard '*')")
            
        # Check Security Headers manquants
        if 'Content-Security-Policy' not in headers:
            findings.append("Absence de Content-Security-Policy (CSP)")
            
        if 'X-Frame-Options' not in headers:
            findings.append("Absence de X-Frame-Options (Vulnérable au Clickjacking)")

        if findings:
            for f in findings: print(f"[\033[93m!\033[0m] Faiblesse : {f}")
            add_finding("Header Analyzer", url, f"Problèmes détectés : {', '.join(findings)}")
        else:
            print("[+] En-têtes de base correctement configurés.")

    except Exception as e:
        print(f"[-] Erreur : {e}")