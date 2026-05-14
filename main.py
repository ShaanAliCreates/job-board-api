from fastapi import FastAPI, HTTPException
from db import get_db
from models import JobCreate, JobResponse, CompanyCreate, CompanyResponse

app = FastAPI(title="Job Board API", version="2.0")


@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0"}


@app.post("/companies", response_model=CompanyResponse)
async def create_company(data: CompanyCreate):
    # data is already validated by Pydantic before this runs
    async with get_db() as conn:
        row = await conn.fetchrow(
            """INSERT INTO companies (name, email, website)
               VALUES ($1, $2, $3) RETURNING *""",
            data.name, data.email, data.website
        )
        return dict(row)
    # pool connection auto-released here — no try/finally needed


@app.post("/jobs", response_model=JobResponse)
async def create_job(data: JobCreate, company_id: int):
    async with get_db() as conn:
        # verify company exists — better error message than raw FK violation
        company = await conn.fetchrow(
            "SELECT id FROM companies WHERE id = $1", company_id
        )
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        row = await conn.fetchrow(
            """INSERT INTO jobs
                 (company_id, title, description, location,
                  salary_min, salary_max, is_remote)
               VALUES ($1, $2, $3, $4, $5, $6, $7)
               RETURNING *""",
            company_id, data.title, data.description, data.location,
            data.salary_min, data.salary_max, data.is_remote
        )
        return dict(row)


@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: int):
    async with get_db() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM jobs WHERE id = $1", job_id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Job not found")
        return dict(row)