from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserInfo(BaseModel):
    id: int
    username: str
    full_name: str | None
    
    class Config:
        from_attributes = True

# Schema tạo Quyền (Permission)
class PermissionCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None

# Schema tạo Vai trò (Role)
class RoleCreate(BaseModel):
    code: str
    name: str

# Schema hiển thị thông tin User kèm theo quyền (Để VueJS biết mà vẽ Menu)
class PermissionOut(BaseModel):
    id: int
    code: str
    name: str
    description: str
    
    class Config:
        from_attributes = True

class RoleOut(BaseModel):
    id: int
    code: str
    name: str
    permissions: List[PermissionOut] = []
    
    class Config:
        from_attributes = True

class UserWithRolesOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    roles: List[RoleOut] = []
    
    class Config:
        from_attributes = True

class SyncData(BaseModel):
    ids: List[int]

# Schema Cập nhật Quyền
class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Schema Cập nhật Vai trò
class RoleUpdate(BaseModel):
    name: Optional[str] = None

# Schema Cập nhật Người dùng
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None # Truyền lên nếu muốn đổi mật khẩu mới

# 1. Schema Nhập Kho Mới
class ImportNewCreate(BaseModel):
    serial_moi: str
    ma_kho_spl: str
    ma_san_pham: str
    ma_may: str
    ma_bill: str
    ghi_chu: Optional[str] = None
    pxk_kho_tsb: str
    pxk_vp_tsb:str

# 2. Schema Xuất Kho Mới
class ExportNewCreate(BaseModel):
    serial_moi: str
    nv_giao_hang: str
    ma_kho_spl: str
    bien_so_xe: Optional[str] = None
    ma_bill: str
    ghi_chu: Optional[str] = None
   

# 3. Schema Nhập Kho Cũ (Khách trả)
class ImportOldCreate(BaseModel):
    serial_cu: str
    ma_kho_spl: str
    ma_bill: str
    ghi_chu: Optional[str] = None

# 4. Schema Xuất Kho Cũ (Trả nhà cung cấp)
class ExportOldCreate(BaseModel):
    serial_cu: str
    ma_kho_spl: str
    ma_bill: str
    nv_giao_hang: str
    bien_so_xe: Optional[str] = None
    kho_tra_hang: str
    nguoi_nhan: str
    ghi_chu: Optional[str] = None

class ImportThuongCreate(BaseModel):
    id: int # Định danh thiết bị
    customer_id: int # BẮT BUỘC CÓ
    ma_kho_spl: str
    ten_san_pham: str
    ma_san_pham: str
    so_luong: int
    ghi_chu: Optional[str] = None

class ExportThuongCreate(BaseModel):
    id: int # Định danh thiết bị cần xuất
    ma_kho_spl: str
    customer_id: int # BẮT BUỘC CÓ
    so_luong: int # Số lượng khách muốn xuất (VD: 60)
    nv_giao_hang: str
    bien_so_xe: Optional[str] = None
    ma_bill: str
    ghi_chu: Optional[str] = None
    ma_san_pham: str

class ImportLeCreate(BaseModel):
    id: int
    customer_id: int # BẮT BUỘC CÓ
    ma_kho_spl: str
    ten_san_pham: str
    so_luong: int
    ghi_chu: Optional[str] = None

class ExportLeCreate(BaseModel):
    id: int
    ma_kho_spl: str
    customer_id: int # BẮT BUỘC CÓ
    ten_san_pham: str
    so_luong: int
    nv_giao_hang: str
    bien_so_xe: str
    ma_bill: str
    ghi_chu: Optional[str] = None
    

class TransactionDynamicCreate(BaseModel):
    action_code: str
    
    # Các trường cố định thường xuyên dùng để tìm kiếm
    ma_kho_spl: Optional[str] = None
    ma_bill: Optional[str] = None
    search_key: Optional[str] = None
    so_luong: Optional[int] = 1
    ghi_chu: Optional[str] = None
    
    # Chứa toàn bộ các ô Input động do VueJS đẩy lên
    details: Dict[str, Any] = {}

# Schema cho ViTriKho
class ViTriKhoBase(BaseModel):
    ma_kho: str
    ten_kho: str

class ViTriKhoCreate(ViTriKhoBase):
    pass

class ViTriKhoUpdate(BaseModel):
    ten_kho: str 

class ViTriKhoOut(ViTriKhoBase):
    id: int
    nguoi_tao: Optional[str] = None
    ngay_tao: Optional[datetime] = None

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    ma_khach_hang: str
    ten_khach_hang: str
    sdt: Optional[str] = None
    dia_chi: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    ten_khach_hang: Optional[str] = None
    sdt: Optional[str] = None
    dia_chi: Optional[str] = None

class CustomerOut(CustomerBase):
    id: int
    class Config:
        from_attributes = True




