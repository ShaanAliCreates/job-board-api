from fastapi import HTTPException,APIRouter,Depends
from models import TopSkillItem,HiringVelocityItem,FunnelItems
from dependencies import get_conn
from services.analytics import analyticsService
import asyncpg

router=APIRouter(prefix="/analytics",tags=["analytics"])

@router.get("/hiring-velocity",status_code=200)
async def getHiringVelocity(days:int,conn=Depends(get_conn)):
    svc=analyticsService(conn)
    return await svc.hiring_velocity(days)

@router.get("/top-skills",status_code=200)
async def getTopSkills(limit:int=30,conn=Depends(get_conn)):
    svc=analyticsService(conn)
    return await svc.topSkills(limit)

@router.get("/funnel-analysis",status_code=200)
async def getFunnelAnalysis(conn=Depends(get_conn)):
    svc=analyticsService(conn)
    return await svc.funnel_analysis()