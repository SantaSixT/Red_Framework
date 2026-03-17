import aiohttp
import asyncio
from aiohttp import ClientTimeout # <--- Import nécessaire pour le typage
from core.reporter import add_finding

# Base de signatures pour le Giga-Outil
CMS_SIGNATURES = {
    "WordPress": {
        "paths": ["/wp-login.php", "/wp-content/", "/wp-includes/"],
        "strings": ["wp-embed.min.js", "WordPress"]
    },
    "Joomla": {
        "paths": ["/administrator/", "/components/com_contact/"],
        "strings": ["Joomla! - Open Source Content Management"]
    },
    "Drupal": {
        "paths": ["/sites/default/", "/core/modules/"],
        "strings": ["Drupal 8", "Drupal 9", "Drupal 10"]
    },
    "Magento": {
        "paths": ["/static/frontend/", "/errors/design.xml"],
        "strings": ["Mage.Cookies"]
    },
    "PrestaShop": {
        "paths": ["/img/cms/", "/themes/prestashop/"],
        "strings": ["PrestaShop"]
    }
}

async def detect_cms(target_url):
    """Analyse la cible pour identifier le CMS utilisé."""
    print(f"[*] Analyse intelligente du CMS pour : {target_url}")
    found_cms = []
    
    # On définit les timeouts proprement pour aiohttp
    timeout_long = ClientTimeout(total=5)
    timeout_short = ClientTimeout(total=3)

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        # 1. On récupère la page d'accueil
        try:
            async with session.get(target_url, timeout=timeout_long) as resp:
                html = await resp.text()
                for cms, data in CMS_SIGNATURES.items():
                    if any(s in html for s in data["strings"]):
                        found_cms.append(cms)
        except Exception:
            pass

        # 2. Recherche par chemins si rien n'est trouvé dans le code source
        if not found_cms:
            for cms, data in CMS_SIGNATURES.items():
                for path in data["paths"]:
                    check_url = f"{target_url.rstrip('/')}{path}"
                    try:
                        async with session.get(check_url, timeout=timeout_short) as resp:
                            if resp.status == 200:
                                found_cms.append(cms)
                                break 
                    except Exception:
                        continue

    # 3. Rapport et affichage
    if found_cms:
        unique_cms = list(set(found_cms))
        cms_str = ", ".join(unique_cms)
        print(f"[\033[92m+\033[0m] CMS Détecté : \033[1m{cms_str}\033[0m")
        add_finding("CMS Detector", target_url, f"Technologie identifiée : **{cms_str}**")
    else:
        print("[-] Aucun CMS connu détecté.")

def run_cms(args):
    """Wrapper pour arsenal.py"""
    asyncio.run(detect_cms(args.url))