from fastapi import APIRouter, Request
from services.whisky_service import get_all_whiskies
from services.data_collection.youtube_url_to_text import process_youtube_url_to_text

router = APIRouter()

@router.get("/get_all_whiskies")
def list_whiskies():
    return get_all_whiskies()




@router.post("/youtube_url_to_text")
async def youtube_url_to_text(request: Request):
    body = await request.json()
    url = body.get("url")
    if not url:
        return ({
            'text': 'text가 없습니다',
        })
    # todo 윗부분 공통화 작업 필요

    if url.startswith('https://www.youtube.com') or url.startswith('https://m.youtube.com'):
        text = process_youtube_url_to_text(url)
    else:
        return ({
            'text': '유튜브 영상이 아닙니다',
        })

    return text


