from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from auth import models, schemas, utils

# DB 초기화
init_db()

router = APIRouter()

# OAuth2 기반 JWT 인증 (토큰 사용)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# DB 세션 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 1. 회원가입 API
@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    
    hashed_password = utils.hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ✅ 2. 로그인 API (JWT 토큰 발급)
@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="잘못된 이메일 또는 비밀번호입니다.")
    
    # 🔹 JWT 토큰 생성 후 반환
    access_token = utils.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ 3. 현재 로그인된 사용자 정보 반환 API
@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = utils.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {"email": user.email}

# ✅ 4. 비밀번호 변경 API
@router.put("/update-password")
def update_password(email: str, new_password: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = utils.verify_token(token)
    if not payload or payload.get("sub") != email:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = utils.hash_password(new_password)
    db.commit()
    return {"message": "비밀번호가 성공적으로 변경되었습니다."}

# ✅ 5. 회원 탈퇴 API
@router.delete("/delete-account")
def delete_account(email: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = utils.verify_token(token)
    if not payload or payload.get("sub") != email:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "회원 탈퇴가 완료되었습니다."}
