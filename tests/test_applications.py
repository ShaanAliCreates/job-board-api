from conftest import make_applicant ,make_company,make_job

def _apply(client,job_id:int,applicant_id:int):
    return client.post(f"/applications/?job_id={job_id}&applicant_id={applicant_id}")

def _transtion(client,application_id:int,status:str):
    return client.patch(f"/applications/{application_id}/status",json={"status":status})


def test_apply_success(client):
    co=make_company(client,name="testClient",email="testMail@gmail.com")
    job=make_job(client,co["id"])
    appli=make_applicant(client)
    r=_apply(client,job["id"],appli["id"])
    assert r.status_code==201
    assert r.json()["status"]=="applied"

def test_apply_duplicate(client):
    co=make_company(client)
    job=make_job(client,co["id"])
    appli=make_applicant(client)
    r=_apply(client,job["id"],appli["id"])
    r2=_apply(client,job["id"],appli["id"])

    assert r2.status_code==409
    assert r2.json()["type"]=="DuplicateApplicationError"

def test_valid_transition_applied_to_screening(client):
    co=make_company(client)
    job=make_job(client,co["id"])
    appli=make_applicant(client)
    application=_apply(client,job["id"],appli["id"]).json

    r=_transtion(client,application["id"],"screening")
    assert r.status_code==200
    assert r.json()["status"]=="applied"

def test_invalid_transition_applied_to_offer(client):
    co=make_company(client)
    job=make_job(client,co["id"])
    appli=make_applicant(client)

    application=_apply(client,job["id"],appli["id"]).json()

    r=_transtion(client,application["id"],"offer")

    assert r.status_code==400
    assert r.json()["type"]=="InvalidTranstionError"

def test_terminal_state_rejected(client):
    co=make_company(client)
    job=make_job(client,co["id"])
    appli=make_applicant(client)

    application=_apply(client,job["id"],appli["id"]).json()

    r=_transtion(client,application["id"],"rejected")
    r2=_transtion(client,application["id"],"screening")

    assert r2.status_code==400
    assert r2.json()["type"]=="InvalidTranstionError"

def test_closed_job(client):
    co=make_company(client)
    job=make_job(client,co["id"])
    client.delete(f"/job/{job['id']}")
    applicant=make_applicant(client)

    r=_apply(client,job["id"],applicant["id"])
    assert r.status_code==404
    assert r.json()["type"]=="JobNotFoundError"


