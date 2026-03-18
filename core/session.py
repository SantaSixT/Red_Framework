import json
import os

SESSION_FILE = ".red_session"

def _load_all():
    """Charge toutes les sessions actives."""
    if not os.path.exists(SESSION_FILE):
        return {}
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def _save_all(data):
    """Sauvegarde les données de session sur le disque."""
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def save_state(module_name, target_id, current_index, current_wordlist):
    """Enregistre la progression d'une attaque."""
    data = _load_all()
    session_key = f"{module_name}_{target_id}"
    data[session_key] = {
        "index": current_index,
        "wordlist": current_wordlist
    }
    _save_all(data)

def get_state(module_name, target_id):
    """Récupère une session existante si elle existe."""
    data = _load_all()
    session_key = f"{module_name}_{target_id}"
    return data.get(session_key)

def clear_state(module_name, target_id):
    """Efface la session une fois l'attaque terminée avec succès."""
    data = _load_all()
    session_key = f"{module_name}_{target_id}"
    if session_key in data:
        del data[session_key]
        _save_all(data)