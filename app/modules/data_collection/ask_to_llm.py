from llama_cpp import Llama
from tqdm import tqdm
import os
import json
import re

# LLM 질의 처리 함수
def process_ask_to_llm(text: str) -> str:

    results = process_pipeline(text)
    print("\n✅ 최종 검증된 JSON 결과:")
    for item in results:
        print(json.dumps(item, ensure_ascii=False, indent=2))
    return results


# 모델 경로 설정 (WSL 기준)
model_path = "/mnt/d/models/nous/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf"

# 모델 경로 유효성 검사
if not os.path.exists(model_path):
    raise FileNotFoundError(f"모델 경로가 존재하지 않습니다: {model_path}")

# 모델 초기화
llm = Llama(
    model_path=model_path,
    n_ctx=2048,
    n_threads=6,
    use_mlock=False
)

# 텍스트 청크 분할 함수
def split_text_into_chunks(text: str, max_chars: int = 1000):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


# 단계 1: 오탈자 및 명칭 정규화
def correct_typos(text: str) -> str:
    chunks = split_text_into_chunks(text, max_chars=800)
    corrected_chunks = []
    for chunk in chunks:
        prompt = (
            "다음 텍스트는 위스키 관련 정보야. 오탈자나 잘못된 표기 (위스키 이름이나 브랜드)를 "
            "정확하게 수정해줘. 결과는 순수 텍스트로 출력해줘.\n\n"
            f"```{chunk}```"
        )
        result = llm(prompt, max_tokens=512, stop=["```"])
        corrected_chunks.append(result["choices"][0]["text"].strip())
    return "\n".join(corrected_chunks)


# 단계 2: JSON 추출
def extract_whisky_json(text: str) -> str:
    chunks = split_text_into_chunks(text, max_chars=800)
    json_results = []
    for chunk in chunks:
        prompt = (
            "다음은 정제된 위스키 정보야. 여기에서 위스키 이름_연도포함(name_age), 용량(volume_ml), "
            "가격(price_krw), 날짜(date)를 포함한 JSON 객체들을 추출해줘. "
            "복수 항목이라면 리스트로 출력해줘:\n\n"
            f"```{chunk}```"
        )
        result = llm(prompt, max_tokens=1024, stop=["```"])
        json_results.append(result["choices"][0]["text"].strip())
    return "\n".join(json_results)



# 전체 처리 파이프라인
def process_pipeline(raw_text) :
    # 1단계: 오탈자 교정
    print("📘 1단계: 오탈자 및 명칭 정규화 중...")
    corrected = correct_typos(raw_text)

    # 2단계: JSON 추출
    print("📗 2단계: JSON 추출 중...")
    json_text = extract_whisky_json(corrected)


    return json_text

