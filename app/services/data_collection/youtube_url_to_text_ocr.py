import uuid
import yt_dlp



def process_youtube_url_to_text_ocr(url):


    # 동영상 다운로드
    mp4_file = download_video(url)
    print("동영상 다운 완료")



    text=''

    return {"text": text}



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