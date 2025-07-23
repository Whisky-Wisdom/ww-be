from fastapi import APIRouter, Request

from app.core.process.llm.service import ask_whisky_info_to_llm
from app.features.whisky.collector.prompt.make_whisky_info_promt import make_whisky_prompt
from app.features.whisky.service.total_service import save_whisky_info_to_firestore

from app.shared.utils.local_api import call_api

router = APIRouter(prefix="/collector")

@router.post("/process_youtube_url_to_text_and_save")
async def process_youtube_url_to_text_and_save(request: Request):
    try:
        body = await request.json()
        url = body.get("url")
        description = body.get("description")

        data = await call_api(
            "/process_youtube_url_to_text-data",
            {"url": url}
        )

        upload_date = data["date"]
        text = data["text"]

        year = int(upload_date[:4])
        month = int(upload_date[4:6])

        # 6. LLM 프롬프트 생성 및 요청
        prompt = make_whisky_prompt(text, year, month, description)
        whisky_infos = ask_llm(model, prompt)

        # 7. Firestore에 저장
        save_whisky_info_to_firestore(whisky_infos)

        return {
            "success": True,
            "date": f"{year}-{month:02d}",
            "whisky_infos": whisky_infos
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }




