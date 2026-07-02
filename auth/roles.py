from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from auth.jwt import decode_token,get_current_applicant
from dependencies import get_conn

companies_schema= OAuth2PasswordBearer(tokenUrl="/auth/company_login",scheme_name="CompanyAuth")

async def require_applicant(current_user:dict=Depends(get_current_applicant)):
    return current_user


async def get_current_company(token:str=Depends(companies_schema),conn=Depends(get_conn)):
    payload=decode_token(token)
    if payload['type'] != "access":
        raise HTTPException(status_code=401,detail="Required access token but found refresh token")
    
    if payload['role'] != "recruiter":
        raise HTTPException(status_code=403,detail="You are not a authorize user for this")
    
    row = await conn.fetchrow("select id ,name ,email from companies where id=$1 and is_active=TRUE",int(payload['sub']))

    if not row:
        raise HTTPException(status_code=401,detail="company not found")
    
    return dict(row)

async def require_recruiter(company:dict=Depends(get_current_company)):
    return company

