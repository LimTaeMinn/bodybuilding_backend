from fastapi import FastAPI

app = FastAPI()  # FastAPI 앱 객체 생성

@app.get("/")
def read_root():
    return {"message": "Hello, Backend!"}
