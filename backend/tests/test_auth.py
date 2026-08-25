import jwt

from app import config


def test_login_admin_returns_admin_role(client):
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["role"] == "ADMIN"
    payload = jwt.decode(body["access_token"], config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
    assert payload["role"] == "ADMIN"
    assert payload["sub"] == "1"


def test_login_learner_returns_learner_role(client):
    resp = client.post("/api/auth/login", json={"username": "learner", "password": "learner123"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["role"] == "LEARNER"


def test_login_wrong_password(client):
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "nope"})
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_login_missing_fields(client):
    resp = client.post("/api/auth/login", json={"username": "", "password": ""})
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "MISSING_FIELDS"


def test_passwords_are_hashed(db_session):
    from app.models import User

    user = db_session.query(User).filter(User.username == "admin").first()
    assert user.password_hash != "admin123"
    assert user.password_hash.startswith("pbkdf2_sha256$")
