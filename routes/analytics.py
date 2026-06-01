from fastapi import APIRouter,Depends
from models import TopSkillResponse,HiringVelocityResponse,FunnelResponse
from dependencies import get_conn
from services.analytics import analyticsService
import asyncpg

router=APIRouter(prefix="/analytics",tags=["analytics"])

@router.get("/hiring-velocity",status_code=200,response_model=HiringVelocityResponse)
async def getHiringVelocity(days:int,conn=Depends(get_conn)):
    svc=analyticsService(conn)
    return await svc.hiring_velocity(days)

@router.get("/top-skills",status_code=200,response_model=TopSkillResponse)
async def getTopSkills(limit:int=30,conn=Depends(get_conn)):
    svc=analyticsService(conn)
    return await svc.topSkills(limit)

@router.get("/funnel-analysis",status_code=200,response_model=FunnelResponse)
async def getFunnelAnalysis(conn=Depends(get_conn)):
    svc=analyticsService(conn)
    return await svc.funnel_analysis()