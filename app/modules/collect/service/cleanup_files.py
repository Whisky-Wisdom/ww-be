import os

# 동영상 및 오디오 파일 삭제
def cleanup_files(mp4_file, audio_file):
    if os.path.exists(mp4_file):
        os.remove(mp4_file)
    if os.path.exists(audio_file):
        os.remove(audio_file)