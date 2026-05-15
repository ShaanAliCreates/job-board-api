from fastapi import FastAPI
from routes.companies import router as companyRouter

app=FastAPI(title="Job board api",version="3.0")

app.include_router(companyRouter)

@app.get("/health")
async def gethealth():
    return {"status":"ok","version":"3.0"}