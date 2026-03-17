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
    

def show_notes():
    """Lit et affiche le rapport Markdown de manière stylisée dans le terminal."""
    if not os.path.exists(REPORT_FILE):
        print(f"[\033[91m!\033[0m] Aucun rapport trouvé ({REPORT_FILE}).")
        return

    print(f"\n\033[95m\033[1m" + "="*50)
    print(f"   📜 CONSULTATION DES NOTES D'AUDIT")
    print("="*50 + "\033[0m\n")

    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            # Stylisation des titres de modules
            if line.startswith("###"):
                print(f"\n\033[96m\033[1m{line.replace('### ', '▶ ')}\033[0m")
            # Stylisation des points clés (Heure, Découverte)
            elif line.startswith("-"):
                # On met en vert ce qui est entre étoiles (le gras en MD)
                formatted_line = line.replace("**", "\033[92m").replace("**", "\033[0m")
                print(f"  {formatted_line}")
            # En-tête du rapport
            elif line.startswith("# "):
                print(f"\033[91m\033[1m{line}\033[0m")
            else:
                print(f"  {line}")
    
    print(f"\n\033[95m" + "="*50 + "\033[0m\n")