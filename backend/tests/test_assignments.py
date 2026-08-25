from tests.helpers import auth


def test_list_assignments_admin(client, admin_token):
    resp = client.get("/api/assignments", headers=auth(admin_token))
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_assignments_learner_forbidden(client, learner_token):
    resp = client.get("/api/assignments", headers=auth(learner_token))
    assert resp.status_code == 403


def test_create_assignment(client, admin_token):
    resp = client.post(
        "/api/assignments", headers=auth(admin_token), json={"learner_id": 1, "course_id": 2}
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["progress"] == 0
    assert body["status"] == "NOT_STARTED"


def test_create_assignment_duplicate(client, admin_token):
    client.post("/api/assignments", headers=auth(admin_token), json={"learner_id": 1, "course_id": 2})
    resp = client.post(
        "/api/assignments", headers=auth(admin_token), json={"learner_id": 1, "course_id": 2}
    )
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "ASSIGNMENT_EXISTS"


def test_create_assignment_unknown_learner(client, admin_token):
    resp = client.post(
        "/api/assignments", headers=auth(admin_token), json={"learner_id": 999, "course_id": 2}
    )
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "LEARNER_NOT_FOUND"


def test_create_assignment_unknown_course(client, admin_token):
    resp = client.post(
        "/api/assignments", headers=auth(admin_token), json={"learner_id": 1, "course_id": 999}
    )
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "COURSE_NOT_FOUND"


def test_create_assignment_learner_forbidden(client, learner_token):
    resp = client.post(
        "/api/assignments", headers=auth(learner_token), json={"learner_id": 1, "course_id": 2}
    )
    assert resp.status_code == 403


def _assign(client, admin_token, learner_id=1, course_id=2):
    return client.post(
        "/api/assignments",
        headers=auth(admin_token),
        json={"learner_id": learner_id, "course_id": course_id},
    ).json()


def test_update_progress_own(client, admin_token, learner_token):
    assignment = _assign(client, admin_token, learner_id=1, course_id=2)
    resp = client.put(
        f"/api/assignments/{assignment['id']}/progress",
        headers=auth(learner_token),
        json={"progress": 75},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["progress"] == 75
    assert body["status"] == "IN_PROGRESS"


def test_update_progress_completed(client, admin_token, learner_token):
    assignment = _assign(client, admin_token, learner_id=1, course_id=2)
    resp = client.put(
        f"/api/assignments/{assignment['id']}/progress",
        headers=auth(learner_token),
        json={"progress": 100},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "COMPLETED"


def test_update_progress_out_of_range(client, admin_token, learner_token):
    assignment = _assign(client, admin_token, learner_id=1, course_id=2)
    resp = client.put(
        f"/api/assignments/{assignment['id']}/progress",
        headers=auth(learner_token),
        json={"progress": 120},
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_PROGRESS"


def test_update_progress_inconsistent_status(client, admin_token, learner_token):
    assignment = _assign(client, admin_token, learner_id=1, course_id=2)
    resp = client.put(
        f"/api/assignments/{assignment['id']}/progress",
        headers=auth(learner_token),
        json={"progress": 50, "status": "COMPLETED"},
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_PROGRESS"


def test_update_progress_other_learners_assignment(client, admin_token, learner_token):
    other = _assign(client, admin_token, learner_id=2, course_id=2)
    resp = client.put(
        f"/api/assignments/{other['id']}/progress",
        headers=auth(learner_token),
        json={"progress": 50},
    )
    assert resp.status_code == 403


def test_update_progress_admin_forbidden(client, admin_token):
    assignment = _assign(client, admin_token, learner_id=1, course_id=2)
    resp = client.put(
        f"/api/assignments/{assignment['id']}/progress",
        headers=auth(admin_token),
        json={"progress": 50},
    )
    assert resp.status_code == 403


def test_update_progress_not_found(client, learner_token):
    resp = client.put(
        "/api/assignments/999/progress", headers=auth(learner_token), json={"progress": 50}
    )
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "ASSIGNMENT_NOT_FOUND"
