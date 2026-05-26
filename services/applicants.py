import asyncpg
import logging
from models import Applicantcreate
from exceptions import ApplicantNotFoundError
logger=logging.getLogger(__name__)


class ApplicantServices:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def create(self,data:Applicantcreate):
        row=await self.conn.fetchrow("insert into applicants(name,email) values($1,$2) returning *",data.name,data.email)
        return dict(row)
    
    async def getApplicant(self,applicant_id:int):
        row=await self.conn.fetchrow("select * from applicants where id=$1",applicant_id)
        
        if not row:
            raise ApplicantNotFoundError(applicant_id)
    
        return dict(row)