# 🗺️ Feuille de Route (Roadmap) - Red_Framework

Voici les prochaines fonctionnalités et modules prévus pour les futures versions du framework. Les contributions sont les bienvenues !

## 🟢 À Court Terme (Prochaines semaines)
- [ ] **Module JWT Breaker :** Analyse, décodage et tentative de falsification de tokens JWT (attaque *Algorithm: None* et brute-force de signature).
- [ ] **Module SSRF Hunter :** Détection automatisée de Server-Side Request Forgery via des callbacks (OAST).
- [ ] **Intégration BloodHound :** Export des données du module `ldap` vers un format compatible BloodHound pour l'analyse des chemins d'attaque Active Directory.

## 🟡 À Moyen Terme
- [ ] **Gestionnaire de Sessions (Stateful) :** Sauvegarde de l'état des scans en base de données SQLite pour pouvoir mettre en pause et reprendre un audit plus tard.
- [ ] **Bypass WAF Avancé :** Ajout de techniques de fragmentation de requêtes et d'encodage polymorphe dans `core/waf.py`.
- [ ] **Module Kerberoast :** Extraction asynchrone des TGS pour le cassage hors-ligne.

## 🔴 À Long Terme
- [ ] **Interface Web / GUI :** Création d'un petit dashboard web local en Flask/FastAPI pour piloter l'arsenal à la souris (Optionnel, l'outil restera CLI-first).
- [ ] **Agents C2 Multi-OS :** Implants en Go ou Rust (Windows/Linux/macOS) se connectant automatiquement au module `c2`.