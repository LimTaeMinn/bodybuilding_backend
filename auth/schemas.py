from pydantic import BaseModel, Field
from datetime import datetime

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

# 사용자 정보 수정용 스키마
class UserUpdate(BaseModel):
    name: str = Field(..., example="홍길순")
    phone_number: str = Field(..., example="010-9876-5432")

# 비밀번호 변경용 스키마
class PasswordUpdate(BaseModel):
    old_password: str = Field(..., example="기존비번123")
    new_password: str = Field(..., example="새로운비번456")

# 전화번호 인증번호 스키마
class PhoneNumberSchema(BaseModel):
    phone_number: str = Field(..., example="010-1234-5678")

class VerificationSchema(BaseModel):
    phone_number: str
    code: str


class FatHistoryCreate(BaseModel):
    fat_rate: str = Field(..., example="10~14 %")
    confidence: float = Field(..., example=98.5)
    recommended_diet: str = Field(..., example="단백질 위주 식단")
    recommended_workout: str = Field(..., example="유산소")
    
class FatHistoryResponse(BaseModel):
    id: int
    fat_rate: str
    confidence: float
    recommended_diet: str
    recommended_workout: str
    created_at: datetime

    class Config:
        orm_mode = True
