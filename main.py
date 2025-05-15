from fastapi import FastAPI, Response
from api.v1 import whisky_router


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}


app.include_router(whisky_router, prefix="/api/v1/whiskies")



# todo favicon 추가
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)  # No Content