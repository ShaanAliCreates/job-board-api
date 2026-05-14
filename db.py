import asyncpg
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

_pool = None  # module-level singleton — created once, reused forever


async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "jobboard"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            min_size=2,   # keep 2 connections alive even when idle
            max_size=10   # never open more than 10 simultaneous connections
        )
    return _pool


@asynccontextmanager  # makes this usable with "async with"
async def get_db():
    pool = await get_pool()
    async with pool.acquire() as conn:
        # pool.acquire() checks out a connection from the pool
        # yield passes it to the caller (your route function)
        # when async with block exits — even on exception —
        # asyncpg automatically returns the connection to the pool
        yield conn
         # conn.close() is NOT called — goes back to pool, stays alive