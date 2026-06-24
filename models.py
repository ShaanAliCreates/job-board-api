from pydantic import BaseModel, EmailStr, field_validator,ConfigDict
from typing import Optional
from datetime import datetime




class JobCreate(BaseModel):
    
    title:       str
    description: str
    location:    Optional[str] = None    
    salary_min:  Optional[int] = None
    salary_max:  Optional[int] = None
    is_remote:   bool = False
    skills:      list[str] = []

    @field_validator('salary_max')
    @classmethod
    def max_above_min(cls, v, info):
        if v and info.data.get('salary_min') and v < info.data['salary_min']:
            raise ValueError('salary_max must be >= salary_min')
        return v


class JobResponse(BaseModel):
    
    id:         int
    title:      str
    company_id: int
    description: Optional[str]
    location:   Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    created_at: Optional[datetime]
    is_remote:  bool
    status: str
    skills:Optional[list[str]]
    


class GetListIdResponse(BaseModel):
    id:int
    company_name:Optional[str]
    company_id: Optional[int]
    title:str
    description: Optional[str]
    location:Optional[str]
    salary_min:Optional[int]
    salary_max:Optional[int]
    is_remote:bool
    status: Optional[str]
    skills:list[str]
    created_at: Optional[datetime]

    model_config=ConfigDict(extra="forbid")
    
class GetListResponse(BaseModel):
    items:list[GetListIdResponse]
    total:int
    limit:int
    offset:int
    model_config=ConfigDict(extra="forbid")



class filterData(BaseModel):
    location:Optional[str]=None
    is_remote:Optional[bool]=None
    salary_min:Optional[int]=None
    salary_max:Optional[int]=None
    skills:Optional[str]=None
    status:str='active'
    skip: int=0
    limit:int=10

class CompanyCreate(BaseModel):
    
    name:    str
    email:   EmailStr
    website: Optional[str] = None


class CompanyResponse(BaseModel):
    id:        int
    name:      str
    email:     str
    website:   Optional[str]
    is_active: bool

class CompanyListResponse(BaseModel):
    rows:Optional[list[CompanyResponse]]

class Applicantcreate(BaseModel):
    name:str
    email:EmailStr

class Applicantresponse(BaseModel):
    id:int
    name:str
    email:str
    created_at:Optional[datetime]

class Applicationresponse(BaseModel):
    id:int
    job_id:int
    applicant_id:int
    status:str
    applied_at:Optional[datetime]
    update_at:Optional[datetime]

class StatusTransitionRequest(BaseModel):
    status:str

    @field_validator('status')
    @classmethod
    def must_be_valid(cls,v):
        valid={'applied','screening','interview','offer','rejected'}

        if v not in valid:
            raise ValueError(f"entered status not valid. valid status{valid}")
        return v
    

# here is the model related to my analytics __________________________
class HiringVelocityItem(BaseModel):
    name:str
    total_jobs:int
    rank:int
    contripercentage:float
    model_config=ConfigDict(extra="forbid")

class HiringVelocityResponse(BaseModel):
    jobs:list[HiringVelocityItem]


class TopSkillItem(BaseModel):
    skill:str
    job_count:int
    rank:int

    model_config=ConfigDict(extra="forbid")

class TopSkillResponse(BaseModel):
    jobs:list[TopSkillItem]

class FunnelItems(BaseModel):
    status:str
    count:int
    conversion_pct:float
    running_total:int

    model_config=ConfigDict(extra="forbid")


class FunnelResponse(BaseModel):
    jobs:list[FunnelItems]
    
    


#analytics model end here _________________________________


#-------------------here is our job item used for demostrating the cursor
class CursorJobItem(BaseModel):
    id:int
    company_name:Optional[str]
    title:str
    location:Optional[str]
    is_remote:bool
    created_at:Optional[datetime]

    model_config=ConfigDict(extra="forbid")

    
class CursorResponse(BaseModel):
    jobs:list[CursorJobItem]
    next_cursor:Optional[str]
    has_more:bool


# JWT authentication related model below ----------------------------

class ApplicantRegister(BaseModel):
    name:str
    email:EmailStr
    password:str

    @field_validator('password')
    @classmethod
    def password_strength(cls,v):
        if len(v)<8:
            raise ValueError("Password must be at least of 8 character")
        
        return v
    

class Token_Response(BaseModel):
    access_token:str
    type:str
    refresh_token:Optional[str]=None
    
