import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def get_connection():
    return await asyncpg.connect(host=os.getenv("DB_HOST","localhost"),
                                 database=os.getenv("DB_NAME","jobboard"),
                                 user=os.getenv("DB_USER"),
                                 password=os.getenv("DB_PASSWORD"),
                                 port=int(os.getenv("DB_PORT",5432))
                                 )