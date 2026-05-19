from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime




class JobCreate(BaseModel):
    """Input schema — what the client sends to create a job."""
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
    """Output schema — what the API returns. Never expose raw DB rows."""
    id:         int
    title:      str
    location:   Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    is_remote:  bool
    status:     str

class CompanyCreate(BaseModel):
    """Input schema for registering a company."""
    name:    str
    email:   EmailStr
    website: Optional[str] = None


class CompanyResponse(BaseModel):
    id:        int
    name:      str
    email:     str
    website:   Optional[str]
    is_active: bool

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
    application_id:int
    status:str
    applied_at:Optional[datetime]
    updated_at:Optional[datetime]

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
    company:str
    job_count:int
    rank:int
    contriPercentage:float
    class config:
        from_attributes=True


class TopSkillItem(BaseModel):
    skill:str
    job_count:int
    rank:int

    class config:
        from_attributes=True


class FunnelItems(BaseModel):
    status:str
    count:int
    conversion_pct:float
    running_total:int

    class config:
        from_attributes=True
    


#analytics model end here _________________________________