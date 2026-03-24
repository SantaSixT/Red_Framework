import aiohttp
import asyncio

# Quelques mots-clés typiques de WAF trouvés dans les headers (Cloudflare, Akamai, etc.)
WAF_SIGNATURES = ["cloudflare", "sucuri", "incapsula", "akamai", "imperva", "f5"]

async def detect_waf(target_url):
    """
    Envoie un payload malveillant pour tester la présence d'un WAF.
    Retourne (True, "Raison") si un WAF est détecté, sinon (False, "").
    """
    print(f"[*] Analyse des défenses sur {target_url}...")
    
    # Payload hyper agressif qui déclenche 99% des WAF (SQLi + XSS)
    poison = "?id=1'+OR+1=1--&test=<script>alert(1)</script>"
    
    # Gestion propre de l'URL
    url_poisoned = target_url + poison if target_url.endswith('/') else target_url + '/' + poison

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Red_Framework/1.0"
    }

    # 1. On crée l'objet Timeout requis par aiohttp
    timeout = aiohttp.ClientTimeout(total=5)

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            # 2. On passe l'objet timeout au lieu d'un simple entier
            async with session.get(target_url, timeout=timeout) as resp_clean:
                status_clean = resp_clean.status
                headers_clean = str(resp_clean.headers).lower()

            # Vérification des headers pour des WAFs très connus
            for sig in WAF_SIGNATURES:
                if sig in headers_clean:
                    return True, f"Signature '{sig}' détectée dans les headers HTTP."

            # 3. Pareil ici, on utilise l'objet timeout
            async with session.get(url_poisoned, timeout=timeout) as resp_poison:
                status_poison = resp_poison.status

            # Analyse de la différence
            if status_clean in [200, 301, 302] and status_poison in [403, 406, 501, 429]:
                return True, f"Blocage comportemental (Code {status_poison} reçu sur payload malveillant)."

    except Exception as e:
        return False, f"Erreur de connexion lors du test : {e}"

    return False, "Aucune défense apparente détectée."