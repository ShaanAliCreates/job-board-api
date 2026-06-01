import asyncpg
import logging
from models import CompanyCreate
logger=logging.getLogger(__name__)

class companyService:
    def __init__(self,conn:asyncpg.Connection):
        self.conn=conn

    async def create(self,data:CompanyCreate):
        row=await self.conn.fetchrow("insert into companies(name,email,website) values($1,$2,$3) returning*",data.name,data.email,data.website)
        return dict(row)
    
    async def getCompList(self,limit:int,skip:int):
        rows=await self.conn.fetch("select * from companies "
                     "where is_active=TRUE "
                     "order by created_at "
                     "limit $1 offset $2",limit,skip
                     )
        return{
            "rows":[dict(r) for r in rows]
            }


