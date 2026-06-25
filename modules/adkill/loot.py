from pathlib import Path
from datetime import datetime


class LootStore:
    """Stockage central des données récoltées pendant l'attaque AD.
    Système d'observers : chaque ajout peut déclencher une réaction
    automatique (ex: hash ajouté -> crack auto)."""

    def __init__(self, domain, dc_ip):
        self.domain = domain
        self.dc_ip = dc_ip
        self.users = set()
        self.valid_creds = []   # [(user, secret, type)]
        self.hashes = []        # [(user, hash, htype)]
        self.spns = []          # [(user, spn)]
        self._observers = []

    # --- Ajouts avec notification ---
    def add_user(self, user):
        if user and user not in self.users:
            self.users.add(user)

    def add_hash(self, user, h, htype):
        """htype: 'asrep' ou 'tgs'"""
        self.hashes.append((user, h, htype))
        self._notify("hash", (user, h, htype))

    def add_cred(self, user, secret, stype):
        if (user, secret, stype) not in self.valid_creds:
            self.valid_creds.append((user, secret, stype))
            self._notify("cred", (user, secret, stype))
            print(f"[+] NOUVEAU CRED: {user}:{secret} ({stype})")

    def add_spn(self, user, spn):
        if (user, spn) not in self.spns:
            self.spns.append((user, spn))

    # --- Observers ---
    def on(self, callback):
        self._observers.append(callback)

    def _notify(self, event_type, data):
        for cb in self._observers:
            try:
                cb(event_type, data)
            except Exception as e:
                print(f"[!] Observer error: {e}")

    # --- Export ---
    def summary(self):
        return {
            "users": len(self.users),
            "creds": len(self.valid_creds),
            "hashes": len(self.hashes),
            "spns": len(self.spns),
        }

    def dump(self, outdir="loot_output"):
        """Sauvegarde le butin sur disque (cross-platform)."""
        out = Path(outdir)
        out.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        if self.valid_creds:
            f = out / f"creds_{ts}.txt"
            with open(f, "w", newline="\n") as fh:
                for user, secret, stype in self.valid_creds:
                    fh.write(f"{user}:{secret}:{stype}\n")
            print(f"[*] Creds sauvegardés -> {f}")

        if self.users:
            f = out / f"users_{ts}.txt"
            with open(f, "w", newline="\n") as fh:
                for u in sorted(self.users):
                    fh.write(f"{u}\n")
            print(f"[*] Users sauvegardés -> {f}")

        return out
