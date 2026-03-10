import os
from dotenv import load_dotenv
from app.database import SessionLocal, engine, Base
from app.models import User, Role, Permission
from app.security import get_password_hash # Bắt buộc phải import hàm băm mật khẩu

# Load cấu hình từ file .env
load_dotenv()

def seed_production_data():
    db = SessionLocal()
    try:
        print("Đang chạy kịch bản khởi tạo dữ liệu Production...")

        # 1. TẠO CÁC QUYỀN CỐT LÕI (Giữ nguyên)
        permissions_data = [
            {"code": "FUNC_ADMIN_ALL", "name": "Toàn quyền hệ thống", "description": "Quyền Tối Thượng của Super Admin"},
            {"code": "FUNC_VIP_NHAP_MOI", "name": "VIP - Nhập kho mới", "description": ""},
            {"code": "FUNC_THUONG_NHAP_MOI", "name": "THƯỜNG - Nhập kho mới", "description": ""},
            # Bạn có thể thêm các quyền khác vào đây...
        ]
        
        db_permissions = {}
        for p_data in permissions_data:
            perm = db.query(Permission).filter(Permission.code == p_data["code"]).first()
            if not perm:
                perm = Permission(**p_data)
                db.add(perm)
                db.commit()
                db.refresh(perm)
            db_permissions[p_data["code"]] = perm

        # 2. TẠO CÁC VAI TRÒ MẶC ĐỊNH (Giữ nguyên)
        roles_data = [
            {
                "code": "ROLE_SUPER_ADMIN", 
                "name": "Quản trị viên hệ thống",
                "perms": [db_permissions["FUNC_ADMIN_ALL"]] # Admin All là bài miễn tử, gán 1 cái là đủ
            },
            {
                "code": "ROLE_VIP", 
                "name": "Khách hàng VIP",
                "perms": [db_permissions["FUNC_VIP_NHAP_MOI"]]
            },
            {
                "code": "ROLE_THUONG", 
                "name": "Khách hàng Thường",
                "perms": [db_permissions["FUNC_THUONG_NHAP_MOI"]]
            }
        ]

        db_roles = {}
        for r_data in roles_data:
            role = db.query(Role).filter(Role.code == r_data["code"]).first()
            if not role:
                role = Role(code=r_data["code"], name=r_data["name"])
                role.permissions = r_data["perms"] 
                db.add(role)
                db.commit()
                db.refresh(role)
            db_roles[r_data["code"]] = role

        # 3. TẠO TÀI KHOẢN SUPER ADMIN ĐẦU TIÊN TỪ FILE .ENV
        # Lấy thông tin từ file .env, nếu không có thì gán mặc định (thực tế phải cấu hình file .env)
        admin_username = os.getenv("FIRST_SUPERUSER", "admin")
        admin_password = os.getenv("FIRST_SUPERUSER_PASSWORD", "MatKhauSieuKho123@")

        admin_user = db.query(User).filter(User.username == admin_username).first()
        if not admin_user:
            # Hash mật khẩu ngay tại đây
            hashed_pw = get_password_hash(admin_password)
            
            admin_user = User(
                username=admin_username, 
                password=hashed_pw, # Mật khẩu đã được mã hóa an toàn
                full_name="System Administrator"
            )
            admin_user.roles.append(db_roles["ROLE_SUPER_ADMIN"])
            db.add(admin_user)
            db.commit()
            print(f"✅ Đã khởi tạo thành công tài khoản Quản trị gốc: {admin_username}")
        else:
            print("Tài khoản Quản trị đã tồn tại, bỏ qua bước tạo mới.")

        print("Hoàn tất thiết lập môi trường Production!")

    except Exception as e:
        print(f"❌ Có lỗi nghiêm trọng xảy ra: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_production_data()