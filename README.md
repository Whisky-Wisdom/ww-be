# ww-be


가상환경 설치(3.11 ver 로 만들것!) 이름 바꿀시 깃 이그노어 해주세요 

```bash
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