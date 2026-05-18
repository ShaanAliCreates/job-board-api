from fastapi import FastAPI
from routes.companies import router as companyRouter
from routes.jobs import router as jobRouter
from routes.applicants import router as applicantRouter
from routes.applications import router as appRouter
app=FastAPI(title="Job board api",version="6.0")

app.include_router(companyRouter)
app.include_router(jobRouter)
app.include_router(applicantRouter)
app.include_router(appRouter)
@app.get("/health")
async def gethealth():
    return {"status":"ok","version":"6.0"}