from tests.helpers import auth


def test_dashboard_admin(client, admin_token):
    resp = client.get("/api/dashboard", headers=auth(admin_token))
    assert resp.status_code == 200
    body = resp.json()
    assert set(body.keys()) == {
        "total_learners",
        "total_courses",
        "active_courses",
        "completed_courses",
        "certificates",
    }
    assert body["total_learners"] == 5
    assert body["total_courses"] == 3
    assert body["active_courses"] == 3
    assert body["completed_courses"] == 0
    assert body["certificates"] == 0


def test_dashboard_learner(client, learner_token):
    resp = client.get("/api/dashboard", headers=auth(learner_token))
    assert resp.status_code == 200
    body = resp.json()
    assert set(body.keys()) == {
        "assigned_courses",
        "in_progress",
        "completed",
        "certificates",
    }
    assert body["assigned_courses"] == 0
    assert body["in_progress"] == 0
    assert body["completed"] == 0
    assert body["certificates"] == 0


def test_dashboard_missing_token(client):
    resp = client.get("/api/dashboard")
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "MISSING_AUTH"
