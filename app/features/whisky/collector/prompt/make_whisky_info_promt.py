# make_whisky_prompt.py

def make_whisky_prompt(text: str, year: int, month: int, description: str = None) -> str:
    """
     텍스트, 연도, 월, 설명을 받아 위스키 정보 JSON을 추출하는 프롬프트
    """
    desc_text = f"\n설명: {description}" if description else ""

    return f'''
        다음 텍스트는 {year}년 {month}월에 수집된 위스키 관련 정보입니다.{desc_text}
        1. 텍스트 내의 오탈자, 비표준 표기, 잘못된 위스키 이름이나 브랜드명을 실존하는 정확한 위스키 명칭(브랜드, 제품명, 숙성 연수 포함)으로 모두 수정해 주세요.
        2. 아래와 같은 JSON 형식으로 위스키 정보를 추출해 주세요.
        - brand: 브랜드명(한글 또는 영문)
        - name_age: 위스키 이름(연도 포함)
        - volume_ml: 용량(ml, 숫자)
        - location: 판매 장소(마트, 코스트코 등)
        - price_krw: 현재 가격(원, 숫자)
        - date: 수집 날짜(YYYY-MM-DD)
        - price_history: 가격 변동 내역 (예: [{{"year":2023,"month":9,"price":249800}}, {{"year":2023,"month":12,"price":214400}}, ...])
        - price_change: 이번 달 가격 변동폭(원, 숫자, 예: -14600)
        복수 항목이면 리스트로 출력해 주세요.
        반드시 JSON만 출력해 주세요.
        예시:
        [
          {{
            "brand": "William Grant & Sons",
            "name_age": "Glenfiddich 12",
            "volume_ml": 700,
            "location": "이마트",
            "price_krw": 65000,
            "date": "2024-05-25",
            "price_history": [
              {{"year":2023,"month":9,"price":74900}},
              {{"year":2024,"month":5,"price":65000}}
            ],
            "price_change": -9900
          }}
        ]
        ---
        텍스트:
        {text}
'''
