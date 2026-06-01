from fastapi import APIRouter,Depends
from models import Applicantcreate,Applicantresponse
from dependencies import get_conn
import asyncpg
from exceptions import ApplicantNotFoundError
from services.applicants import ApplicantServices

router=APIRouter(prefix="/applicants",tags=["applicants"])

@router.post("/",status_code=201,response_model=Applicantresponse)
async def createApplicant(data:Applicantcreate,conn=Depends(get_conn)):
    svc=ApplicantServices(conn)
    return await svc.create(data)
    
    
@router.get("/{applicant_id}",status_code=200,response_model=Applicantresponse)
async def getapplicant(applicant_id:int,conn=Depends(get_conn)):
   svc=ApplicantServices(conn)
   return await svc.getApplicant(applicant_id)