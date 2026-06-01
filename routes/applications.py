from fastapi import APIRouter,Depends
from models import StatusTransitionRequest,Applicationresponse
from dependencies import get_conn
from services.applications import ApplicationService
import asyncpg


router=APIRouter(prefix="/applications",tags=["applications"])

@router.post("/",status_code=201,response_model=Applicationresponse)
async  def apply_to_job(job_id:int,applicant_id:int,conn=Depends(get_conn)):
    svc=ApplicationService(conn)

    return await svc.apply(job_id,applicant_id)

@router.get("/{application_id}",status_code=200,response_model=Applicationresponse)
async def getApplication(application_id:int,conn=Depends(get_conn)):
    svc=ApplicationService(conn)
    return await svc.get_application(application_id)

@router.patch("/{application_id}",status_code=201,response_model=Applicationresponse)
async def updateStatus(application_id:int,body:StatusTransitionRequest,conn=Depends(get_conn)):
    svc=ApplicationService(conn)
    return await svc.transition_state(application_id,body.status)



