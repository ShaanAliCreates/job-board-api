from fastapi import APIRouter,HTTPException,Depends
from models import Applicantcreate
from dependencies import get_db
import asyncpg

router=APIRouter(prefix="/applicants",tags=["applicants"])

@router.post("/",status_code=201)
async def createApplicant(data:Applicantcreate,conn=Depends(get_db)):
    try:
        row=await conn.fetchrow("insert into applicants(name,email) value($1,$2) returning *",data.name,data.email)
        return dict(row)
    
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=409,detail="Email already registered")
    

@router.get("/{applicant_id}",status_code=200)
async def getapplicant(applicant_id:int,conn=Depends(get_db)):
    row=await conn.fetchrow("select * from applicants where id=$1",applicant_id)

    if not row:
        raise HTTPException(status_code=404,detail="no applicant found of this id")
    
    return dict(row)



