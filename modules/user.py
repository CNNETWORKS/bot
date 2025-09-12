from config import USERS_FILE
from .utils import load_json, save_json

# In-memory caches (kept simple)
_users = load_json(USERS_FILE)

DEFAULT_USER = {
    "credits": 5,
    "free_used": False,
    "banned": False,
    "is_admin": False,
    "referred_by": None,
    "referrals": []        
}

def get_user(uid: int | str) -> dict:
    key = str(uid)
    if key not in _users:
        _users[key] = DEFAULT_USER.copy()
        save_json(USERS_FILE, _users)
    return _users[key]

def save_user(uid: int | str):
    save_json(USERS_FILE, _users)


def add_credits(uid: int | str, amount: int):
    user = get_user(uid)
    user["credits"] = user.get("credits", 0) + int(amount)
    save_user(uid)

def set_ban(uid: int | str, banned: bool):
    user = get_user(uid)
    user["banned"] = bool(banned)
    save_user(uid)

def is_banned(uid: int | str) -> bool:
    return get_user(uid).get("banned", False)

def all_users() -> dict:
    return _users

def totals():
    total_users = len(_users)
    banned_users = sum(1 for u in _users.values() if u.get("banned"))
    return total_users, banned_users, total_users - banned_users
