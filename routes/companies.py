from fastapi import APIRouter,Depends,HTTPException
from dependencies import get_company_or_404,get_conn
from models import CompanyCreate
import asyncpg

router=APIRouter(prefix="/companies",tags=["companies"])

@router.post("/",status_code=201)
async def createcompany(data:CompanyCreate,conn=Depends(get_conn)):

    row=await conn.fetchrow("insert into companies(name,email,website) values($1,$2,$3) returning *",data.name,data.email,data.website)
    return dict(row)
    

@router.get("/{company_id}",status_code=200)
async def getcompany(company:dict=Depends(get_company_or_404)):
    return company

@router.get("/",status_code=200)
async def getlist(limit:int=10,skip:int=0,conn=Depends(get_conn)):
    rows=await conn.fetch("select * from companies "
                     "where is_active=TRUE "
                     "order by created_at "
                     "limit $1 offset $2",limit,skip
                     )
    return [dict(r) for r in rows]


