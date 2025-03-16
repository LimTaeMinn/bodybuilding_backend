from fastapi import FastAPI
from auth.routes import router as auth_router

app = FastAPI()

# 인증 API 추가
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "서버 정상 작동 중!"}
