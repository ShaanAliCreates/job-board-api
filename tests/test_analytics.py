from conftest import make_job,make_company,make_applicant

def test_top_skills_empty(client):
    r=client.get("/analytics/top-skills")
    r.status_code==200
    assert r.json()["jobs"]==[]

def test_top_skills_with_data(client):
    co=make_company(client)

    make_job(client,co["id"])
    make_job(client,co["id"],title="SDE2")

    r=client.get("/analytics/top-skills?limit=5")
    assert r.status_code==200
    data = r.json()["jobs"]

    skills = [item["skill"] for item in data]

    assert "python" in skills
    assert data[0]["rank"] == 1

def test_funnel_analysis_empty(client):
    r=client.get("/analytics/funnel-analysis")
    assert r.status_code==200
    assert r.json()["jobs"]==[]