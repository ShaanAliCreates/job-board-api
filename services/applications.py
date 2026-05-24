from fastapi import HTTPException
import asyncpg
from exceptions import ApplicationNotFoundError,DuplicateApplicationError,InvalidTranstionError,JobNotActiveError,NoJobs

valid_transition={
    "applied":["screening","rejected"],
    "screening":["interview","rejected"],
    "interview":["offer","rejected"],
    "offer":["rejected"],
    "rejected":[] #this is terminal no transaction allowed here alsoo, it is dead state of FSM
}

class ApplicationService:
    def __init__(self,conn:asyncpg.connection):
        self.conn=conn

# for handling the apply logic

    async def apply(self,job_id:int,applicant_id:int):
        job= await self.conn.fetchrow("select * from jobs where status='active' and id=$1",job_id)

        if not job or job['status']!='active':
            raise JobNotActiveError()
        
        
        row= await self.conn.fetchrow("insert into applications(applicant_id,job_id) values($1,$2) returning *",applicant_id,job_id)

        return dict(row)
    

# for handling the transition logics

    async def transition_state(self,application_id:int,new_state:str):
        app= await self.conn.fetchrow("select * from applications where id=$1",application_id)

        if not app:
            raise ApplicationNotFoundError(application_id)
        
        current=app['status']
        allowed=valid_transition.get(current,[])

        if new_state not in allowed:
            raise InvalidTranstionError(current,new_state,allowed)
        
        row=await self.conn.fetchrow("update applications set status =$1,update_at=now() where id=$2 returning *",new_state,application_id)

        return dict(row)
        
# for the get_application logic
    async def get_application(self,application_id:int):
        row=await self.conn.fetchrow("select a.*,j.title,ap.name,ap.email from applications a join jobs j on a.job_id=j.id join applicants ap on a.applicant_id=ap.id where a.id=$1",application_id )
        
        if not row:
            raise ApplicationNotFoundError(application_id)

        return dict(row)
        
    
