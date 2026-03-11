import os
from flask import Request

ROLE_ADMIN = "ADMIN"
ROLE_STAFF = "STAFF"

def _parse_keys(env_value: str) -> set[str]:
    if not env_value:
        return set()
    return {k.strip() for k in env_value.split(",") if k.strip()}

def get_role(req: Request):
    """
    Lee X-ADMIN-KEY y devuelve:
      - ROLE_ADMIN ("ADMIN")
      - ROLE_STAFF ("STAFF")
      - None
    """
    key = (req.headers.get("X-ADMIN-KEY") or "").strip()
    if not key:
        return None

    admin_keys = _parse_keys(os.getenv("ADMIN_KEYS", ""))
    staff_keys = _parse_keys(os.getenv("STAFF_KEYS", ""))

    if key in admin_keys:
        return ROLE_ADMIN
    if key in staff_keys:
        return ROLE_STAFF
    return None

def require_role(req: Request, allowed_roles: set[str]):
    role = get_role(req)
    if role in allowed_roles:
        return role
    return None