from tests.helpers import auth


def test_list_courses_admin(client, admin_token):
    resp = client.get("/api/courses", headers=auth(admin_token))
    assert resp.status_code == 200
    assert len(resp.json()) == 3


def test_list_courses_learner(client, learner_token):
    resp = client.get("/api/courses", headers=auth(learner_token))
    assert resp.status_code == 200
    assert len(resp.json()) == 3


def test_get_course(client, admin_token):
    resp = client.get("/api/courses/1", headers=auth(admin_token))
    assert resp.status_code == 200
    assert resp.json()["id"] == 1


def test_get_course_not_found(client, admin_token):
    resp = client.get("/api/courses/999", headers=auth(admin_token))
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "COURSE_NOT_FOUND"


def test_create_course(client, admin_token):
    resp = client.post(
        "/api/courses",
        headers=auth(admin_token),
        json={"title": "Web Development Basics", "description": "HTML/CSS/JS", "duration_hours": 12},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "ACTIVE"
    assert body["duration_hours"] == 12


def test_create_course_empty_title(client, admin_token):
    resp = client.post(
        "/api/courses",
        headers=auth(admin_token),
        json={"title": "  ", "description": "x", "duration_hours": 5},
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_COURSE"


def test_create_course_bad_duration(client, admin_token):
    resp = client.post(
        "/api/courses",
        headers=auth(admin_token),
        json={"title": "T", "description": "x", "duration_hours": 0},
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_COURSE"


def test_create_course_learner_forbidden(client, learner_token):
    resp = client.post(
        "/api/courses",
        headers=auth(learner_token),
        json={"title": "T", "description": "x", "duration_hours": 5},
    )
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "INSUFFICIENT_SCOPE"


def test_update_course_status(client, admin_token):
    resp = client.put("/api/courses/1", headers=auth(admin_token), json={"status": "INACTIVE"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "INACTIVE"


def test_update_course_bad_duration(client, admin_token):
    resp = client.put("/api/courses/1", headers=auth(admin_token), json={"duration_hours": -1})
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_COURSE"


def test_update_course_not_found(client, admin_token):
    resp = client.put("/api/courses/999", headers=auth(admin_token), json={"title": "X"})
    assert resp.status_code == 404


def test_delete_course(client, admin_token):
    resp = client.delete("/api/courses/3", headers=auth(admin_token))
    assert resp.status_code == 204
    resp = client.get("/api/courses/3", headers=auth(admin_token))
    assert resp.status_code == 404


def test_delete_course_not_found(client, admin_token):
    resp = client.delete("/api/courses/999", headers=auth(admin_token))
    assert resp.status_code == 404
