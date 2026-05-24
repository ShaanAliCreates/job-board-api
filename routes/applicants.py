from fastapi import APIRouter,HTTPException,Depends
from models import Applicantcreate
from dependencies import get_conn
import asyncpg
from exceptions import ApplicantNotFoundError

router=APIRouter(prefix="/applicants",tags=["applicants"])

@router.post("/",status_code=201)
async def createApplicant(data:Applicantcreate,conn=Depends(get_conn)):
    row=await conn.fetchrow("insert into applicants(name,email) values($1,$2) returning *",data.name,data.email)
    return dict(row)
    
    
    

@router.get("/{applicant_id}",status_code=200)
async def getapplicant(applicant_id:int,conn=Depends(get_conn)):
    row=await conn.fetchrow("select * from applicants where id=$1",applicant_id)

    if not row:
        raise ApplicantNotFoundError(applicant_id)
    
    return dict(row)



