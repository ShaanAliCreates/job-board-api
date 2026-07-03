import asyncpg
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

_pool = None 

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "jobboard_test"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            min_size=2,  
            max_size=10   
        )
    return _pool


@asynccontextmanager 
async def get_db():
    pool = await get_pool()
    async with pool.acquire() as conn:
       
        yield conn
        
        