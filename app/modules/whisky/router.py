from fastapi import APIRouter, Request


router = APIRouter(prefix="/whisky")


@router.get("/a")
async def process_collect_data(request: Request):





    return {"asdasd":"aasdasdasdasdasd"}
