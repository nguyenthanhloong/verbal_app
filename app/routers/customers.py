# app/routers/customers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Customer
from ..schemas import CustomerCreate, CustomerUpdate, CustomerOut

# Thay get_current_user bằng RequirePermission
from ..dependencies import RequirePermission 

router = APIRouter(
    prefix="/api/customers",
    tags=["Quản lý Khách Hàng (Customers)"],
)

@router.post("", response_model=CustomerOut, dependencies=[Depends(RequirePermission("FUNC_CUSTOMER_MGR"))] )
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    # Check trùng mã KH
    db_cus = db.query(Customer).filter(Customer.ma_khach_hang == customer.ma_khach_hang).first()
    if db_cus:
        raise HTTPException(status_code=400, detail="Mã khách hàng đã tồn tại")
    db_phone = db.query(Customer).filter(Customer.sdt == customer.sdt).first()
    if db_phone:
        raise HTTPException(status_code=400, detail="Số điện thoại đã tồn tại")
    
    new_cus = Customer(**customer.model_dump())
    db.add(new_cus)
    db.commit()
    db.refresh(new_cus)
    return new_cus

@router.get("", response_model=List[CustomerOut])
def get_all_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Customer).offset(skip).limit(limit).all()

@router.put("/{customer_id}", response_model=CustomerOut, dependencies=[Depends(RequirePermission("FUNC_CUSTOMER_MGR"))] )
def update_customer(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)):
    cus = db.query(Customer).filter(Customer.id == customer_id).first()
    if not cus:
        raise HTTPException(status_code=404, detail="Không tìm thấy khách hàng")
    
    update_data = payload.model_dump(exclude_unset=True) # Chỉ lấy các trường có gửi lên
    for key, value in update_data.items():
        setattr(cus, key, value)
        
    db.commit()
    db.refresh(cus)
    return cus

@router.delete("/{customer_id}", dependencies=[Depends(RequirePermission("FUNC_CUSTOMER_MGR"))] )
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    cus = db.query(Customer).filter(Customer.id == customer_id).first()
    if not cus:
        raise HTTPException(status_code=404, detail="Không tìm thấy khách hàng")
    
    db.delete(cus)
    db.commit()
    return {"message": "Đã xóa khách hàng thành công"}