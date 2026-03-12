from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from typing import List, Optional # Bổ sung cái này ở đầu file nếu chưa có
from ..models import User, Role, Permission
from ..schemas import RoleCreate, PermissionCreate, UserWithRolesOut, UserCreate, RoleOut, PermissionOut, SyncData, UserUpdate, RoleUpdate, PermissionUpdate
from ..dependencies import RequirePermission, get_current_user
from ..security import get_password_hash

router = APIRouter(
    prefix="/api/admin/rbac",
    tags=["Quản trị Phân quyền (Admin)"],
    dependencies=[Depends(RequirePermission("FUNC_ADMIN_ALL"))] # <--- THÊM DÒNG NÀY
)

# ---------------------------------------------------------
# 1. API TẠO CHỨC NĂNG / QUYỀN MỚI (Permission)
# ---------------------------------------------------------
@router.post("/permissions")
def create_permission(perm: PermissionCreate, db: Session = Depends(get_db)):
    db_perm = db.query(Permission).filter(Permission.code == perm.code).first()
    if db_perm:
        raise HTTPException(status_code=400, detail="Mã Permission đã tồn tại")
    
    new_perm = Permission(code=perm.code, name=perm.name, description=perm.description)
    db.add(new_perm)
    db.commit()
    db.refresh(new_perm)
    return {"message": "Tạo Permission thành công", "data": new_perm}

# ---------------------------------------------------------
# 2. API TẠO VAI TRÒ MỚI (Role)
# ---------------------------------------------------------
@router.post("/roles")
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.code == role.code).first()
    if db_role:
        raise HTTPException(status_code=400, detail="Mã Role đã tồn tại")
    
    new_role = Role(code=role.code, name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return {"message": "Tạo Role thành công", "data": new_role}

# ---------------------------------------------------------
# 3. API GÁN QUYỀN VÀO VAI TRÒ (Gán Permission -> Role)
# ---------------------------------------------------------
@router.post("/roles/{role_id}/assign-permission/{permission_id}")
def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    
    if not role or not permission:
        raise HTTPException(status_code=404, detail="Không tìm thấy Role hoặc Permission")
    
    # Kỹ thuật của SQLAlchemy: Chỉ cần append vào list, nó tự động lưu vào bảng trung gian role_permissions
    if permission not in role.permissions:
        role.permissions.append(permission)
        db.commit()
    
    return {"message": f"Đã gán quyền {permission.code} cho Role {role.code}"}

# ---------------------------------------------------------
# 4. API GÁN VAI TRÒ CHO NGƯỜI DÙNG (Gán Role -> User)
# ---------------------------------------------------------
@router.post("/users/{user_id}/assign-role/{role_id}")
def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not user or not role:
        raise HTTPException(status_code=404, detail="Không tìm thấy User hoặc Role")
    
    if role not in user.roles:
        user.roles.append(role)
        db.commit()
        
    return {"message": f"Đã gán Role {role.code} cho User {user.username}"}

# ---------------------------------------------------------
# 5. LẤY THÔNG TIN CỦA USER KÈM THEO CÂY PHÂN QUYỀN
# API này cực kỳ quan trọng để VueJS biết user có quyền gì
# ---------------------------------------------------------
@router.get("/users/{user_id}", response_model=UserWithRolesOut)
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy user")
    return user

# API Gỡ Quyền khỏi Vai trò
@router.delete("/roles/{role_id}/remove-permission/{permission_id}")
def remove_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    
    if not role or not permission:
        raise HTTPException(status_code=404, detail="Không tìm thấy Role hoặc Permission")
    
    if permission in role.permissions:
        role.permissions.remove(permission) # Xóa khỏi danh sách
        db.commit()
    return {"message": f"Đã thu hồi quyền {permission.code} khỏi Role {role.code}"}

# API Gỡ Vai trò khỏi Người dùng
@router.delete("/users/{user_id}/remove-role/{role_id}")
def remove_role_from_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not user or not role:
        raise HTTPException(status_code=404, detail="Không tìm thấy User hoặc Role")
    
    if role in user.roles:
        user.roles.remove(role)
        db.commit()
    return {"message": f"Đã thu hồi Role {role.code} khỏi User {user.username}"}

@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username đã tồn tại")
    
    hashed_pw = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_pw, full_name=user.full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Tạo User thành công", "user_id": new_user.id}

# ---------------------------------------------------------
# 6. LẤY DANH SÁCH TOÀN BỘ VAI TRÒ (Dành cho Dropdown chọn Role)
# ---------------------------------------------------------
@router.get("/roles", response_model=List[RoleOut])
def get_all_roles(db: Session = Depends(get_db)):
    """API này trả về danh sách toàn bộ Role để VueJS vẽ thẻ <select>"""
    roles = db.query(Role).all()
    return roles

# ---------------------------------------------------------
# 7. LẤY DANH SÁCH TOÀN BỘ QUYỀN (Dành cho bảng quản lý Permission)
# ---------------------------------------------------------
@router.get("/permissions", response_model=List[PermissionOut])
def get_all_permissions(db: Session = Depends(get_db)):
    """API này trả về toàn bộ mã Quyền đang có trong hệ thống"""
    permissions = db.query(Permission).all()
    return permissions

@router.get("/users")
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Dùng joinedload để load trước mảng roles, chống N+1 Query
    users = db.query(User).options(joinedload(User.roles)).offset(skip).limit(limit).all()
    total = db.query(User).count()
    
    return {
        "total": total,
        "data": [
            {
                "id": u.id,
                "username": u.username,
                "full_name": u.full_name,
                "roles": [
                    {"id": r.id, "name": r.name, "code": r.code} for r in u.roles
                ] # VueJS sẽ lấy mảng này để in tên Role ra bảng Table
            } for u in users
        ]
    }

@router.put("/roles/{role_id}/permissions")
def sync_permissions_for_role(role_id: int, payload: SyncData, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Không tìm thấy Role")
    
    # CHỐT CHẶN: Bảo vệ Role Super Admin
    if role.code == "ROLE_SUPER_ADMIN":
        admin_perm = db.query(Permission).filter(Permission.code == "FUNC_ADMIN_ALL").first()
        if admin_perm and admin_perm.id not in payload.ids:
            raise HTTPException(status_code=403, detail="Hành động nguy hiểm: Không thể gỡ quyền Tối thượng khỏi Vai trò Quản trị!")

    new_permissions = db.query(Permission).filter(Permission.id.in_(payload.ids)).all()
    role.permissions = new_permissions
    db.commit()
    return {"message": "Đã cập nhật đồng bộ quyền cho Role thành công"}

@router.put("/users/{user_id}/roles")
def sync_roles_for_user(user_id: int, payload: SyncData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy User")
    
    # CHỐT CHẶN: Bảo vệ Tài khoản Admin gốc
    if user.username == "admin": # Hoặc username bạn cấu hình trong .env
        super_role = db.query(Role).filter(Role.code == "ROLE_SUPER_ADMIN").first()
        if super_role and super_role.id not in payload.ids:
            raise HTTPException(status_code=403, detail="Hành động nguy hiểm: Không thể gỡ Vai trò Quản trị khỏi tài khoản gốc!")

    new_roles = db.query(Role).filter(Role.id.in_(payload.ids)).all()
    user.roles = new_roles
    db.commit()
    return {"message": "Đã cập nhật đồng bộ Vai trò cho User thành công"}

# ---------------------------------------------------------
# 11. CẬP NHẬT THÔNG TIN NGƯỜI DÙNG (Đổi tên / Reset Mật khẩu)
# ---------------------------------------------------------
@router.put("/users/{user_id}")
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy User")
    
    if payload.full_name:
        user.full_name = payload.full_name
    if payload.password:
        user.password = get_password_hash(payload.password) # Băm lại pass mới
        
    db.commit()
    db.refresh(user)
    return {"message": "Cập nhật thông tin User thành công", "full_name": user.full_name}

# ---------------------------------------------------------
# 12. CẬP NHẬT TÊN VAI TRÒ
# ---------------------------------------------------------
@router.put("/roles/{role_id}")
def update_role(role_id: int, payload: RoleUpdate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Không tìm thấy Role")
    
    if payload.name:
        role.name = payload.name
        db.commit()
        
    return {"message": "Cập nhật tên Role thành công"}

# ---------------------------------------------------------
# 13. CẬP NHẬT TÊN/MÔ TẢ QUYỀN
# ---------------------------------------------------------
@router.put("/permissions/{permission_id}")
def update_permission(permission_id: int, payload: PermissionUpdate, db: Session = Depends(get_db)):
    perm = db.query(Permission).filter(Permission.id == permission_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Không tìm thấy Permission")
    
    if payload.name:
        perm.name = payload.name
    if payload.description is not None:
        perm.description = payload.description
        
    db.commit()
    return {"message": "Cập nhật Permission thành công"}