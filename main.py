from fastapi import FastAPI
import asyncpg
from db import get_connection

app=FastAPI(title="job board api",version="1.0")

@app.get("/health")
async def health():
    return {"status":"ok","version":"1.0"}

@app.post("/jobs")
async def create_job(title:str,company:str,location:str):
    conn=await get_connection()
    try:
        row = await conn.fetchrow("insert into jobs(title,company,location) values($1,$2,$3) returning *",title,company,location)
        return dict(row)
    
    finally:
        await conn.close()


@app.get("/jobs/{job_id}")
async def get_job(job_id:int):
    conn=await get_connection()

    try:
        row=await conn.fetchrow("select * from jobs where id=$1",job_id)
        if not row:
            return {"error":"not found"}
        return dict(row)
    finally:
        await conn.close()

@app.get("/jobs")
async def get_job():
    conn=await get_connection()

    try:
        rows=await conn.fetch("select * from jobs")
        if not rows:
            return {"error":"not found"}
        return [dict(row) for row in rows]
    finally:
        await conn.close()
