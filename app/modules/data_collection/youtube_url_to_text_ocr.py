# 성능 이슈로 인해 보류 > 나중에 개선하거나 새로운 모댈 기다릴것





# import yt_dlp
# import uuid
# import os
# from tqdm import tqdm
# import cv2
# from PIL import Image
# import torch
# from transformers import VisionEncoderDecoderModel, DonutProcessor
#
#
# # Donut 모델 로드
# processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
# model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
# model.to("cuda" if torch.cuda.is_available() else "cpu")
# model.eval()
#
# device = "cuda" if torch.cuda.is_available() else "cpu"
#
# # 유튜브 영상 다운로드
# def download_video(url):
#     filename = f"{uuid.uuid4()}.mp4"
#     ydl_opts = {
#         'format': 'mp4',
#         'outtmpl': filename,
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
#     return filename
#
# # 프레임 추출
# def extract_frames(video_path, interval_sec=2.0):
#     vidcap = cv2.VideoCapture(video_path)
#     fps = vidcap.get(cv2.CAP_PROP_FPS)
#     interval_frames = int(fps * interval_sec)
#
#     frames = []
#     count = 0
#     success, image = vidcap.read()
#     while success:
#         if count % interval_frames == 0:
#             frames.append(image)
#         success, image = vidcap.read()
#         count += 1
#     vidcap.release()
#     return frames
#
#
# # Donut 모델을 통한 텍스트 추출
# def extract_text_with_donut(frame, save_debug_image=False, debug_filename=None):
#     image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     image_pil = Image.fromarray(image_rgb)
#
#     # 디버그 이미지 저장
#     if save_debug_image and debug_filename:
#         image_pil.save(debug_filename)
#
#     # Donut 모델 입력 준비
#     pixel_values = processor(image_pil, return_tensors="pt").pixel_values.to(device)
#     task_prompt = "<s_cord-v2>"
#     decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt")["input_ids"].to(device)
#
#     # 추론
#     outputs = model.generate(
#         pixel_values,
#         decoder_input_ids=decoder_input_ids,
#         max_length=1024,
#         early_stopping=True,
#         pad_token_id=processor.tokenizer.pad_token_id,
#         eos_token_id=processor.tokenizer.eos_token_id,
#     )
#
#     # 결과 디코딩
#     result = processor.batch_decode(outputs, skip_special_tokens=True)[0]
#     return result
#
#
# # 전체 파이프라인
# def process_youtube_url_to_text_ocr(url):
#     mp4_file = download_video(url)
#     print("동영상 다운 완료")
#
#     frames = extract_frames(mp4_file, interval_sec=2.0)
#     print(f"{len(frames)}개의 프레임 추출 완료")
#
#     extracted_data = []
#
#     for i, frame in tqdm(enumerate(frames), total=len(frames), desc="프레임 처리 중"):
#         try:
#             result = extract_text_with_donut(frame)
#             print(f"\n[{i}번째 프레임 Donut 결과]:\n{result}\n")
#             extracted_data.append(result)
#         except Exception as e:
#             print(f"{i}번째 프레임 처리 실패: {e}")
#
#     os.remove(mp4_file)
#     print(f"동영상 파일 {mp4_file} 삭제 완료.")
#
#     return {"results": extracted_data}
