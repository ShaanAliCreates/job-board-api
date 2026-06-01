from fastapi import APIRouter,Depends
from dependencies import get_company_or_404,get_conn
from models import CompanyCreate,CompanyResponse,CompanyListResponse
import asyncpg
from services.companies import companyService

router=APIRouter(prefix="/companies",tags=["companies"])

@router.post("/",status_code=201,response_model=CompanyResponse)
async def createcompany(Alldata:CompanyCreate,conn=Depends(get_conn)):
    svc=companyService(conn)
    return await svc.create(Alldata)
    

@router.get("/",status_code=200,response_model=CompanyListResponse)
async def getlist(limit:int=10,skip:int=0,conn=Depends(get_conn)):
   svc=companyService(conn)
   return await svc.getCompList(limit,skip)


@router.get("/{company_id}",status_code=200,response_model=CompanyResponse)
async def getcompany(company:dict=Depends(get_company_or_404)):
    return company

