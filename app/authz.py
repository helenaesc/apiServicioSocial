import os
from flask import Request, session

ROLE_ADMIN = "ADMIN"
ROLE_STAFF = "STAFF"


def _parse_keys(env_value: str) -> set[str]:
    if not env_value:
        return set()
    return {k.strip() for k in env_value.split(",") if k.strip()}


def _is_legacy_header_auth_enabled() -> bool:
    value = (os.getenv("ENABLE_LEGACY_HEADER_AUTH", "true") or "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def get_role(req: Request):
    """
    Prioridad:
    1) sesión real de admin/staff
    2) compatibilidad temporal con X-ADMIN-KEY (si está habilitado)
    """

    # 1. Sesión real
    session_role = session.get("admin_user_role")
    if session_role in {ROLE_ADMIN, ROLE_STAFF}:
        return session_role

    # 2. Compatibilidad temporal con header legacy
    if not _is_legacy_header_auth_enabled():
        return None

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