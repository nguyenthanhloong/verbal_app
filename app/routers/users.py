from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserWithRolesOut
from ..dependencies import get_current_user
from ..security import verify_password, get_password_hash

router = APIRouter(
    prefix="/api/users",
    tags=["Trang cá nhân (Người dùng)"]
)

# ---------------------------------------------------------
# 1. LẤY THÔNG TIN CỦA CHÍNH MÌNH (Kèm theo Quyền)
# VueJS sẽ gọi API này ngay sau khi Login thành công
# ---------------------------------------------------------
@router.get("/me", response_model=UserWithRolesOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Trả về thông tin của user đang đăng nhập hiện tại.
    Dữ liệu bao gồm mảng roles và permissions để VueJS vẽ Menu.
    """
    return current_user
