from tests.helpers import auth


def test_get_assessment_hides_correct_option(client, learner_token):
    resp = client.get("/api/assessments/2", headers=auth(learner_token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["course_id"] == 2
    assert body["passing_score"] == 60
    assert len(body["questions"]) == 1
    assert "correct_option" not in body["questions"][0]
    assert set(body["questions"][0].keys()) == {
        "id",
        "question_text",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
    }


def test_get_assessment_not_found(client, learner_token):
    resp = client.get("/api/assessments/1", headers=auth(learner_token))
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "ASSESSMENT_NOT_FOUND"


def test_submit_all_correct(client, learner_token):
    resp = client.post(
        "/api/assessments/1/submit", headers=auth(learner_token), json={"answers": {"1": "A"}}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["score"] == 100
    assert body["result"] == "PASS"


def test_submit_below_passing(client, learner_token):
    resp = client.post(
        "/api/assessments/1/submit", headers=auth(learner_token), json={"answers": {"1": "B"}}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["score"] == 0
    assert body["result"] == "FAIL"


def test_submit_unknown_question(client, learner_token):
    resp = client.post(
        "/api/assessments/1/submit", headers=auth(learner_token), json={"answers": {"99": "A"}}
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_SUBMISSION"


def test_submit_invalid_option(client, learner_token):
    resp = client.post(
        "/api/assessments/1/submit", headers=auth(learner_token), json={"answers": {"1": "Z"}}
    )
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_SUBMISSION"


def test_submit_missing_answers(client, learner_token):
    resp = client.post("/api/assessments/1/submit", headers=auth(learner_token), json={})
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_SUBMISSION"


def test_submit_not_found(client, learner_token):
    resp = client.post(
        "/api/assessments/999/submit", headers=auth(learner_token), json={"answers": {"1": "A"}}
    )
    assert resp.status_code == 404


def test_submit_does_not_issue_certificate(client, learner_token, db_session):
    from app.models import Certificate

    client.post(
        "/api/assessments/1/submit", headers=auth(learner_token), json={"answers": {"1": "A"}}
    )
    assert db_session.query(Certificate).count() == 0


def test_list_attempts_admin(client, admin_token):
    resp = client.get("/api/assessments/attempts", headers=auth(admin_token))
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_attempts_learner_forbidden(client, learner_token):
    resp = client.get("/api/assessments/attempts", headers=auth(learner_token))
    assert resp.status_code == 403
