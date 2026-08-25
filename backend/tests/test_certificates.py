from tests.helpers import auth


def test_generate_eligible_learner(client, admin_token, learner_token):
    client.post(
        "/api/assignments", headers=auth(admin_token), json={"learner_id": 1, "course_id": 2}
    )
    assignment = client.get("/api/assignments", headers=auth(admin_token)).json()[0]
    client.put(
        f"/api/assignments/{assignment['id']}/progress",
        headers=auth(learner_token),
        json={"progress": 100},
    )
    client.post("/api/assessments/1/submit", headers=auth(learner_token), json={"answers": {"1": "A"}})

    resp = client.post("/api/certificates", headers=auth(learner_token), json={"course_id": 2})
    assert resp.status_code == 201
    body = resp.json()
    assert body["certificate_number"] == "CERT-2026-001"
    assert body["status"] == "CERTIFIED"
    assert body["learner_id"] == 1


def test_generate_ignores_body_learner_id_for_learner(client, admin_token, learner_token):
    client.post(
        "/api/assignments", headers=auth(admin_token), json={"learner_id": 1, "course_id": 2}
    )
    assignment = client.get("/api/assignments", headers=auth(admin_token)).json()[0]
    client.put(
        f"/api/assignments/{assignment['id']}/progress",
        headers=auth(learner_token),
        json={"progress": 100},
    )
    client.post("/api/assessments/1/submit", headers=auth(learner_token), json={"answers": {"1": "A"}})

    resp = client.post(
        "/api/certificates", headers=auth(learner_token), json={"learner_id": 999, "course_id": 2}
    )
    assert resp.status_code == 201
    assert resp.json()["learner_id"] == 1


def test_generate_not_eligible_not_completed(client, admin_token):
    client.post(
        "/api/assignments", headers=auth(admin_token), json={"learner_id": 2, "course_id": 2}
    )
    resp = client.post(
        "/api/certificates", headers=auth(admin_token), json={"learner_id": 2, "course_id": 2}
    )
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "NOT_ELIGIBLE"


def test_generate_duplicate(client, admin_token, learner_token):
    client.post(
        "/api/assignments", headers=auth(admin_token), json={"learner_id": 1, "course_id": 2}
    )
    assignment = client.get("/api/assignments", headers=auth(admin_token)).json()[0]
    client.put(
        f"/api/assignments/{assignment['id']}/progress",
        headers=auth(learner_token),
        json={"progress": 100},
    )
    client.post("/api/assessments/1/submit", headers=auth(learner_token), json={"answers": {"1": "A"}})
    client.post("/api/certificates", headers=auth(learner_token), json={"course_id": 2})

    resp = client.post("/api/certificates", headers=auth(learner_token), json={"course_id": 2})
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "CERTIFICATE_EXISTS"


def test_list_certificates_learner_scoped(client, admin_token, learner_token):
    client.post(
        "/api/assignments", headers=auth(admin_token), json={"learner_id": 1, "course_id": 2}
    )
    assignment = client.get("/api/assignments", headers=auth(admin_token)).json()[0]
    client.put(
        f"/api/assignments/{assignment['id']}/progress",
        headers=auth(learner_token),
        json={"progress": 100},
    )
    client.post("/api/assessments/1/submit", headers=auth(learner_token), json={"answers": {"1": "A"}})
    client.post("/api/certificates", headers=auth(learner_token), json={"course_id": 2})

    admin_resp = client.get("/api/certificates", headers=auth(admin_token))
    assert admin_resp.status_code == 200
    assert len(admin_resp.json()) == 1

    learner_resp = client.get("/api/certificates", headers=auth(learner_token))
    assert learner_resp.status_code == 200
    assert len(learner_resp.json()) == 1
    assert learner_resp.json()[0]["learner_id"] == 1


def test_get_certificate_admin(client, admin_token, learner_token):
    client.post(
        "/api/assignments", headers=auth(admin_token), json={"learner_id": 1, "course_id": 2}
    )
    assignment = client.get("/api/assignments", headers=auth(admin_token)).json()[0]
    client.put(
        f"/api/assignments/{assignment['id']}/progress",
        headers=auth(learner_token),
        json={"progress": 100},
    )
    client.post("/api/assessments/1/submit", headers=auth(learner_token), json={"answers": {"1": "A"}})
    created = client.post("/api/certificates", headers=auth(learner_token), json={"course_id": 2}).json()

    resp = client.get(f"/api/certificates/{created['id']}", headers=auth(admin_token))
    assert resp.status_code == 200
    assert resp.json()["certificate_number"] == "CERT-2026-001"


def test_get_certificate_not_found(client, learner_token):
    resp = client.get("/api/certificates/999", headers=auth(learner_token))
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "CERTIFICATE_NOT_FOUND"
