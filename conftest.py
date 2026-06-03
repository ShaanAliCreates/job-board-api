import pytest
import asyncio
import os
import asyncpg
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="session")
def event_loop():
    loop= asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def client():
    os.environ["DB_NAME"] = "jobboard_test"
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
async def clean_db():
    conn = await asyncpg.connect(
        host=os.getenv("DB_HOST","localhost"),
        database=os.getenv("DB_NAME","jobboard_test"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT",5432))
    )

    await conn.execute("TRUNCATE applications,job_skills,jobs,skills,applicants,companies RESTART IDENTITY CASCADE")
    await conn.close()
    yield

    #-------------------------------------------------- 
def make_company(client,name="TestCo",email="Test@Co.com"):
    r=client.post("/companies/",json={"name":name,"email":email})
    assert r.status_code == 201
    return r.json()
    

def make_job(client,company_id:int,title="Engineer"):
    r=client.post(f"/jobs/?company_id={company_id}",json={"title":title,"company_id":company_id,"description":"desc","location":"banglore","skills":["python"]})
    assert r.status_code == 201
    return r.json()

def make_applicant(client,email="Test@Co.com"):
    r=client.post("/applicants/",json={"name":"TestUser","email":email})
    assert r. status_code == 201
    return r.json()