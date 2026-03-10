from passlib.context import CryptContext
import bcrypt
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key_neu_quen_dien")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
# BẮT BUỘC PHẢI CÓ int() Ở ĐÂY
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
# Cấu hình sử dụng thuật toán bcrypt
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Băm mật khẩu trước khi lưu vào database (Sử dụng bcrypt gốc)"""
    # Bước 1: Chuyển string thành bytes
    pwd_bytes = password.encode('utf-8')
    # Bước 2: Tạo muối (salt) và băm
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Bước 3: Trả về dạng string để lưu vào MySQL
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu người dùng nhập có khớp với hash trong DB không"""
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # So sánh trực tiếp
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

def create_access_token(data: dict):
    """Tạo JWT Token chứa thông tin username"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt