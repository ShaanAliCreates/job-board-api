from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timezone,timedelta
import os
from dependencies import get_conn
from jose import JWTError,jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY","")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7 

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain:str,hashed:str)->bool:
    return pwd_context.verify(plain,hashed)


def create_access_token(data:dict)->str:
    payload=data.copy()
    payload["exp"]=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["type"]="access"
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def create_refresh_token(data:dict)->str:
    payload=data.copy()
    payload["exp"]=datetime.now(timezone.utc)+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload["type"]="refresh"
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)