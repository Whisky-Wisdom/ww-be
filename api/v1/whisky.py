from fastapi import APIRouter
from services.whisky_service import get_all_whiskies

router = APIRouter()

@router.get("/get_all_whiskies")
def list_whiskies():
    return get_all_whiskies()



