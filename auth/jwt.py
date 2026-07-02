from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from passlib.context import CryptContext
from dependencies import get_conn
from datetime import datetime,timedelta,timezone
import os


SECRET_KEY=os.getenv("SECRET_KEY","ddf2eb01c084017375f8819692557b7d5c73a6cc16becb32536b60c22c852fa1")
ALGORITHM="HS256"
ACCESS_TOKEN_LIMIT_IN_MINUTES=30
REFRESH_TOKEN_LIMIT_IN_DAYS=7


pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto")
OAuth2_schema= OAuth2PasswordBearer(tokenUrl="/auth/login",scheme_name="ApplicantAuth")

def password_hash(password:str)->str:
    return pwd_context.hash(password)

def verify(plain:str,hash:str)->bool:
    return pwd_context.verify(plain,hash)

def create_access_token(data:dict):
    payload=data.copy()
    payload["exp"]=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_LIMIT_IN_MINUTES)
    payload["type"]="access"
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


def create_refresh_token(data:dict):
    payload=data.copy()
    payload["exp"]=datetime.now(timezone.utc)+timedelta(days=REFRESH_TOKEN_LIMIT_IN_DAYS)
    payload["type"]="refresh"
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


def decode_token(token:str)->str:
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or experied token",
            headers={"www-Authenticate":"Bearer"}
        )
    
async def get_current_applicant(token:str=Depends(OAuth2_schema),conn=Depends(get_conn)):
    payload=decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401,detail="Use access token not refresh token")
    
    row = await conn.fetchrow("select id,name,email from applicants where id=$1 and is_active=True",int(payload["sub"]))

    if not row:
        raise HTTPException(status_code=401,detail="Applicant not found or deactivated")
    
    return dict(row)
    