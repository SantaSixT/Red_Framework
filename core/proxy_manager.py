from aiohttp_socks import ProxyConnector

def get_connector(proxy_url=None):
    """
    Retourne un connecteur aiohttp. 
    Si proxy_url est fourni (ex: socks5://127.0.0.1:9050), tout passe par là.
    """
    if proxy_url:
        print(f"[\033[94m*\033[0m] Mode Furtif : Routage via {proxy_url}")
        return ProxyConnector.from_url(proxy_url, ssl=False)
    
    # Sinon, connecteur standard
    return None