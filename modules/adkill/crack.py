import subprocess
import shutil
from pathlib import Path
from datetime import datetime


class Cracker:
    """Wrapper hashcat avec fallback john. Conçu pour Parrot OS.
    Détecte automatiquement les binaires dans le PATH."""

    HASHCAT_MODES = {
        "asrep": "18200",
        "tgs": "13100",
    }
    JOHN_FORMATS = {
        "asrep": "krb5asrep",
        "tgs": "krb5tgs",
    }

    def __init__(self, wordlist="/usr/share/wordlists/rockyou.txt", workdir="crack_tmp"):
        self.wordlist = Path(wordlist)
        self.workdir = Path(workdir)
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.has_hashcat = shutil.which("hashcat") is not None
        self.has_john = shutil.which("john") is not None

    def crack(self, user, hash_str, htype):
        """Tente hashcat puis john. Retourne le mot de passe ou None."""
        if not self.wordlist.exists():
            print(f"[!] Wordlist introuvable: {self.wordlist}")
            return None

        # Écriture du hash (newline unix explicite)
        hash_file = self.workdir / f"{user}_{htype}.hash"
        with open(hash_file, "w", newline="\n") as fh:
            fh.write(hash_str.strip() + "\n")

        # 1. hashcat
        if self.has_hashcat:
            pwd = self._try_hashcat(hash_file, htype)
            if pwd:
                return pwd

        # 2. fallback john
        if self.has_john:
            pwd = self._try_john(hash_file, htype)
            if pwd:
                return pwd

        if not self.has_hashcat and not self.has_john:
            print("[!] Ni hashcat ni john trouvés dans le PATH.")
        return None

    def _try_hashcat(self, hash_file, htype):
        mode = self.HASHCAT_MODES.get(htype)
        if not mode:
            return None
        potfile = self.workdir / f"{htype}.potfile"
        cmd = [
            "hashcat", "-m", mode, "-a", "0",
            str(hash_file), str(self.wordlist),
            "--potfile-path", str(potfile),
            "--quiet",
        ]
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            # Récupération du résultat via --show
            show = subprocess.run(
                ["hashcat", "-m", mode, str(hash_file),
                 "--potfile-path", str(potfile), "--show"],
                capture_output=True, text=True, timeout=60,
            )
            if show.stdout.strip():
                # format: hash:password
                line = show.stdout.strip().split("\n")[0]
                return line.split(":")[-1]
        except subprocess.TimeoutExpired:
            print(f"[!] hashcat timeout sur {hash_file.name}")
        except Exception as e:
            print(f"[!] hashcat erreur: {e}")
        return None

    def _try_john(self, hash_file, htype):
        fmt = self.JOHN_FORMATS.get(htype)
        cmd = ["john", f"--format={fmt}",
               f"--wordlist={self.wordlist}", str(hash_file)]
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            show = subprocess.run(
                ["john", "--show", f"--format={fmt}", str(hash_file)],
                capture_output=True, text=True, timeout=60,
            )
            for line in show.stdout.strip().split("\n"):
                if ":" in line and not line.startswith("0 password"):
                    return line.split(":")[1]
        except subprocess.TimeoutExpired:
            print(f"[!] john timeout sur {hash_file.name}")
        except Exception as e:
            print(f"[!] john erreur: {e}")
        return None
