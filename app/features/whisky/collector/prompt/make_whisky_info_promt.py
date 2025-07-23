async def correct_typos_with_llm(text: str) -> str:
    """
    LLM을 사용하여 텍스트에서 오탈자를 수정합니다.
    """
    prompt = f"""
    다음 텍스트에서 오탈자, 비표준 표기, 잘못된 위스키 이름이나 브랜드명을 실존하는 정확한 위스키 명칭(브랜드, 제품명, 숙성 연수 포함)으로 수정해 주세요:

    텍스트: "{text}"

    수정된 텍스트만 반환해 주세요.
    """
    return prompt

async def extract_whisky_info_with_llm(text: str, year: int, month: int, description: str) -> str:
    """
    LLM을 사용하여 텍스트에서 위스키 정보를 추출합니다.
    """
    prompt = f"""
    위스키 관련 정보를 추출합니다. 주어진 텍스트에서 위스키와 관련된 모든 정보를 추출하여 실존하는 브랜드명과 제품명으로 수정하고, 오류가 있는 부분을 정정하여 아래의 JSON 형식으로 반환해주세요. 
    텍스트는 {year}년 {month}월에 해당하는 위스키 정보를 포함해야 합니다.

    텍스트: "{text}"

    JSON 형식으로 반환할 때는 다음과 같은 필드를 포함하세요:
    - brand: 위스키의 브랜드명 (정확한 브랜드명으로 수정)
    - name_kr: 제품명 (한국어)
    - name_en: 제품명 (영어)
    - volume: 용량 (ml)
    - abv: 알콜 도수 (%)
    - genre: 장르 (예: 싱글몰트, 블랜디드, 버번 등)
    - description_kr: 제품 설명 (한국어)
    - description_en: 제품 설명 (영어)
    - price_history: 가격 이력 (연도, 월, 가격 포함)
    - tags: 제품 태그 (선택사항)

    **예시 정보는 리턴하면 안 됩니다**. 주어진 텍스트를 기반으로 정확하게 정제하여 반환해주세요.
    """
    return prompt



async def extract_price_history_with_llm(text: str) -> str:
    """
    LLM을 사용하여 위스키 가격 변동 정보를 시기별로 추출합니다.
    """
    prompt = f"""
    주어진 텍스트에서 위스키의 가격 변동을 시기별로 추출하여 가격 이력을 아래와 같은 형식으로 반환해주세요:

    텍스트: "{text}"

    가격 이력 형식:
    - year: 연도
    - month: 월
    - price: 가격 (원)
    
    예시:
    [
        {{ "year": 2025, "month": 10, "price": 199800 }},
        {{ "year": 2024, "month": 12, "price": 189800 }},
        {{ "year": 2023, "month": 11, "price": 179800 }}
    ]
    """
    return prompt