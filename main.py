from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "서버 정상 작동 중!"}

@app.post("/analyze-bodyfat")
def analyze_bodyfat():
    return {"message": "체지방률 분석 기능 미구현"}
