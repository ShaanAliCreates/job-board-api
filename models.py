from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


# ── JOB SCHEMAS ──────────────────────────────────────────────

class JobCreate(BaseModel):
    """Input schema — what the client sends to create a job."""
    title:       str
    description: str
    location:    Optional[str] = None    # optional — remote jobs have no location
    salary_min:  Optional[int] = None    # optional — many Indian cos hide salary
    salary_max:  Optional[int] = None
    is_remote:   bool = False
    skills:      list[str] = []           # names — we resolve to IDs in route

    @field_validator('salary_max')
    @classmethod
    def max_above_min(cls, v, info):
        # info.data holds already-validated fields
        # salary_min validated first (field order matters in Pydantic v2)
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
    # notice: description not here — list view doesn't need it
    # notice: company_id not here — internal FK, clients don't need raw IDs


# ── COMPANY SCHEMAS ──────────────────────────────────────────

class CompanyCreate(BaseModel):
    """Input schema for registering a company."""
    name:    str
    email:   EmailStr              # pydantic validates email format — pip install pydantic[email]
    website: Optional[str] = None


class CompanyResponse(BaseModel):
    id:        int
    name:      str
    email:     str
    website:   Optional[str]
    is_active: bool