from fastapi import FastAPI ,Request
from fastapi.responses import JSONResponse
import logging
import time
import asyncpg


from routes.auth import router as auth_router
from routes.companies import router as companyRouter
from routes.jobs import router as jobRouter
from routes.applicants import router as applicantRouter
from routes.applications import router as appRouter
from routes.analytics import router as analyticsRouter
from exceptions import JobBoardException

logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger=logging.getLogger(__name__)


app=FastAPI(title="Job board api",version="12.0")


#-----here is middleware of my app

@app.middleware("http")
async def log_requests(request:Request,call_next):
    start=time.perf_counter()
    response= await call_next(request)
    ms=round((time.perf_counter()-start)*1000,2)
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({ms}ms)")
    return response

#--------------Here exception handler start--------------------
@app.exception_handler(JobBoardException)
async def job_board_handler(request: Request,exc: JobBoardException):

    return JSONResponse(
        status_code=exc.status_code,
        content={"error":exc.msg,"type": type(exc).__name__}
    )

@app.exception_handler(asyncpg.UniqueViolationError)
async def unique_violation_handler(request: Request, exc):
    
    return JSONResponse(
        status_code=409,
        content={"error": "Duplicate entry", "type": "UniqueViolationError"}
    )
@app.exception_handler(Exception)
async def global_exception_handler(request: Request,exc: Exception):
    logger.error(f"Unhandled Exception occur on {request.method} {request.url.path}:{exc}",exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error":"Internal Server Error","type":type(exc).__name__}
    )

#-----------Here exception handler end--------------
app.include_router(companyRouter)
app.include_router(jobRouter)
app.include_router(applicantRouter)
app.include_router(appRouter)
app.include_router(analyticsRouter)
app.include_router(auth_router)
@app.get("/health")
async def gethealth():
    return {"status":"ok","version":"12.0"}