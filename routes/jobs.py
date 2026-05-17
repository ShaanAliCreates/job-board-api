from fastapi import APIRouter,Depends,HTTPException
from models import JobCreate
from dependencies import get_conn,get_company_or_404
from typing import Optional
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
async def getlist(location:Optional[str]=None,
                  is_remote:Optional[bool]=None,
                  salary_min:Optional[int]=None,
                  salary_max:Optional[int]=None,
                  skills:Optional[str]=None,
                  status:str='active',
                  skip: int=0,
                  limit:int=10

                  ,conn=Depends(get_conn)):
    # here is the where claude dynamically
    condition=["j.status=$1 "]
    params=[status]
    param_count=1

    if location:
        param_count+=1
        condition.append(f"j.location ilike ${param_count}")
        params.append(f"%{location}%")
    
    if is_remote is not None:
        param_count+=1
        condition.append(f"j.is_remote=${param_count}")
        params.append(is_remote)
    if salary_min:
        param_count+=1
        condition.append(f"j.salary_min>=${param_count}")
        params.append(salary_min)

    if salary_max:
        param_count+=1
        condition.append(f"j.salary_max<=${param_count}")
        params.append(salary_max)

    # skill filter the tedi kheer one okkkk 
    skill_filter=""
    if skills:
        skill_list=[s.lower().strip() for s in skills.split(",")]
        param_count+=1

        skill_filter=f" and j.id in (select js.job_id from job_skills js join skills s on js.skill_id=s.id where s.name =any(${param_count}::text[]) group by job_id having count(distinct s.name)={len(skill_list)} )"
        params.append(skill_list)

    where_clause=" and ".join(condition)


    #here is the sql for the count 
    count_sql=f"select count(distinct j.id) from jobs j join companies c on j.company_id=c.id where {where_clause}{skill_filter}"

    #here is the sql for the data
    data_sql= (f"""select j.id,j.title,j.location,j.salary_min,j.salary_max,j.is_remote,c.name,coalesce(array_agg(distinct s.name),array[]::text[]) from jobs j join companies c on j.company_id=c.id 
               left join job_skills js on j.id=js.job_id left join skills s on js.skill_id=s.id where {where_clause}{skill_filter} group by j.id,j.title,
               j.location,j.salary_min,j.salary_max,j.is_remote,c.name   order by j.created_at desc limit ${param_count+1} offset ${param_count+2}""")
    
    total=await conn.fetchval(count_sql,*params)
    rows=await conn.fetch(data_sql,*params,limit,skip)
    return{
        "items":[dict(r) for r in rows],
        "total":total,
        "limit":limit,
        "offset":skip

    }

    

@router.delete("/{job_id}",status_code=204)
async def deletejob(job_id:int,conn=Depends(get_conn)):
    row= await conn.execute("update jobs set status='inactive' where status='active' and id=$1",job_id)

    if row == "UPDATE 0"or"update 0"or"Update 0":
        raise HTTPException(status_code=404,detail="job not found or already closed")
    
    