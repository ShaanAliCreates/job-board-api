
import asyncpg
from exceptions import JobNotFoundError,NoJobs
import logging

logger=logging.getLogger(__name__)
class analyticsService:
    def __init__(self,conn:asyncpg.connection):
        self.conn=conn

    
    async def hiring_velocity(self,days:int):
        jobs=await self.conn.fetch("with recentjobs as (select company_id,count(*) as total_jobs from jobs where status='active' and created_at > now() - interval '1 day' * $1 group by company_id) select c.name,rj.total_jobs,rank() over(order by total_jobs desc) as rank,round(rj.total_jobs*100/sum(rj.total_jobs) over(),2) as contriPercentage from recentjobs rj join companies c on rj.company_id=c.id ",days)
        
        
        return{
            "jobs":[dict(job) for job in jobs]
            }
    
    async def topSkills(self,limit:int):
        jobs=await self.conn.fetch("with allskills as(select j.id as jobId,j.title as jobTitle,s.name as skillName from jobs j " 
                                    "join job_skills js on j.id=js.job_id "
                                    "join skills s on js.skill_id=s.id where j.status='active') "
                                    "select skillName as skill,count(distinct jobId) as job_count,rank() over(order by count(distinct jobId) desc) as rank "
                                    "from allskills group by skillName limit $1",limit)
        
        
        
        return{
            "jobs":[dict(job) for job in jobs]
            }
    
#name iska funnel analysis hai but here we are analysing the conversion % of the respective status with running total
    async def funnel_analysis(self):
        jobs=await self.conn.fetch("with appStatus as(select status ,count(*)  as count from applications group by status), totalcount as (select sum(count ) as total from appStatus) "
                                    "select aps.status as status,aps.count as count,round(aps.count*100/t.total,2) as conversion_pct,sum(aps.count) over(order by aps.count desc)::int as running_total from appStatus aps,totalcount t "
                                   "order by aps.count desc ")
        
        
        return{
            "jobs":[dict(job) for job in jobs]}