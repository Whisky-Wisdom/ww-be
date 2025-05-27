from fastapi import FastAPI, Response
from app.api.v1.router import api_v1_router


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}


app.include_router(api_v1_router)


# todo favicon 추가
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)  # No Content

# 서버 시작 시 메시지 출력
@app.on_event("startup")
async def startup_event():
    print("✅ FastAPI 서버가 준비되었습니다.")