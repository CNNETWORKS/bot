import json
import os
from threading import RLock
from config import DATA_DIR, USERS_FILE, REDEEMS_FILE

_lock = RLock()

def ensure_data_folder():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, {})
    if not os.path.exists(REDEEMS_FILE):
        save_json(REDEEMS_FILE, {})

def load_json(file_path: str):
    with _lock:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

def save_json(file_path: str, data):
    with _lock:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def clamp_int(n, low, high):
    return max(low, min(high, n))
