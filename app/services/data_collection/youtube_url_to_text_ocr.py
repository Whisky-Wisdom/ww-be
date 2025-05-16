import yt_dlp
import re
import easyocr
import cv2
import uuid
import os
from tqdm import tqdm

# EasyOCR 모델 초기화 (다국어 지원)
reader = easyocr.Reader(['en', 'ko'])


# 편집이 없는 동영상의 경우 (메뉴판 가격이 그대로 나와있는경우)
def extract_text_from_frame_easyocr(frame):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러를 사용하여 노이즈를 제거
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 히스토그램 균등화로 대비를 높임
    equalized = cv2.equalizeHist(blurred)

    # 이진화(Thresholding) 적용하여 대비를 높임
    _, thresholded = cv2.threshold(equalized, 150, 255, cv2.THRESH_BINARY)

    # OpenCV 이미지에서 EasyOCR로 텍스트 추출
    result = reader.readtext(thresholded)
    return result


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


def extract_product_price_from_text(text):
    # 가격을 추출하기 위한 간단한 정규 표현식
    price_data = []
    product = ""
    price = ""

    for line in text:
        text_str = line[1].strip()  # 텍스트 부분
        match = re.search(r'(.+?)\s+(\d{1,3}(?:,\d{3})*(?:₩|원|USD|€))', text_str)

        # 텍스트가 가격을 포함하고 있을 때
        if match:
            if product and price:
                price_data.append({"product": product, "price": price})

            product = match.group(1).strip()
            price = match.group(2).strip()

        # 텍스트가 가격을 포함하지 않으면 상품명으로 취급
        else:
            if not product:
                product = text_str

    # 마지막 남은 상품 추가
    if product and price:
        price_data.append({"product": product, "price": price})

    return price_data


def process_youtube_url_to_text_ocr(url):
    mp4_file = download_video(url)
    print("동영상 다운 완료")

    frames = extract_frames(mp4_file, interval_sec=1.0)
    print(f"{len(frames)}개의 프레임 추출 완료")

    extracted_data = []

    for i, frame in tqdm(enumerate(frames), total=len(frames), desc="프레임 처리 중"):
        text = extract_text_from_frame_easyocr(frame)
        items = extract_product_price_from_text(text)
        if items:
            print(f"{i}번째 프레임에서 상품 발견: {items}")
            extracted_data.extend(items)

    # 동영상 파일 삭제
    os.remove(mp4_file)
    print(f"동영상 파일 {mp4_file} 삭제 완료.")

    return {"results": extracted_data}


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
