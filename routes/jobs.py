from fastapi import APIRouter,Depends
from models import JobCreate,CursorResponse,filterData,GetListResponse,GetListIdResponse,JobResponse
from dependencies import get_conn,get_company_or_404
from typing import Optional
from services.jobs import JobServices


router=APIRouter(prefix="/jobs",tags=["jobs"])

@router.get("/cursor",status_code=200,response_model=CursorResponse)
async def list_job_cursor(cursor:Optional[str]=None,limit:int=20,status:str='active',conn=Depends(get_conn)):
    svc=JobServices(conn)
    return await svc.get_cursorList(cursor,limit,status)

@router.post("/",status_code=201,response_model=JobResponse)
async def createjob(data:JobCreate,company:dict=Depends(get_company_or_404),conn=Depends(get_conn)):
    svc=JobServices(conn)
    return await svc.create(data,company['id'])

@router.get("/",status_code=200,response_model=GetListResponse)
async def getlist(data:filterData=Depends(),conn=Depends(get_conn)):
    svc=JobServices(conn)
    return await svc.getList(data)

@router.get("/{job_id}",status_code=200,response_model=GetListIdResponse)
async def getjob(job_id:int,conn=Depends(get_conn)):
    svc=JobServices(conn)
    return await svc.getJobId(job_id)


@router.delete("/{job_id}",status_code=204)
async def deletejob(job_id:int,conn=Depends(get_conn)):
    svc=JobServices(conn)
    return await svc.deleteJob(job_id)