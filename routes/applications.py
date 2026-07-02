from fastapi import APIRouter,Depends,HTTPException
from models import StatusTransitionRequest,Applicationresponse
from dependencies import get_conn
from services.applications import ApplicationService
from auth.jwt import get_current_applicant
from auth.roles import require_applicant,require_recruiter
from auth.roles import require_recruiter, companies_schema

import asyncpg


router=APIRouter(prefix="/applications",tags=["applications"])

@router.post("/",status_code=201,response_model=Applicationresponse)
async  def apply_to_job(job_id:int,current_user:int=Depends(require_applicant),conn=Depends(get_conn)):
    svc=ApplicationService(conn)
    return await svc.apply(job_id,current_user['id'])

@router.get("/{application_id}",status_code=200,response_model=Applicationresponse)
async def getApplication(application_id:int,conn=Depends(get_conn)):
    svc=ApplicationService(conn)
    return await svc.get_application(application_id)


@router.patch("/{application_id}/status",response_model=Applicationresponse)
async def update_status(application_id: int,body: StatusTransitionRequest,recruiter: dict = Depends(require_recruiter),conn = Depends(get_conn)):
    owns = await conn.fetchrow("select count(*) from application a join jobs j on a.job_id=j.id where j.id=$1 and j.company_id=$2",application_id,recruiter['id'])
    if not owns:
        raise HTTPException(status_code=403,detail="You are not authorize for this application")
    svc=ApplicationService(conn)
    return await svc.transition_state(application_id,body.status)



