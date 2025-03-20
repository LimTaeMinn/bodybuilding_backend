from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router

app = FastAPI()

# ✅ CORS 설정 추가 (프론트엔드에서 API 요청 가능하게 설정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔹 모든 도메인에서 API 호출 가능 (보안 강화하려면 특정 도메인만 허용)
    allow_credentials=True,
    allow_methods=["*"],   # 🔹 모든 HTTP 메소드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],   # 🔹 모든 HTTP 헤더 허용
)

# ✅ 인증 API 추가
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "서버 정상 작동 중!"}
