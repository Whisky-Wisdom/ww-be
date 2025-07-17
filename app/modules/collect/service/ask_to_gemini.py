import google.generativeai as genai
from tqdm import tqdm
import os
import json
from datetime import datetime

# --- Gemini API 키 설정 ---
# 환경 변수에서 API 키를 가져옵니다.
# 'GOOGLE_API_KEY' 환경 변수에 발급받은 Gemini API 키를 설정해야 합니다.
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다. API 키를 설정해주세요.")

genai.configure(api_key=API_KEY)

# 사용할 Gemini 모델 설정
# 'gemini-1.5-flash'는 더 빠르고 비용 효율적이며, 긴 컨텍스트에 적합합니다.
# 더 높은 품질이 필요하다면 'gemini-1.5-pro'를 사용할 수도 있습니다.
MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# --- 텍스트 청크 분할 함수 ---
def split_text_into_chunks(text: str, max_chars: int = 1000):
    """
    텍스트를 최대 문자 수에 따라 청크로 분할합니다.
    Gemini 1.5 Flash는 매우 긴 컨텍스트를 지원하므로, 청크 크기를 늘릴 수 있습니다.
    """
    # Gemini 1.5 Flash는 100만 토큰 컨텍스트를 지원하지만,
    # API 요청 제한 및 효율성을 위해 적절한 크기로 분할하는 것이 좋습니다.
    # 토큰 수를 기준으로 하는 것이 더 정확하지만, 여기서는 문자 수를 기준으로 합니다.
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

# --- 1단계: 오탈자 및 명칭 정규화 ---
def correct_typos_gemini(text: str) -> str:
    """
    Gemini 모델을 사용하여 위스키 관련 텍스트의 오탈자 및 명칭을 정규화합니다.
    실존하는 위스키 명칭으로 변경하도록 프롬프트를 강화했습니다.
    """
    # Gemini 1.5 Flash는 매우 긴 프롬프트도 처리할 수 있으므로, 청크 크기를 더 크게 설정합니다.
    # 대략 1글자 = 0.25 토큰으로 가정하여 10000자 = 약 4000 토큰으로 설정 (여유 있게).
    chunks = split_text_into_chunks(text, max_chars=10000)
    corrected_chunks = []

    print("📘 1단계: 오탈자 및 실존 위스키 명칭 정규화 중...")
    for chunk in tqdm(chunks, desc="🔍 정규화 처리 중"):
        prompt = (
            "당신은 위스키 전문가입니다. 다음 텍스트는 위스키 관련 정보입니다. "
            "텍스트 내의 **오탈자, 비표준 표기, 잘못된 위스키 이름이나 브랜드명**을 "
            "**실존하는 정확한 위스키 명칭(브랜드, 제품명, 숙성 연수 포함)**으로 수정해 주세요. "
            "예를 들어, '글렌핏딕'은 '글렌피딕', '맥켈란 12년 더블케스크'는 '맥캘란 12년 더블 캐스크'와 같이 수정합니다. "
            "수정된 결과는 원문의 문맥과 의미를 유지하며 순수한 텍스트로만 출력해 주세요. "
            "추가적인 설명이나 JSON 형식은 포함하지 마세요.\n\n"
            f"```text\n{chunk}\n```"
        )

        # Gemini 모델 호출
        # generation_config를 사용하여 안정적인 응답을 유도
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.3,  # 창의성 낮추고 일관성 높임
                top_p=0.95,
                max_output_tokens=4096, # 충분히 큰 출력 토큰
            )
        )

        # 응답 텍스트 추출
        corrected_text = response.text.strip()
        if corrected_text: # 빈 응답 방지
            corrected_chunks.append(corrected_text)

    return "\n".join(corrected_chunks)

# --- 2단계: JSON 추출 ---
def extract_whisky_json_gemini(text: str) -> list:
    """
    Gemini 모델을 사용하여 정제된 위스키 텍스트에서 JSON 객체를 추출합니다.
    """
    # JSON 추출을 위한 프롬프트는 청크당 하나의 JSON 객체를 유도하는 것이 좋습니다.
    # 복수 항목일 경우 LLM이 리스트로 반환하도록 가이드합니다.
    chunks = split_text_into_chunks(text, max_chars=8000) # JSON 추출을 위한 큰 청크 사이즈
    json_results = []

    print("📗 2단계: 위스키 정보에서 JSON 추출 중...")
    for chunk in tqdm(chunks, desc="📦 JSON 추출 처리 중"):
        # 현재 날짜 (수집 날짜)를 자동으로 추가
        current_date = datetime.now().strftime("%Y-%m-%d")

        prompt = (
            "다음은 정제된 위스키 정보입니다. 여기에서 **위스키 이름_연도포함(name_age)**, "
            "**용량(volume_ml, 숫자만)**, **가격(price_krw, 숫자만)**을 포함하는 JSON 객체를 추출해 주세요. "
            f"**날짜(date)**는 이 정보를 추출하는 현재 날짜인 '{current_date}'로 고정해 주세요.\n"
            "추출할 항목이 여러 개라면 반드시 JSON 배열(리스트) 형태로 출력해 주세요. "
            "가격과 용량을 찾을 수 없는 경우 해당 필드를 포함하지 마세요. "
            "필요 없는 추가 설명 없이 순수한 JSON 형식만 출력해야 합니다.\n\n"
            "예시 출력 형식:\n"
            "```json\n"
            "[\n"
            "  {\n"
            "    \"name_age\": \"Glenfiddich 12 Year Old\",\n"
            "    \"volume_ml\": 700,\n"
            "    \"price_krw\": 65000,\n"
            "    \"date\": \"2024-07-02\"\n"
            "  },\n"
            "  {\n"
            "    \"name_age\": \"Macallan 18 Year Old\",\n"
            "    \"volume_ml\": 700,\n"
            "    \"price_krw\": 500000,\n"
            "    \"date\": \"2024-07-02\"\n"
            "  }\n"
            "]\n"
            "```\n\n"
            f"```text\n{chunk}\n```"
        )

        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.1,  # JSON 추출은 최대한 정확해야 하므로 온도를 낮춤
                    top_p=0.9,
                    max_output_tokens=4096,
                )
            )

            # 응답 텍스트가 백틱으로 감싸져 있을 수 있으므로 제거
            json_string = response.text.strip()
            if json_string.startswith("```json"):
                json_string = json_string[len("```json"):].strip()
            if json_string.endswith("```"):
                json_string = json_string[:-len("```")].strip()

            if json_string:
                parsed = json.loads(json_string)
                if isinstance(parsed, list):
                    json_results.extend(parsed)
                else: # 단일 객체인 경우 리스트로 변환하여 추가
                    json_results.append(parsed)

        except json.JSONDecodeError as e:
            print(f"⚠️ JSON 파싱 실패 (원본 텍스트 청크): {chunk[:100]}...")
            print(f"⚠️ JSON 파싱 실패 (모델 응답): {response.text}")
            print(f"오류: {e}")
        except Exception as e:
            print(f"API 호출 중 예기치 않은 오류 발생: {e}")

    return json_results

# --- 3단계: SQL INSERT 문 생성 ---
def generate_insert_sql(whisky_data: list) -> list:
    """
    추출된 위스키 JSON 데이터를 기반으로 SQL INSERT 문을 생성합니다.
    """
    sql_statements = []
    # 테이블 이름은 'whisky_info'로 가정합니다. 필요에 따라 변경하세요.
    table_name = "whisky_info"

    for item in whisky_data:
        # 필드 값 준비 (None 값 처리)
        # JSON 파싱 시 필드가 없을 경우 None이 될 수 있으므로, 'get' 메서드를 사용하여 기본값 'NULL' 설정
        name_age = item.get("name_age")
        volume_ml = item.get("volume_ml")
        price_krw = item.get("price_krw")
        date = item.get("date") # 추출된 JSON에 date가 없으면 None

        # SQL 값 형식화
        # 문자열 값은 따옴표로 감싸고, 내부 따옴표는 이스케이프하며, None은 SQL NULL로 처리
# 더 읽기 쉬운 표현식 (동일한 결과)
        name_age_sql = f"'{name_age.replace(\"'\", \"''\")}'" if name_age is not None else "NULL"            
        # 숫자 값은 직접 사용하거나 None인 경우 SQL NULL로 처리
        volume_ml_sql = str(volume_ml) if volume_ml is not None else "NULL"
        price_krw_sql = str(price_krw) if price_krw is not None else "NULL"

        # 날짜 값은 따옴표로 감싸고, None은 SQL NULL로 처리
        date_sql = f"'{date}'" if date is not None else "NULL"

        # INSERT 문 생성
        sql = (
            f"INSERT INTO {table_name} (name_age, volume_ml, price_krw, date) "
            f"VALUES ({name_age_sql}, {volume_ml_sql}, {price_krw_sql}, {date_sql});"
        )
        sql_statements.append(sql)

        # 모든 항목을 처리한 후 리스트를 반환합니다.
    return sql_statements

# --- LLM 질의 처리 메인 함수 ---
def process_ask_to_llm_gemini(raw_text: str):
    """
    주어진 텍스트를 정규화하고, JSON을 추출한 후 SQL INSERT 문을 생성합니다.
    """
    # 1단계: 오탈자 및 명칭 정규화
    corrected_text = correct_typos_gemini(raw_text)
    print("\n✅ 1단계 정규화 결과:")
    print(corrected_text)
    print("-" * 50)

    # 2단계: JSON 추출
    extracted_json = extract_whisky_json_gemini(corrected_text)
    print("\n✅ 2단계 JSON 추출 결과:")
    if extracted_json:
        for item in extracted_json:
            print(json.dumps(item, ensure_ascii=False, indent=2))
    else:
        print("추출된 JSON 데이터가 없습니다.")
    print("-" * 50)

    # 3단계: SQL INSERT 문 생성
    sql_statements = generate_insert_sql(extracted_json)
    print("\n✅ 3단계 SQL INSERT 문:")
    if sql_statements:
        for sql in sql_statements:
            print(sql)
    else:
        print("생성된 SQL INSERT 문이 없습니다.")
    print("-" * 50)

    return sql_statements

# --- 사용 예시 ---
if __name__ == "__main__":
    sample_text = """
    오늘 글랜피딕 12년 더블캐스크 700ml 6만 5천원에 샀다. 날짜는 2024년 5월 25일.
    맥켈란 18년 500ml 50만원에도 팔던데 비싸서 안 샀음.
    발렌타인 21y 700ml 150000원 행사하던데, 2024년 6월 10일자 정보.
    조니워커 블루 750ml 250000원.
    """

    # process_ask_to_llm_gemini 함수를 호출하여 전체 워크플로우 실행
    final_sql_statements = process_ask_to_llm_gemini(sample_text)

    # 필요한 경우 final_sql_statements를 데이터베이스에 실행
    # print("\n--- 최종 SQL INSERT 문 ---")
    # for sql in final_sql_statements:
    #     print(sql)