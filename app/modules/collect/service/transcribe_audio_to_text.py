import torch
import whisper

# 오디오에서 텍스트를 추출 (음성 인식)
def transcribe_audio_to_text(audio_file):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("medium", device=device)  # GPU 사용 (cuda)
    result = model.transcribe(audio_file, language='ko')  # GPU에서 FP16 자동 적용
    return result["text"]