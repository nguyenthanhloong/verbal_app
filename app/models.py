import enum
from sqlalchemy import  Column, BigInteger, Integer, String, ForeignKey, Table, DateTime, Text, Enum, Date
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, date
from sqlalchemy.sql import func

# Bảng trung gian
user_roles = Table('user_roles', Base.metadata,
    Column('user_id', BigInteger, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('role_id', BigInteger, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True)
)

role_permissions = Table('role_permissions', Base.metadata,
    Column('role_id', BigInteger, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True),
    Column('permission_id', BigInteger, ForeignKey('permissions.id', ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    
    # lazy="joined" giúp chống lỗi N+1 Query
    roles = relationship("Role", secondary=user_roles, lazy="joined")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    
    permissions = relationship("Permission", secondary=role_permissions, lazy="joined")

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

class ImportNew(Base):
    __tablename__ = 'import_new'
    id = Column(BigInteger, primary_key=True)
    serial_moi = Column(String(100), primary_key=True)
    ma_kho_spl = Column(String(50))
    ma_san_pham = Column(String(100))
    ma_may = Column(String(100))
    pxk_kho_tsb = Column(String(100))
    pxk_vp_tsb = Column(String(100))
    ma_bill = Column(String(100))
    nv_nhap_lieu = Column(String(100))
    ghi_chu = Column(Text)
    ngay = Column(DateTime, default=datetime.now) # Tự động lấy ngày hiện tại

class ExportNew(Base):
    __tablename__ = 'export_new'
    id = Column(BigInteger, primary_key=True)
    serial_moi = Column(String(100), primary_key=True)
    ma_kho_spl = Column(String(50))
    ma_san_pham = Column(String(100))
    ma_may = Column(String(100))
    nv_giao_hang = Column(String(100))
    bien_so_xe = Column(String(50))
    ma_bill = Column(String(100))
    nv_nhap_lieu = Column(String(100))
    ghi_chu = Column(Text)
    ngay = Column(DateTime, default=datetime.now)
    ngay_nhap_kho = Column(Date) # Sẽ copy từ import_new sang

class ImportOld(Base):
    __tablename__ = 'import_old'
    id = Column(BigInteger, primary_key=True)
    serial_cu = Column(String(100), primary_key=True)
    ma_kho_spl = Column(String(50))
    ma_bill = Column(String(100))
    nv_nhap_lieu = Column(String(100))
    ghi_chu = Column(Text)
    ngay = Column(DateTime, default=datetime.now)

class ExportOld(Base):
    __tablename__ = 'export_old'
    id = Column(BigInteger, primary_key=True)
    serial_cu = Column(String(100), primary_key=True)
    ma_kho_spl = Column(String(50))
    ma_bill = Column(String(100))
    nv_giao_hang = Column(String(100))
    bien_so_xe = Column(String(50))
    kho_tra_hang = Column(String(100))
    nguoi_nhan = Column(String(100))
    nv_nhap_lieu = Column(String(100))
    ghi_chu = Column(Text)
    ngay = Column(DateTime, default=datetime.now)
    ngay_nhap_kho = Column(Date)

class ImportThuong(Base):
    __tablename__ = 'import_thuong'

    record_id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Khóa chính kép: 1 sản phẩm nhập trong 1 ngày tạo thành 1 Lô (Batch)
    id = Column(BigInteger) 
    ngay = Column(DateTime, default=datetime.now)
    
    ma_kho_spl = Column(String(50))
    ten_san_pham = Column(String(255))
    ma_san_pham = Column(String(100))
    so_luong = Column(Integer)
    nv_nhap_lieu = Column(String(100))
    ghi_chu = Column(Text)
    customer_id = Column(BigInteger, ForeignKey("customers.id", ondelete="SET NULL"))
    customer = relationship("Customer") # Tự động lấy chi tiết Khách hàng

class ExportThuong(Base):
    __tablename__ = 'export_thuong'
    # Khóa chính của dòng xuất kho
    record_id = Column(BigInteger, primary_key=True, autoincrement=True) 
    
    id = Column(BigInteger) # ID sản phẩm (Giống hệt bảng Import)
    ma_kho_spl = Column(String(50))
    ten_san_pham = Column(String(255))
    ma_san_pham = Column(String(100))
    so_luong = Column(Integer) # Số lượng xuất thực tế của dòng này
    nv_giao_hang = Column(String(100))
    bien_so_xe = Column(String(50))
    ma_bill = Column(String(100))
    nv_nhap_lieu = Column(String(100))
    ghi_chu = Column(Text)
    
    ngay = Column(DateTime, default=datetime.now)
    ngay_nhap_kho = Column(Date)            # RULE 3: Lưu ngày của lô nhập (Batch Date)
    customer_id = Column(BigInteger, ForeignKey("customers.id", ondelete="SET NULL"))
    customer = relationship("Customer")

class ImportLe(Base):
    __tablename__ = 'import_le'

    # THÊM DÒNG NÀY LÀM KHÓA CHÍNH MỚI
    record_id = Column(BigInteger, primary_key=True, autoincrement=True)

    id = Column(BigInteger) 
    ngay = Column(DateTime, default=datetime.now)
    
    ma_kho_spl = Column(String(50))
    ten_san_pham = Column(String(255))
    # KHÔNG CÓ ma_san_pham
    so_luong = Column(Integer)
    nv_nhap_lieu = Column(String(100))
    ghi_chu = Column(Text)
    customer_id = Column(BigInteger, ForeignKey("customers.id", ondelete="SET NULL"))
    customer = relationship("Customer")

class ExportLe(Base):
    __tablename__ = 'export_le'
    record_id = Column(BigInteger, primary_key=True, autoincrement=True) 
    
    id = Column(BigInteger) 
    ma_kho_spl = Column(String(50))
    ten_san_pham = Column(String(255))
    # KHÔNG CÓ ma_san_pham
    so_luong = Column(Integer) 
    nv_giao_hang = Column(String(100))
    bien_so_xe = Column(String(50))
    ma_bill = Column(String(100))
    nv_nhap_lieu = Column(String(100))
    ghi_chu = Column(Text)
    
    ngay = Column(DateTime, default=datetime.now)
    ngay_nhap_kho = Column(Date)
    customer_id = Column(BigInteger, ForeignKey("customers.id", ondelete="SET NULL"))
    customer = relationship("Customer")

class ViTriKho(Base):
    __tablename__ = "vi_tri_kho"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ma_kho = Column(String(50), unique=True, nullable=False)
    ten_kho = Column(String(255), nullable=False)
    nguoi_tao = Column(String(100))
    ngay_tao = Column(DateTime, server_default=func.now())

class Customer(Base):
    __tablename__ = "customers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ma_khach_hang = Column(String(50), unique=True, nullable=False, index=True)
    ten_khach_hang = Column(String(255), nullable=False)
    sdt = Column(String(20))
    dia_chi = Column(String(500))