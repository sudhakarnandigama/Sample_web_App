"""Password hashing, JWT signing/verification, and the scope-based auth dependency.

Passwords are stored as ``pbkdf2_sha256$<salt_hex>$<hash_hex>`` using the
stdlib ``hashlib.pbkdf2_hmac`` with 100k iterations (see
docs/sources/decisions/2026-08-24-auth-transport.md).
"""

import hashlib
import hmac
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, Header
from sqlalchemy.orm import Session

from . import config
from .database import get_db
from .errors import ApiError
from .models import Learner, User

PBKDF2_ITERATIONS = 100_000

# Role -> scope mapping, canonical in docs/wiki/auth/02-scopes.md.
ROLE_SCOPES = {
    "ADMIN": {
        "dashboard:read",
        "courses:read",
        "courses:write",
        "learners:read",
        "learners:write",
        "assignments:write",
        "assessments:read",
        "certificates:read",
        "certificates:write",
        "reports:read",
    },
    "LEARNER": {
        "dashboard:read",
        "courses:read",
        "progress:write:own",
        "assessments:read",
        "assessments:submit",
        "certificates:read",
        "certificates:write",
    },
}


def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), PBKDF2_ITERATIONS
    ).hex()
    return f"pbkdf2_sha256${salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, salt, digest = stored.split("$")
        if scheme != "pbkdf2_sha256":
            return False
    except ValueError:
        return False
    computed = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), PBKDF2_ITERATIONS
    ).hex()
    return hmac.compare_digest(computed, digest)


def create_access_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=config.JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])


@dataclass
class CurrentUser:
    user_id: int
    role: str
    learner_id: Optional[int] = None


def require_scope(scope: str):
    """Return a FastAPI dependency enforcing ``Authorization: Bearer <jwt>`` and ``scope``."""

    def dependency(
        authorization: Optional[str] = Header(default=None),
        db: Session = Depends(get_db),
    ) -> CurrentUser:
        if not authorization:
            raise ApiError("MISSING_AUTH", "missing Authorization header", 401)
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise ApiError("MISSING_AUTH", "missing bearer token", 401)

        try:
            payload = decode_token(token)
        except jwt.PyJWTError:
            raise ApiError("INVALID_TOKEN", "invalid or expired token", 401)

        try:
            user_id = int(payload.get("sub"))
        except (TypeError, ValueError):
            raise ApiError("INVALID_TOKEN", "invalid or expired token", 401)

        role = payload.get("role")
        if role not in ROLE_SCOPES:
            raise ApiError("INVALID_TOKEN", "invalid or expired token", 401)

        if scope not in ROLE_SCOPES[role]:
            raise ApiError("INSUFFICIENT_SCOPE", "insufficient scope for this operation", 403)

        user = db.get(User, user_id)
        if user is None:
            raise ApiError("INVALID_TOKEN", "invalid or expired token", 401)

        learner_id = None
        if role == "LEARNER":
            learner = db.query(Learner).filter(Learner.user_id == user_id).first()
            learner_id = learner.id if learner else None

        return CurrentUser(user_id=user_id, role=role, learner_id=learner_id)

    return dependency
