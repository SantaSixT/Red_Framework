import os
from datetime import datetime

REPORT_FILE = "arsenal_report.md"

def init_report():
    """Crée l'en-tête du fichier Markdown s'il n'existe pas encore."""
    if not os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("# 🛡️ Arsenal Red Team - Rapport d'Audit Automatique\n\n")
            f.write(f"**Date de début de mission :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

def add_finding(module_name, target, finding_details):
    """Ajoute une découverte formatée en Markdown au rapport global."""
    init_report()
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write(f"### 🎯 Module : `{module_name}` | Cible : `{target}`\n")
        f.write(f"- **Heure :** {timestamp}\n")
        f.write(f"- **Découverte :** {finding_details}\n\n")
        
    # Petit retour visuel discret pour l'opérateur
    print(f"[\033[92m+\033[0m] Résultat sauvegardé dans {REPORT_FILE}")