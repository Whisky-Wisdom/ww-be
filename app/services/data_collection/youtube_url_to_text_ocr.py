import yt_dlp
import re
import pytesseract  # Tesseract OCR 라이브러리 임포트
import cv2
import uuid
import os
from tqdm import tqdm


# 편집이 없는 동영상의 경우 (메뉴판 가격이 그대로 나와있는 경우)
def process_youtube_url_to_text_ocr(url):
    mp4_file = download_video(url)
    print("동영상 다운 완료")

    frames = extract_frames(mp4_file, interval_sec=1.0)
    print(f"{len(frames)}개의 프레임 추출 완료")

    extracted_data = []

    # if frames:
    #     cv2.imwrite("first_frame.png", frames[20])  # n 번째 프레임을 저장


    for i, frame in tqdm(enumerate(frames), total=len(frames), desc="프레임 처리 중"):
        # 프레임에서 텍스트 추출
        text = extract_text_from_frame(frame)
        if text:
            print(f"{i}번째 프레임에서 텍스트 발견: {text}")
            extracted_data.append(text)

    # 동영상 파일 삭제
    os.remove(mp4_file)
    print(f"동영상 파일 {mp4_file} 삭제 완료.")

    return {"results": extracted_data}


# 동영상에서 프레임을 추출
def extract_frames(video_path, interval_sec=2.0):
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    interval_frames = int(fps * interval_sec)

    frames = []
    count = 0
    success, image = vidcap.read()
    while success:
        if count % interval_frames == 0:
            frames.append(image)
        success, image = vidcap.read()
        count += 1
    vidcap.release()
    return frames


# 1. datatemp 디렉토리에 유튜브 URL에서 동영상을 다운로드하고 MP4로 저장
def download_video(url):
    filename = f"{uuid.uuid4()}.mp4"
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': filename,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename


# 프레임에서 텍스트 추출 (OCR 처리)
def extract_text_from_frame(frame):
    # 이미지를 그레이스케일로 변환
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 이미지에 대해 한글 OCR 실행
    text = pytesseract.image_to_string(gray_image, lang='kor')

    # 텍스트가 비어 있지 않으면 반환
    if text.strip():
        return text.strip()
    return None