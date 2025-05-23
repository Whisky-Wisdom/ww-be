# ww-be


가상환경 설치(3.11 ver 로 만들것!) 이름 바꿀시 깃 이그노어 해주세요 

```bash
sudo apt update
sudo apt install python3.11


python3.11 -m venv venv
```

가상 환경 실행
```bash
source venv/bin/activate
```
pip install -r requirements.txt



1855 포트로 실행

```bash
uvicorn app.main:app --reload --port 1855
```



```
app/
├── main.py                  # FastAPI 앱 실행 엔트리포인트
├── core/                    # 전역 설정 및 공통 유틸
│   ├── config.py            # 환경변수 및 설정
│   ├── logging.py           # 로깅 설정
│   ├── security.py          # 인증/인가 관련 로직
│   └── dependencies.py      # 공통 종속성 주입
├── common/                  # 전역적으로 사용하는 유틸/에러/응답 모델
│   ├── exceptions.py        # 커스텀 예외
│   ├── schemas.py           # 공통 Pydantic 스키마
│   └── utils.py             # 범용 유틸 함수
├── api/                     # 엔드포인트 라우터 구성
│   ├── v1/                  # API 버저닝
│   │   ├── __init__.py
│   │   ├── user.py          # 각 도메인 라우터
│   │   └── post.py
│   └── dependencies.py      # API 단 전용 의존성
├── modules/                 # 도메인별 모듈 (FSD 구조와 매칭)
│   ├── user/
│   │   ├── models.py        # SQLAlchemy 모델
│   │   ├── schemas.py       # Pydantic 스키마
│   │   ├── service.py       # 비즈니스 로직
│   │   ├── repository.py    # DB 접근
│   │   └── router.py        # FastAPI 라우터 (api/v1/user.py에서 include)
│   ├── post/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   └── router.py
├── db/                      # DB 관련 초기 설정 및 세션 관리
│   ├── base.py              # BaseModel 메타 설정
│   ├── session.py           # DB 세션 생성기
│   └── migrations/          # Alembic 마이그레이션
├── tests/                   # 단위/통합 테스트
│   ├── conftest.py
│   ├── test_user.py
│   └── test_post.py
└── requirements.txt         # 의존성 정의




```




MongoDB는 가격 변동 추적, 실시간 데이터 수집, 유저 리뷰, 빠른 검색 등 다양한 요구 사항에 매우 적합합니다. 수평 확장성이 뛰어나고, 비정형 데이터 처리에 유리합니다. 따라서 이 서비스에는 MongoDB가 가장 적합한 데이터베이스


