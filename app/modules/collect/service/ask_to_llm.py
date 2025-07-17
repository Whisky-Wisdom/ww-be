# from llama_cpp import Llama
# from tqdm import tqdm
# import os
# import json
#
# # LLM 질의 처리 함수
# def process_ask_to_llm(raw_text: str):
#     print("📘 1단계: 오탈자 및 명칭 정규화 중...")
#     corrected = correct_typos(raw_text)
#     print(corrected)
#
#     # print("📗 2단계: JSON 추출 중...")
#     # json_text = extract_whisky_json(corrected)
#     #
#     # print("\n✅ 최종 검증된 JSON 결과:")
#     # for item in json_text:
#     #     print(json.dumps(item, ensure_ascii=False, indent=2))
#
#     return corrected
#
# # 모델 경로 설정
# model_path = "/mnt/d/models/DevQuasar/allenai.Llama-3.1-Tulu-3-8B-GGUF/allenai.Llama-3.1-Tulu-3-8B.Q4_K_S.gguf"
#
# if not os.path.exists(model_path):
#     raise FileNotFoundError(f"모델 경로가 존재하지 않습니다: {model_path}")
#
# llm = Llama(
#     model_path=model_path,
#     n_ctx=7700,
#     n_threads=6,
#     use_mlock=False,
#     use_mmap=True,
#     keep_in_memory=True
# )
#
# # 텍스트 청크 분할
# def split_text_into_chunks(text: str, max_chars: int = 1000):
#     return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
#
# # 1단계: 오탈자 및 명칭 정규화
# def correct_typos(text: str) -> str:
#     chunks = split_text_into_chunks(text, max_chars=1800)
#     corrected_chunks = []
#     for chunk in tqdm(chunks, desc="🔍 정규화 처리 중"):
#         prompt = (
#             "다음 텍스트는 위스키 관련 정보야. 오탈자나 잘못된 표기 (위스키 이름이나 브랜드)를 "
#             "정확하게 수정해줘. 결과는 순수 텍스트로 출력해줘.\n\n"
#             f"```{chunk}```"
#         )
#         result = llm(
#             prompt,
#             temperature=0.3,
#             top_p=0.95,
#             max_tokens=2048,
#         )
#         corrected_chunks.append(result["choices"][0]["text"].strip())
#
#     return "\n".join(corrected_chunks)
#
# # 2단계: JSON 추출
# def extract_whisky_json(text: str) -> list:
#     chunks = split_text_into_chunks(text, max_chars=1800)
#     json_results = []
#     for chunk in tqdm(chunks, desc="📦 JSON 추출 중"):
#         prompt = (
#             "다음은 정제된 위스키 정보야. 여기에서 위스키 이름_연도포함(name_age), 용량(volume_ml), "
#             "가격(price_krw), 날짜(date)를 포함한 JSON 객체들을 추출해줘. "
#             "복수 항목이라면 리스트로 출력해줘.\n\n"
#             "반드시 JSON 형식으로 출력해줘. 예시는 다음과 같아:\n\n"
#             "[\n"
#             "  {\n"
#             "    \"name_age\": \"Glenfiddich 12\",\n"
#             "    \"volume_ml\": 700,\n"
#             "    \"price_krw\": 65000,\n"
#             "    \"date\": \"2024-05-25\"\n"
#             "  }\n"
#             "]\n\n"
#             f"```{chunk}```"
#         )
#         result = llm(
#             prompt,
#             temperature=0.3,
#             top_p=0.95,
#             max_tokens=2048,
#         )
#         json_results.append(result["choices"][0]["text"].strip())
#
#     # JSON 파싱 (검증 및 변환)
#     parsed_results = []
#     for item in json_results:
#         try:
#             parsed = json.loads(item)
#             if isinstance(parsed, list):
#                 parsed_results.extend(parsed)
#             else:
#                 parsed_results.append(parsed)
#         except json.JSONDecodeError:
#             print("⚠️ JSON 파싱 실패:", item)
#
#     return parsed_results
