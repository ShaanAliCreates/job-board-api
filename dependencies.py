from fastapi import Depends,HTTPException
from db import get_db
from typing import AsyncGenerator
import asyncpg


async def get_conn()->AsyncGenerator:
    async with get_db() as conn:
        yield conn


async def get_company_or_404(company_id:int,conn:asyncpg.Connection=Depends(get_conn))->dict:
    row= await conn.fetchrow("select * from companies where id=$1 and is_active=TRUE",company_id)
    if not row:
        raise HTTPException(status_code=404,detail=f"company with id {company_id} not found")
    
    return dict(row)