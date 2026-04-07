from fastapi import APIRouter

from fake_news_detector.controller import router as fake_news_detector_router
from health.controller import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(fake_news_detector_router)
