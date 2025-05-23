import uuid
import yt_dlp


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
