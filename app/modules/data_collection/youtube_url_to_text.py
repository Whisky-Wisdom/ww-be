import uuid
import yt_dlp
from pydub import AudioSegment
import os
import whisper
import torch


def process_youtube_url_to_text(url):


    # 동영상 다운로드
    mp4_file, upload_date = download_video(url)
    print("동영상 다운 완료")
    print(f"업로드 날짜: {upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}")

    # 오디오 추출
    audio_file = extract_audio_from_video(mp4_file)
    print("오디오 추출 완료")
    
    # 오디오에서 텍스트 추출
    text = transcribe_audio_to_text(audio_file)

    print("텍스트 추출 완료")

    # 파일 삭제
    cleanup_files(mp4_file, audio_file)
    
    print("파일 삭제 완료")

    return {
        "date": upload_date ,
        "text": text
            }




# 1. datatemp 디렉토리에 유튜브 URL에서 동영상을 다운로드하고 MP4로 저장
def download_video(url):
    filename = f"{uuid.uuid4()}.mp4"
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': filename,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        upload_date = info_dict.get('upload_date', 'unknown')  # 예: '20230519'
    return filename, upload_date

# 2. MP4 파일에서 오디오를 추출
def extract_audio_from_video(mp4_file):
    audio_file = mp4_file.replace('.mp4', '.wav')
    video = AudioSegment.from_file(mp4_file, format="mp4")
    video.export(audio_file, format="wav")
    return audio_file



# 3. 오디오에서 텍스트를 추출 (음성 인식)
def transcribe_audio_to_text(audio_file):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("medium", device=device)  # GPU 사용 (cuda)
    result = model.transcribe(audio_file, language='ko')  # GPU에서 FP16 자동 적용
    return result["text"]


# 4. 동영상 및 오디오 파일 삭제
def cleanup_files(mp4_file, audio_file):
    if os.path.exists(mp4_file):
        os.remove(mp4_file)
    if os.path.exists(audio_file):
        os.remove(audio_file)