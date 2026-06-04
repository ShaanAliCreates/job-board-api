from conftest import make_job,make_company

def test_create_job_success(client):
    co=make_company(client,"testComp","test@gmail.com")
    c_id=co['id']
    r=client.post(f"/jobs/?company_id={c_id}",json={"title":"Engineer","description":"desc","location":"testLocation","salary_min":10000,"salary_max":20000,"is_remote":False,"skills":["python","FastAPI"]})
    assert r.status_code==201
    data=r.json()
    assert data["title"]=="Engineer"
    assert "id" in data

def test_create_job_invalid_company_id(client):
    r=client.post("/jobs/?company_id=9999",json={"title":"Engineer","description":"desc","location":"testLocation","salary_min":10000,"salary_max":20000,"is_remote":False,"skills":["python","FastAPI"]})
    data=r.json()
    assert r.status_code==404
    assert data['type']=="CompanyNotFoundError"


def test_job_with_skills(client):
    co=make_company(client,name="testcomp",email="testmail@gmail.com")
    job=make_job(client,co["id"])
    r=client.get(f"/jobs/{job['id']}")
    assert r.status_code==200
    data=r.json()
    assert data["title"]=="Engineer"
    assert "python" in data["skills"]
    
def test_get_job_not_found(client):
    r=client.get("/jobs/99999")
    data=r.json()
    assert r.status_code==404
    assert data["type"]=="JobNotFoundError"

def test_salary_validtor(client):
    r=client.post("/jobs/",json={"title":"Engineer","description":"desc","location":"Banglore","salary_min":40000,"salary_max":10000,"is_remote":False,"status":"active"})
    assert r.status_code==422

def test_delete_jobs_soft(client):
    co=make_company(client,"testComp","testmail@gmail.com")
    job=make_job(client,co["id"])
    r=client.delete(f"/jobs/{job['id']}")
    assert r.status_code==204

    #checking if status is still active or not

    r2=client.get("/jobs/?status=active")
    ids=[j["id"] for j in r2.json()["items"]]
    assert job["id"] not in ids