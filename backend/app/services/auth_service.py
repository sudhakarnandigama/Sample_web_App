from sqlalchemy.orm import Session

from ..auth import create_access_token, verify_password
from ..errors import ApiError
from ..models import User


def authenticate(db: Session, username: str, password: str) -> dict:
    username = (username or "").strip()
    password = password or ""

    if not username or not password:
        raise ApiError("MISSING_FIELDS", "username and password are required", 400)

    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(password, user.password_hash):
        raise ApiError("INVALID_CREDENTIALS", "invalid username or password", 401)

    token = create_access_token(user.id, user.role)
    return {"access_token": token, "token_type": "bearer", "role": user.role}
