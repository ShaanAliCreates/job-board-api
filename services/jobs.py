import asyncpg
import logging
from exceptions import JobNotFoundError,InvalidCursor
from models import filterData
from typing import Optional
import base64
from datetime import datetime

logger=logging.getLogger(__name__)

class JobServices:
    def __init__(self,conn:asyncpg.Connection):
          self.conn=conn

    async def create(self,data:dict,company_id:int,)->dict:
        async with self.conn.transaction():
            row= await self.conn.fetchrow("insert into jobs(company_id,title,location,description,salary_min,salary_max,is_remote) values($1,$2,$3,$4,$5,$6,$7) returning *",company_id,data.title,data.location,data.description,data.salary_min,data.salary_max,data.is_remote)

            job=dict(row)

            for sk in data.skills:
                clean=sk.lower().strip()
                skill= await self.conn.fetchrow("insert into skills(name) values($1) on conflict(name) do update set name=excluded.name returning id",clean)

                await self.conn.fetchrow("insert into job_skills(job_id,skill_id) values($1,$2)",job['id'],skill['id'])

            job['skills']=data.skills
            return job
        
    
    async def getJobId(self,job_id:int)->dict:
        row = await self.conn.fetchrow("select c.name as company_name,j.*,coalesce(ARRAY_AGG(s.name) filter(where s.name is not null),ARRAY[]::text[]) as skills from jobs j join companies c on j.company_id=c.id left join job_skills js on j.id=js.job_id left join skills s on js.skill_id=s.id where j.id=$1 and j.status='active' group by j.id,c.name",job_id)
        if not row:
            raise JobNotFoundError(job_id)
        return dict(row)


    async def deleteJob(self,job_id:int)->dict:
        row= await self.conn.execute("update jobs set status='inactive' where id=$1 and status='active' returning id",job_id)

        if row=="UPDATE 0":
            raise JobNotFoundError(job_id)
        
    async def getList(self,data:filterData)->dict:
        condition=["j.status=$1 "]
        params=[data.status]
        param_count=1

        if data.location:
            param_count+=1
            condition.append(f"j.location=${param_count}")
            params.append(data.location)
        
        if data.salary_min:
            param_count+=1
            condition.append(f"j.salary_min>=${param_count}")
            params.append(data.salary_min)

        if data.salary_max:
            param_count+=1
            condition.append(f"j.salary_max<=${param_count}")
            params.append(data.salary_max)

        if data.is_remote is not None:
            param_count+=1
            condition.append(f"j.is_remote=${param_count}")
            params.append(data.is_remote)

        skillFilter=""
        if data.skills:
            skill_list=[s.lower().strip() for s in data.skills.split(",")]
            param_count+=1
            skillFilter=f"and j.id in (select js.job_id from job_skills js join skills s on js.skill_id=s.id where s.name=any(${param_count}::text[]) group by js.job_id having count(distinct s.name)={len(skill_list)})"
            params.append(skill_list)
        where_clause=" and ".join(condition)

        count_sql=f"select count(distinct j.id) from jobs j join companies c on j.company_id=c.id where {where_clause}{skillFilter}"

        data_sql = f"""
    SELECT
        j.id,
        j.title,
        j.location,
        j.salary_min,
        j.salary_max,
        j.is_remote,
        j.company_id,
        j.description,
        j.status,
        j.created_at,
        c.name AS company_name,
        COALESCE(
            array_agg(DISTINCT s.name) FILTER (WHERE s.name IS NOT NULL),
            array[]::text[]
        ) AS skills
    FROM jobs j
    JOIN companies c ON j.company_id = c.id
    LEFT JOIN job_skills js ON js.job_id = j.id
    LEFT JOIN skills s ON js.skill_id = s.id
    WHERE {where_clause} {skillFilter}
    GROUP BY
        j.id, j.title, j.location,
        j.salary_min, j.salary_max,
        j.is_remote, j.company_id,
        j.description, j.status, j.created_at,
        c.name
    ORDER BY j.created_at
    LIMIT ${param_count + 1} OFFSET ${param_count + 2}
"""

        total= await self.conn.fetchval(count_sql,*params)
        rows=await self.conn.fetch(data_sql,*params,data.limit,data.skip)
        
        return{
            "items":[dict(r) for r in rows],
            "total":total,
            "limit":data.limit,
            "offset":data.skip
        }
    

    async def get_cursorList(self,cursor:Optional[str],limit:int,status:str):
        if cursor:
            try:
                decode=base64.b64decode(cursor).decode()
                cursor_time=datetime.fromisoformat(decode)

            except Exception:
                raise InvalidCursor()
            jobs= await self.conn.fetch("select j.id,c.name as company_name,j.title,j.location,j.is_remote,j.created_at from jobs j join companies c on j.company_id=c.id where created_at>$1 and status=$2 order by j.created_at limit $3",cursor_time,status,limit+1)

        else:
            jobs= await self.conn.fetch("select j.id,c.name as company_name,j.title,j.location,j.is_remote,j.created_at from jobs j join companies c on j.company_id=c.id where  status=$1 order by j.created_at limit $2",status,limit+1)

        rows=[dict(r) for r in jobs]

        has_more=len(rows)>limit
        if has_more:
            rows=rows[:limit]

        next_cursor=None
        if has_more and rows:
            last_ts=rows[-1]['created_at'].isoformat()
            next_cursor=base64.b64encode(last_ts.encode()).decode()

        return{
            "jobs":rows,
            "next_cursor":next_cursor,
            "has_more":has_more
        }


