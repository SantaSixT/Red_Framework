import base64
import urllib.parse
import binascii
import html

def run_decoder(args):
    text = args.text
    mode = args.mode       # encode ou decode
    fmt = args.format      # b64, url, hex, html
    
    try:
        if mode == 'encode':
            if fmt == 'b64':
                res = base64.b64encode(text.encode()).decode()
            elif fmt == 'url':
                res = urllib.parse.quote_plus(text)
            elif fmt == 'hex':
                res = binascii.hexlify(text.encode()).decode()
            elif fmt == 'html':
                res = html.escape(text)
                
        elif mode == 'decode':
            if fmt == 'b64':
                res = base64.b64decode(text.encode()).decode()
            elif fmt == 'url':
                res = urllib.parse.unquote_plus(text)
            elif fmt == 'hex':
                res = binascii.unhexlify(text.encode()).decode()
            elif fmt == 'html':
                res = html.unescape(text)
                
        print(f"\n[\033[92m+\033[0m] Résultat ({mode} en {fmt}) :\n\033[1m{res}\033[0m\n")
        
    except Exception as e:
        print(f"\n[\033[91m!\033[0m] Erreur lors de l'opération : {e}")
        print("    -> Vérifiez que la chaîne à décoder est au bon format.\n")