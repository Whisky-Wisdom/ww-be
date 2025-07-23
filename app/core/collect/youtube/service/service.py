import os
import uuid
import yt_dlp
from pydub import AudioSegment
import torch
import whisper

def cleanup_files(mp4_file, audio_file):
    if os.path.exists(mp4_file):
        os.remove(mp4_file)
    if os.path.exists(audio_file):
        os.remove(audio_file)

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

def extract_audio_from_video(mp4_file):
    audio_file = mp4_file.replace('.mp4', '.wav')
    video = AudioSegment.from_file(mp4_file, format="mp4")
    video.export(audio_file, format="wav")
    return audio_file

def transcribe_audio_to_text(audio_file):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("medium", device=device)  # GPU 사용 (cuda)
    result = model.transcribe(audio_file, language='ko')  # GPU에서 FP16 자동 적용
    return result["text"]
