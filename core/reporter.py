import os
from datetime import datetime

REPORT_DIR = "reports"
REPORT_FILE = "arsenal_report.md"

def init_report():
    """Crée l'en-tête du fichier Markdown s'il n'existe pas encore."""
    if not os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("# 🛡️ Arsenal Red Team - Rapport d'Audit Automatique\n\n")
            f.write(f"**Date de début de mission :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

def add_finding(module_name, target, details):
    """Ajoute une découverte au rapport Markdown."""
    
    # 1. Création automatique du dossier s'il n'existe pas
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        
    # 2. Écriture dans le fichier (le reste du code ne change pas)
    try:
        with open(REPORT_FILE, "a", encoding="utf-8") as f:
            f.write(f"### 🎯 [{module_name}] - {target}\n")
            f.write(f"- **Date :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"- **Détails :** {details}\n")
            f.write("---\n")
    except Exception as e:
        print(f"[-] Erreur de reporting : {e}")

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