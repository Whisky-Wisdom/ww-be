# app/modules/collect/router.py

from fastapi import APIRouter, Request
from app.modules.collect.service import (
    cleanup_files,
    download_video,
    extract_audio_from_video,
    transcribe_audio_to_text,
)
from app.modules.collect.service.ask_to_llm import process_ask_to_llm

router = APIRouter(prefix="/collect")


@router.post("/health_check")
async def process_collect_data(request: Request):
    body = await request.json()
    text = body.get("text")

    return text




@router.post("/process_collect_data")
async def process_collect_data(request: Request):
    body = await request.json()
    text = body.get("text")

    jsondata = process_ask_to_llm(text)


    return jsondata


@router.post("/process_youtube_url_to_text-data")
async def process_youtube_url_to_text(request: Request):
    body = await request.json()
    url = body.get("url")

    # 1. datatemp 디렉토리에 유튜브 URL에서 동영상을 다운로드하고 MP4로 저장
    mp4_file, upload_date = download_video(url)
    print("동영상 다운 완료")
    print(f"업로드 날짜: {upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}")
    # 2. MP4 파일에서 오디오를 추출
    audio_file = extract_audio_from_video(mp4_file)
    print("오디오 추출 완료")

    # 3. 오디오에서 텍스트를 추출 (음성 인식)
    text = transcribe_audio_to_text(audio_file)
    print("텍스트 추출 완료")

    # 4. 동영상 및 오디오 파일 삭제
    cleanup_files(mp4_file, audio_file)
    print("파일 삭제 완료")

    return {
        "date": upload_date,
        "text": text
    }
