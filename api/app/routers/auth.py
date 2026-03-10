from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..security import verify_password, create_access_token

router = APIRouter(tags=["Xác thực (Auth)"])

@router.post("/api/auth/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Tìm user
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # 2. Kiểm tra password đã băm
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai Username hoặc Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Tạo token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}