from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from auth import models, schemas, utils
import datetime
import re  # 이메일 검증을 위한 정규식

# DB 초기화
init_db()

router = APIRouter()

# OAuth2 기반 JWT 인증
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 이메일 유효성 확인 함수
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

# ✅ 1. 회원가입
@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not is_valid_email(user.email):
        raise HTTPException(status_code=400, detail="유효한 이메일 형식이 아닙니다.")
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="비밀번호는 최소 8자 이상이어야 합니다.")
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    
    hashed_password = utils.hash_password(user.password)
    
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        phone_number=user.phone_number
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ✅ 2. 로그인
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="잘못된 이메일 또는 비밀번호입니다.")
    
    expires = datetime.timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = utils.create_access_token({"sub": user.email}, expires_delta=expires)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": utils.ACCESS_TOKEN_EXPIRE_MINUTES
    }

# ✅ 3. 마이페이지 유저 정보 조회
@router.get("/user/me", response_model=schemas.UserResponse)
def get_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = utils.verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


# ✅ 4. 비밀번호 변경
@router.put("/update-password")
def update_password(new_password: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = utils.verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = utils.hash_password(new_password)
    db.commit()
    return {"message": "비밀번호가 성공적으로 변경되었습니다."}

# ✅ 5. 회원 탈퇴
@router.delete("/delete-account")
def delete_account(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = utils.verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "회원 탈퇴가 완료되었습니다."}

# ✅ 6. 마이페이지 이름/번호 수정
@router.patch("/user/profile", response_model=schemas.UserResponse)
def update_profile(
    update: schemas.UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = utils.verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = update.name
    user.phone_number = update.phone_number
    db.commit()
    db.refresh(user)
    
    return user

# ✅ 7. 비밀번호 변경 (기존 비번 확인)
@router.patch("/user/password")
def change_password(
    passwords: schemas.PasswordUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = utils.verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 기존 비밀번호 검증
    if not utils.verify_password(passwords.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="기존 비밀번호가 일치하지 않습니다.")

    # 새 비밀번호 해싱 후 저장
    user.hashed_password = utils.hash_password(passwords.new_password)
    db.commit()
    
    return {"message": "비밀번호가 변경되었습니다."}
