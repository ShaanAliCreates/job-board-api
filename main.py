from fastapi import FastAPI
from routes.companies import router as companyRouter
from routes.jobs import router as jobRouter

app=FastAPI(title="Job board api",version="4.0")

app.include_router(companyRouter)
app.include_router(jobRouter)
@app.get("/health")
async def gethealth():
    return {"status":"ok","version":"4.0"}