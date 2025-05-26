# app/modules/collect/router.py

from fastapi import APIRouter, Request

from app.modules.collect.service.cleanup_files import cleanup_files
from app.modules.collect.service.download_video import download_video
from app.modules.collect.service.extract_audio_from_video import extract_audio_from_video
from app.modules.collect.service.transcribe_audio_to_text import transcribe_audio_to_text

router = APIRouter(prefix="/collect")

@router.get("/collect-data")
def collect_data():


    return {"message": "데이터 수집 완료"}


@router.get("/process_youtube_url_to_text-data")
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
