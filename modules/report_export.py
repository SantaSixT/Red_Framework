import os
import markdown
from datetime import datetime

# On pointe vers le nouveau dossier
REPORT_DIR = "reports"
REPORT_MD = os.path.join(REPORT_DIR, "arsenal_report.md")
REPORT_HTML = os.path.join(REPORT_DIR, "arsenal_report.html")

# CSS "Dark Mode / Hacker" pour le rapport final
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'Audit - Red Framework</title>
    <style>
        body {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: #161b22;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            border: 1px solid #30363d;
        }
        h1 { color: #ff5e5e; border-bottom: 2px solid #ff5e5e; padding-bottom: 10px; }
        h2 { color: #58a6ff; margin-top: 30px; }
        h3 { color: #3fb950; }
        p { font-size: 15px; }
        strong { color: #ff7b72; }
        ul { background: #0d1117; padding: 15px 30px; border-radius: 5px; border-left: 3px solid #3fb950; }
        li { margin-bottom: 8px; }
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 12px;
            color: #8b949e;
            border-top: 1px solid #30363d;
            padding-top: 20px;
        }
        .btn-print {
            background-color: #238636;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
            font-weight: bold;
            float: right;
        }
        .btn-print:hover { background-color: #2ea043; }
    </style>
</head>
<body>
    <div class="container">
        <button class="btn-print" onclick="window.print()">🖨️ Exporter en PDF</button>
        {content}
        <div class="footer">
            Généré automatiquement par <strong>Red_Framework (Giga-Arsenal V4)</strong> le {date}
        </div>
    </div>
</body>
</html>
"""

def generate_html(args):
    print("[*] Génération du rapport HTML interactif en cours...")
    
    if not os.path.exists(REPORT_MD):
        print(f"[-] Erreur : Le fichier {REPORT_MD} n'existe pas encore.")
        return

    # Lire le contenu Markdown
    with open(REPORT_MD, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convertir en HTML
    html_content = markdown.markdown(md_text)

# Injecter dans le template avec replace() pour ne pas perturber le CSS
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_html = HTML_TEMPLATE.replace("{content}", html_content).replace("{date}", current_date)

    # Sauvegarder le fichier final
    with open(REPORT_HTML, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"[\033[92m+\033[0m] Succès ! Rapport généré : \033[1m{os.path.abspath(REPORT_HTML)}\033[0m")
    print("[*] Ouvrez ce fichier dans votre navigateur web pour le visualiser.")