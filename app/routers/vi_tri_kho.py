from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import ViTriKho, User
from ..schemas import ViTriKhoCreate, ViTriKhoUpdate, ViTriKhoOut
from ..dependencies import RequirePermission

router = APIRouter(
    prefix="/api/vi-tri-kho",
    tags=["Quản lý Vị Trí Kho"],
)

@router.post("", response_model=ViTriKhoOut, dependencies=[Depends(RequirePermission("FUNC_CUSTOMER_MGR"))] )
def create_vi_tri_kho(
    payload: ViTriKhoCreate, 
    db: Session = Depends(get_db),
    # Lấy thông tin user đang đăng nhập để điền vào cột 'nguoi_tao'
    current_user: User = Depends(RequirePermission("FUNC_CUSTOMER_MGR")) 
):
    # Kiểm tra xem mã kho đã tồn tại chưa
    db_kho = db.query(ViTriKho).filter(ViTriKho.ma_kho == payload.ma_kho).first()
    if db_kho:
        raise HTTPException(status_code=400, detail="Mã kho này đã tồn tại")
    
    new_kho = ViTriKho(
        ma_kho=payload.ma_kho,
        ten_kho=payload.ten_kho,
        nguoi_tao=current_user.username
    )
    db.add(new_kho)
    db.commit()
    db.refresh(new_kho)
    return new_kho

@router.get("", response_model=List[ViTriKhoOut])
def get_all_vi_tri_kho(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(ViTriKho).offset(skip).limit(limit).all()

@router.get("/{kho_id}", response_model=ViTriKhoOut)
def get_vi_tri_kho_by_id(kho_id: int, db: Session = Depends(get_db)):
    kho = db.query(ViTriKho).filter(ViTriKho.id == kho_id).first()
    if not kho:
        raise HTTPException(status_code=404, detail="Không tìm thấy Vị trí kho")
    return kho

@router.put("/{kho_id}", response_model=ViTriKhoOut, dependencies=[Depends(RequirePermission("FUNC_CUSTOMER_MGR"))])
def update_vi_tri_kho(kho_id: int, payload: ViTriKhoUpdate, db: Session = Depends(get_db)):
    kho = db.query(ViTriKho).filter(ViTriKho.id == kho_id).first()
    if not kho:
        raise HTTPException(status_code=404, detail="Không tìm thấy Vị trí kho")
    
    # Chỉ cập nhật duy nhất Tên kho
    kho.ten_kho = payload.ten_kho
        
    db.commit()
    db.refresh(kho)
    return kho

@router.delete("/{kho_id}", dependencies=[Depends(RequirePermission("FUNC_CUSTOMER_MGR"))])
def delete_vi_tri_kho(kho_id: int, db: Session = Depends(get_db)):
    kho = db.query(ViTriKho).filter(ViTriKho.id == kho_id).first()
    if not kho:
        raise HTTPException(status_code=404, detail="Không tìm thấy Vị trí kho")
    
    db.delete(kho)
    db.commit()
    return {"message": "Đã xóa Vị trí kho thành công"}