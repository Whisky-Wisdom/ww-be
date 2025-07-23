from fastapi import FastAPI, Response
from app.api.v1.router import api_v1_router
from fastapi.middleware.cors import CORSMiddleware
import random
import string
import asyncio
from fastapi import FastAPI

app = FastAPI()

# CORS 미들웨어 설정
origins = [
    "http://localhost:3000",  # Next.js 개발 서버의 기본 Origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # 허용할 Origin 목록
    allow_credentials=True,         # 자격 증명(쿠키, HTTP 인증 등)을 허용할지 여부
    allow_methods=["*"],            # 모든 HTTP 메서드(GET, POST, PUT, DELETE 등) 허용
    allow_headers=["*"],            # 모든 HTTP 헤더 허용
)




@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}




@app.get("/ttest")
async def read_root():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    print( random_string)
    await asyncio.sleep(1)  # 1초 대기
    return {"message": random_string}


app.include_router(api_v1_router)


# todo favicon 추가
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)  # No Content

# 서버 시작 시 메시지 출력
@app.on_event("startup")
async def startup_event():
    print("✅ FastAPI 서버가 준비되었습니다. http://127.0.0.1:1855/")