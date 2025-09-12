import json
import os

PROTECTED_FILE = "data/protected_numbers.json"

# Ensure file exists
if not os.path.exists(PROTECTED_FILE):
    with open(PROTECTED_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def _load_protected():
    try:
        with open(PROTECTED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_protected(numbers):
    with open(PROTECTED_FILE, "w", encoding="utf-8") as f:
        json.dump(numbers, f, indent=2)

def add_protected(number: str) -> bool:
    """Add a number to protected list"""
    numbers = _load_protected()
    if number not in numbers:
        numbers.append(number)
        _save_protected(numbers)
        return True
    return False

def remove_protected(number: str) -> bool:
    """Remove number from protected list"""
    numbers = _load_protected()
    if number in numbers:
        numbers.remove(number)
        _save_protected(numbers)
        return True
    return False

def is_protected(number: str) -> bool:
    """Check if number is protected"""
    return number in _load_protected()

def list_protected() -> list:
    """Return all protected numbers"""
    return _load_protected()
