import yt_dlp
import re
import pytesseract  # Tesseract OCR 라이브러리 임포트
import cv2
import uuid
import os
from tqdm import tqdm
from paddleocr import PaddleOCR

import numpy as np

# 편집이 없는 동영상의 경우 (메뉴판 가격이 그대로 나와있는 경우)
def process_youtube_url_to_text_ocr(url):
    mp4_file = download_video(url)
    print("동영상 다운 완료")

    frames = extract_frames(mp4_file, interval_sec=1.0)
    print(f"{len(frames)}개의 프레임 추출 완료")

    extracted_data = []

    if frames:
        cv2.imwrite("first_frame.png", frames[20])  # n 번째 프레임을 저장
    #
    # if frames:
    #     debug_text = extract_text_from_frame(frames[20], save_debug_image=True, debug_filename="frame20_debug.png")
    #     print(f"20번째 프레임 OCR 결과: {debug_text}")

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


ocr_model = PaddleOCR(use_angle_cls=True, lang='korean')  # 'korean'은 한글 + 영어 지원
# 프레임에서 텍스트 추출 (OCR 처리)
def preprocess_image_and_save_steps(image, save_debug_image=False, debug_filename_prefix="debug"):
    # 1. BGR → RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if save_debug_image:
        cv2.imwrite(f"{debug_filename_prefix}_rgb.png", cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR))

    # 2. 그레이스케일 변환
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
    if save_debug_image:
        cv2.imwrite(f"{debug_filename_prefix}_gray.png", gray_image)

    #
    # # 3. 가우시안 블러 (약하게 적용)
    # blurred_image = cv2.GaussianBlur(gray_image, (5,5), 0)
    # if save_debug_image:
    #     cv2.imwrite(f"{debug_filename_prefix}_blurred.png", blurred_image)
    #
    # # 4. 이진화 (강한 이진화 대신 Otsu 이진화 사용)
    # _, thresholded_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # if save_debug_image:
    #     cv2.imwrite(f"{debug_filename_prefix}_thresholded.png", thresholded_image)



    return gray_image

def extract_text_from_frame(frame, save_debug_image=False, debug_filename="debug_frame.png"):
    # BGR → RGB
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 이미지 전처리 및 저장
    preprocessed_image = preprocess_image_and_save_steps(rgb_image, save_debug_image, debug_filename)

    result = ocr_model.ocr(preprocessed_image, cls=True)

    # 결과에서 텍스트만 추출 + 바운딩 박스 시각화용
    extracted_text = []
    for line in result:
        for word_info in line:
            box = word_info[0]  # 바운딩 박스 좌표 (4개의 점)
            text = word_info[1][0]  # 텍스트
            extracted_text.append(text)

            if save_debug_image:
                # 사각형 좌표를 정수로 변환
                box = [(int(x), int(y)) for x, y in box]
                # box는 4개의 점이므로 사각형을 그리기 위해 첫 번째와 세 번째 점 사용
                cv2.rectangle(preprocessed_image, box[0], box[2], (0, 255, 0), 2)
                # 텍스트도 같이 그려줌
                cv2.putText(preprocessed_image, text, box[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    if save_debug_image:
        cv2.imwrite(debug_filename, preprocessed_image)
        print(f"디버그 이미지 저장 완료: {debug_filename}")

    if extracted_text:
        return " ".join(extracted_text)
    return None