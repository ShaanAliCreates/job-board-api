from fastapi import APIRouter,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import get_conn
from auth.jwt import password_hash,verify,create_access_token,create_refresh_token,decode_token,get_current_applicant
from models import ApplicantRegister,CompanyCreate
import asyncpg

router=APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register")
async def register(data:ApplicantRegister,conn=Depends(get_conn)):
    hashed=password_hash(data.password)

    try:
        row=await conn.fetchrow("insert into applicants(name,email,password_hash) values($1,$2,$3) returning id,name,email",data.name,data.email,hashed)
        return dict(row)
    
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=409,detail="Email already registered")


@router.post("/login")
async def login(data:OAuth2PasswordRequestForm=Depends(),conn=Depends(get_conn)):
    row=await conn.fetchrow("select id,name,password_hash from applicants where email=$1 and is_active=TRUE",data.username)

    if not row or not verify(data.password,row['password_hash']):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    access_token=create_access_token({"sub":str(row['id'])})
    refresh_token=create_refresh_token({"sub":str(row['id'])})

    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }


@router.post("/refresh")
async def refresh(token:str,conn=Depends(get_conn)):
    payload=decode_token(token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401,detail="Please provide refresh token not access token")
    
    new_access=create_access_token({"sub":payload['sub']})
    return {
        "access_token":new_access,
        "access_type":"bearer"
    }


@router.get("/me")
async def me(current_user=Depends(get_current_applicant)):
    from auth.jwt import get_current_applicant
    return current_user

@router.post("/company_register")
async def company_register(data:CompanyCreate,conn=Depends(get_conn)):
    hashed=password_hash(data.password)

    row=await conn.fetchrow("update companies set password_hash=$1 where email=$2 and is_active=true returning id,name,email",hashed,data.email)
    if not row:
        raise HTTPException(status_code=404,detail="company not found first create company then register")
    
    return dict(row)

@router.post("/company_login")
async def company_login(form:OAuth2PasswordRequestForm=Depends(),conn=Depends(get_conn)):
    row = await conn.fetchval("select id,email,password_hash from companies where email=$1 and is_active=true",form.username)
    if not row or not verify(form.password,row['password_hash']):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    
    access_token=create_access_token({"sub":str(row['id']),"role":"recruiter"})
    return {"access_token":access_token,"token_type":"bearer"}
