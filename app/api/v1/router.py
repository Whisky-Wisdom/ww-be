# app/api/v1/router.py

from fastapi import APIRouter
from app.modules.collect.router import router as collect_router
from app.modules.whisky.router import router as whisky_router

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(collect_router)
api_v1_router.include_router(whisky_router)
