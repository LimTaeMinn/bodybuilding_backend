from pydantic import BaseModel, Field

# 회원가입 시 받을 데이터
class UserCreate(BaseModel):
    name: str = Field(..., example="홍길동")
    phone_number: str = Field(..., example="010-1234-5678")
    email: str = Field(..., example="example@gmail.com")
    password: str = Field(..., example="securePassword123")

# 로그인 시 받을 데이터 (name, phone_number 필요 없음)
class UserLogin(BaseModel):
    email: str = Field(..., example="example@gmail.com")
    password: str = Field(..., example="securePassword123")

# 프론트로 반환할 유저 정보
class UserResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    email: str

    class Config:
        orm_mode = True
