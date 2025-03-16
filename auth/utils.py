from passlib.context import CryptContext
from jose import JWTError, jwt
import datetime
import os

# 🔹 보안을 위해 환경 변수에서 SECRET_KEY 불러오기 (없으면 기본값 사용)
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 토큰 유효 시간

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 비밀번호 해싱
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ JWT 토큰 생성 (로그인 성공 시 반환)
def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔹 **추가: JWT 토큰 검증 기능**
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # 토큰 해독
        return payload  # 유효하면 payload 반환
    except JWTError:
        return None  # 유효하지 않은 토큰이면 None 반환
