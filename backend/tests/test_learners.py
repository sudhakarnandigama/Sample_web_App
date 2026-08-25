from tests.helpers import auth


def test_list_learners_admin(client, admin_token):
    resp = client.get("/api/learners", headers=auth(admin_token))
    assert resp.status_code == 200
    assert len(resp.json()) == 5


def test_list_learners_learner_forbidden(client, learner_token):
    resp = client.get("/api/learners", headers=auth(learner_token))
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "INSUFFICIENT_SCOPE"


def test_get_learner(client, admin_token):
    resp = client.get("/api/learners/1", headers=auth(admin_token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == 1
    assert body["user_id"] == 2


def test_get_learner_not_found(client, admin_token):
    resp = client.get("/api/learners/999", headers=auth(admin_token))
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "LEARNER_NOT_FOUND"


def test_create_learner(client, admin_token):
    resp = client.post(
        "/api/learners",
        headers=auth(admin_token),
        json={"name": "Anjali Rao", "email": "new@example.com", "department": "HR"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "ACTIVE"
    assert body["user_id"] is None


def test_create_learner_duplicate_email(client, admin_token):
    resp = client.post(
        "/api/learners",
        headers=auth(admin_token),
        json={"name": "Dup", "email": "john@example.com", "department": "IT"},
    )
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "EMAIL_EXISTS"


def test_create_learner_empty_name(client, admin_token):
    resp = client.post(
        "/api/learners",
        headers=auth(admin_token),
        json={"name": "  ", "email": "x@example.com", "department": "IT"},
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_LEARNER"


def test_create_learner_malformed_email(client, admin_token):
    resp = client.post(
        "/api/learners",
        headers=auth(admin_token),
        json={"name": "X", "email": "not-an-email", "department": "IT"},
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_LEARNER"


def test_update_learner_status(client, admin_token):
    resp = client.put("/api/learners/2", headers=auth(admin_token), json={"status": "INACTIVE"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "INACTIVE"


def test_update_learner_email_conflict(client, admin_token):
    resp = client.put(
        "/api/learners/2", headers=auth(admin_token), json={"email": "john@example.com"}
    )
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "EMAIL_EXISTS"


def test_update_learner_not_found(client, admin_token):
    resp = client.put("/api/learners/999", headers=auth(admin_token), json={"name": "X"})
    assert resp.status_code == 404


def test_delete_learner(client, admin_token):
    resp = client.delete("/api/learners/5", headers=auth(admin_token))
    assert resp.status_code == 204
    resp = client.get("/api/learners/5", headers=auth(admin_token))
    assert resp.status_code == 404


def test_delete_learner_cascades(client, admin_token, db_session):
    from app.models import AssessmentAttempt, Assignment, Certificate

    # Seed dependent rows for learner 2 directly.
    db_session.add(Assignment(course_id=1, learner_id=2, progress=50, status="IN_PROGRESS"))
    db_session.add(
        AssessmentAttempt(assessment_id=1, learner_id=2, score=100, result="PASS")
    )
    db_session.add(
        Certificate(
            learner_id=2,
            course_id=2,
            certificate_number="CERT-2026-999",
            status="CERTIFIED",
        )
    )
    db_session.commit()

    resp = client.delete("/api/learners/2", headers=auth(admin_token))
    assert resp.status_code == 204
    assert db_session.query(Assignment).filter(Assignment.learner_id == 2).count() == 0
    assert db_session.query(AssessmentAttempt).filter(AssessmentAttempt.learner_id == 2).count() == 0
    assert db_session.query(Certificate).filter(Certificate.learner_id == 2).count() == 0
