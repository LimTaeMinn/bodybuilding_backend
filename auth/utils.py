from passlib.context import CryptContext
from jose import JWTError, jwt
import datetime
import os
from dotenv import load_dotenv

# ✅ 환경 변수 로드
load_dotenv()  # .env 파일 로드

# ✅ 보안을 위해 SECRET_KEY를 환경 변수에서 가져오기
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 토큰 유효 시간

# ✅ 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 비밀번호 해싱 함수
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ 비밀번호 검증 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ JWT 토큰 생성 함수 (유효 시간 설정 가능)
def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ JWT 토큰 검증 함수 (이메일 반환)
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email  # 토큰이 유효하면 이메일 반환
    except JWTError:
        return None  # 토큰이 유효하지 않으면 None 반환
