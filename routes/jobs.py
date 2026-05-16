from fastapi import APIRouter,Depends,HTTPException
from models import JobCreate
from dependencies import get_conn,get_company_or_404
import asyncpg

router=APIRouter(prefix="/jobs",tags=["jobs"])


@router.post("/",status_code=201)
async def createjob(data:JobCreate,company:dict=Depends(get_company_or_404),conn=Depends(get_conn)):
    async with conn.transaction():
        row= await conn.fetchrow("insert into jobs(company_id,title,description,location,salary_min,salary_max,is_remote) values($1,$2,$3,$4,$5,$6,$7) returning *",company['id'],data.title,data.description,data.location,data.salary_min,data.salary_max,data.is_remote)

    
    job=dict(row)

    #here handling many to many relation of job and skills okk
    for sk in data.skills:
        clean=sk.lower().strip()
        skill=await conn.fetchrow("insert into skills(name) values($1) "
                              "on conflict(name) do update set name=excluded.name returning id",clean)
        
        await conn.execute("insert into job_skills(job_id,skill_id) "
                           "values($1,$2)",job['id'],skill['id'])
        #here jobcreate model into the form of data came
        #since no skill column in job but in skills relation
        #so we inesrt rest of details into job 
        # and we insert the skill in the skills relation then in job_skills relation
        #now response should include skills
        #so we gave back the incoming data.skill into the job['skills'] response
        job['skills']=data.skills
        return job
        





@router.get("/{job_id}",status_code=200)
async def getjob(job_id:int,conn=Depends(get_conn)):
    row= await conn.fetchrow("select c.name,j.*,coalesce(ARRAY_AGG(s.name) filter(where s.name is not null),ARRAY[]::text[]) " 
                             "from jobs j join companies c on j.company_id=c.id left join job_skills js on j.id=js.job_id "
                             "left join skills s on js.skill_id=s.id where j.id=$1 group by j.id,c.name",job_id)
    if not row:
        raise HTTPException(status_code=404,detail="Job details not found,Enter a valid job id")
    return dict(row)

@router.get("/",status_code=200)
async def getlist(limit:int=10,skip:int=0,company_id:int|None=None,conn=Depends(get_conn)):
    if not company_id:
        row=await conn.fetch("select j.*,c.name as Compnay_Name from jobs j join companies c on j.company_id=c.id where status='active' order by created_at desc limit $1 offset $2",limit,skip)
    else:
        row=await conn.fetch("select j.*,c.name as Compnay_Name from jobs j join companies c on j.company_id=c.id where status='active' and c.id =$1 order by created_at desc limit $2 offset $3",company_id,limit,skip)
    return [dict(r) for r in row]

@router.delete("/{job_id}",status_code=204)
async def deletejob(job_id:int,conn=Depends(get_conn)):
    row= await conn.execute("update jobs set status='inactive' where status='active' and id=$1",job_id)

    if row == "UPDATE 0"or"update 0"or"Update 0":
        raise HTTPException(status_code=404,detail="job not found or already closed")
    
    