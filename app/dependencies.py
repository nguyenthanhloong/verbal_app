from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from jose import JWTError, jwt
from .security import SECRET_KEY, ALGORITHM

# Khai báo nơi hệ thống tìm kiếm Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin (Token hỏng hoặc hết hạn)",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Giải mã token để lấy username
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

class RequirePermission:
    def __init__(self, required_code: str):
        self.required_code = required_code

    def __call__(self, current_user: User = Depends(get_current_user)):
        has_perm = False
        for role in current_user.roles:
            for perm in role.permissions:
                # Đặc quyền Super Admin
                if perm.code == "FUNC_ADMIN_ALL":
                    return current_user
                
                # Kiểm tra quyền bình thường
                if perm.code == self.required_code:
                    has_perm = True
                    break
            if has_perm: break
            
        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Bạn cần quyền: {self.required_code}!"
            )
        return current_user