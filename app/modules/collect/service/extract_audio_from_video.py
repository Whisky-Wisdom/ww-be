from pydub import AudioSegment


def extract_audio_from_video(mp4_file):
    audio_file = mp4_file.replace('.mp4', '.wav')
    video = AudioSegment.from_file(mp4_file, format="mp4")
    video.export(audio_file, format="wav")
    return audio_file