import aiohttp
import asyncio
from core.reporter import add_finding

SECRETS_PATHS = [
    ".git/config", ".env", "web.config", "settings.py", 
    "config.php.bak", ".aws/credentials", ".ssh/id_rsa"
]

async def check_secret(session, base_url, path):
    url = f"{base_url.rstrip('/')}/{path}"
    try:
        async with session.get(url, timeout=5, allow_redirects=False) as resp:
            if resp.status == 200:
                print(f"[\033[91m!\033[0m] SECRET TROUVÉ : {url}")
                add_finding("Secret Sniper", base_url, f"Fichier sensible exposé : **{path}**")
    except:
        pass

async def async_secrets(target):
    async with aiohttp.ClientSession() as session:
        tasks = [check_secret(session, target, path) for path in SECRETS_PATHS]
        await asyncio.gather(*tasks)

def run_secrets(args):
    print(f"[*] Sniper de secrets en joue sur {args.url}...")
    asyncio.run(async_secrets(args.url))