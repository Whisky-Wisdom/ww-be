# app/modules/collect/router.py

from fastapi import APIRouter, Request
from app.core.collect.youtube.service import service

router = APIRouter(prefix="/collect")



@router.post("/health_check")
async def process_collect_data(request: Request):
    body = await request.json()
    text = body.get("text")

    return text




@router.post("/process_youtube_url_to_text-data")
async def process_youtube_url_to_text(request: Request):
    body = await request.json()
    url = body.get("url")

    mp4_file, upload_date = service.download_video(url)
    print("동영상 다운 완료")
    print(f"업로드 날짜: {upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}")
    # 2. MP4 파일에서 오디오를 추출
    audio_file = service.extract_audio_from_video(mp4_file)
    print("오디오 추출 완료")

    # 3. 오디오에서 텍스트를 추출 (음성 인식)
    text = service.transcribe_audio_to_text(audio_file)
    print("텍스트 추출 완료")

    # 4. 동영상 및 오디오 파일 삭제
    service.cleanup_files(mp4_file, audio_file)
    print("파일 삭제 완료")

    return {
        "date": upload_date,
        "text": text
    }
