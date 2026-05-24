from fastapi import Depends,HTTPException
from db import get_db
from typing import AsyncGenerator

from exceptions import CompanyNotFoundError
import asyncpg


async def get_conn()->AsyncGenerator:
    async with get_db() as conn:
        yield conn


async def get_company_or_404(company_id:int,conn:asyncpg.Connection=Depends(get_conn))->dict:
    row= await conn.fetchrow("select * from companies where id=$1 and is_active=TRUE",company_id)
    if not row:
        raise CompanyNotFoundError(company_id)
    
    return dict(row)