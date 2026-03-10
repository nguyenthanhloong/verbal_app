from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import User, TransactionTemplate, InventoryTransaction
from ..schemas import TransactionDynamicCreate
from ..dependencies import get_current_user
import json

router = APIRouter(tags=["Giao Dịch Kho (Dynamic)"])

# ==============================================================================
# HÀM BỔ TRỢ QUYỀN HẠN
# ==============================================================================
def is_admin(user: User) -> bool:
    return any(perm.code == "FUNC_ADMIN_ALL" for role in user.roles for perm in role.permissions)

def get_user_permissions(user: User) -> set:
    perms = set()
    for role in user.roles:
        for p in role.permissions: perms.add(p.code)
    return perms

# ==============================================================================
# TẦNG NGHIỆP VỤ (SERVICES) - CHỨA CÁC LUẬT LỆ KHẮT KHE CỦA KHÁCH HÀNG
# ==============================================================================

def handle_vip_import(db: Session, payload: TransactionDynamicCreate, current_user: User):
    """Kiểm tra khắt khe việc Nhập hàng VIP (Check trùng Serial)"""
    serial = payload.search_key
    
    # Kiểm tra Serial đã tồn tại trong kho (dù là mới hay cũ) chưa?
    existing = db.query(InventoryTransaction).filter(
        InventoryTransaction.action_code.in_(["VIP_IMPORT_NEW", "VIP_IMPORT_OLD"]),
        InventoryTransaction.search_key == serial
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail=f"Lỗi: Số Serial '{serial}' đã tồn tại trong kho!")
    
    # Nếu OK, lưu vào DB
    new_tx = InventoryTransaction(
        action_code=payload.action_code,
        ma_kho_spl=payload.ma_kho_spl,
        ma_bill=payload.ma_bill,
        search_key=serial,
        so_luong=1,
        chi_tiet_phieu=payload.details,
        nv_nhap_lieu=current_user.username
    )
    db.add(new_tx)

def handle_vip_export(db: Session, payload: TransactionDynamicCreate, current_user: User):
    """Kiểm tra khắt khe việc Xuất hàng VIP"""
    serial = payload.search_key
    
    # 1. Phải có trong kho mới cho xuất
    import_record = db.query(InventoryTransaction).filter(
        InventoryTransaction.action_code.in_(["VIP_IMPORT_NEW", "VIP_IMPORT_OLD"]),
        InventoryTransaction.search_key == serial
    ).first()
    
    if not import_record:
        raise HTTPException(status_code=400, detail=f"Lỗi: Không tìm thấy Serial '{serial}' trong kho!")
    
    # 2. Không được xuất lần thứ 2
    export_record = db.query(InventoryTransaction).filter(
        InventoryTransaction.action_code.in_(["VIP_EXPORT_NEW", "VIP_EXPORT_OLD"]),
        InventoryTransaction.search_key == serial
    ).first()
    
    if export_record:
        raise HTTPException(status_code=400, detail=f"Lỗi: Serial '{serial}' đã được xuất đi trước đó rồi!")

    new_tx = InventoryTransaction(
        action_code=payload.action_code,
        ma_kho_spl=payload.ma_kho_spl,
        ma_bill=payload.ma_bill,
        search_key=serial,
        so_luong=1,
        chi_tiet_phieu=payload.details,
        nv_nhap_lieu=current_user.username
    )
    db.add(new_tx)

def handle_fifo_export(db: Session, payload: TransactionDynamicCreate, current_user: User):
    """THUẬT TOÁN FIFO DÙNG CHUNG CHO CẢ KHÁCH THƯỜNG VÀ KHÁCH LẺ"""
    
    # Tự động xác định mã Nhập tương ứng để quét kho
    import_code = "THUONG_IMPORT" if payload.action_code == "THUONG_EXPORT" else "LE_IMPORT"
    search_key = payload.search_key # Là Mã SP (Thường) hoặc Tên SP (Lẻ)
    remaining_qty = payload.so_luong
    
    # 1. Lấy toàn bộ các Lô nhập của sản phẩm này, sắp xếp cũ nhất lên đầu (Bảo mật For Update)
    import_batches = db.query(InventoryTransaction).filter(
        InventoryTransaction.action_code == import_code,
        InventoryTransaction.search_key == search_key
    ).with_for_update().order_by(InventoryTransaction.ngay.asc()).all()
    
    if not import_batches:
        raise HTTPException(status_code=400, detail="Sản phẩm này chưa từng được nhập kho!")
        
    # 2. Tính tổng số lượng ĐÃ XUẤT từ trước đến nay của sản phẩm này
    total_already_exported = db.query(func.coalesce(func.sum(InventoryTransaction.so_luong), 0)).filter(
        InventoryTransaction.action_code == payload.action_code,
        InventoryTransaction.search_key == search_key
    ).scalar()
    
    export_records_to_add = []
    cumulative_import = 0
    
    # 3. Thuật toán trừ lùi FIFO
    for batch in import_batches:
        if remaining_qty <= 0: break
        
        cumulative_import += batch.so_luong
        if total_already_exported >= cumulative_import:
            continue # Lô này đã bị xuất hết từ trước
            
        stock_available = batch.so_luong
        if total_already_exported > (cumulative_import - batch.so_luong):
            stock_available = cumulative_import - total_already_exported
            
        qty_to_deduct = min(remaining_qty, stock_available)
        
        # Bổ sung ngày của lô nhập gốc vào JSON (để lưu vết FIFO)
        details = payload.details.copy()
        details["ngay_nhap_kho"] = batch.ngay.isoformat() if batch.ngay else None

        new_export = InventoryTransaction(
            action_code=payload.action_code,
            ma_kho_spl=batch.ma_kho_spl, # Lấy mã kho của lô cũ xuất ra
            ma_bill=payload.ma_bill,
            search_key=search_key,
            so_luong=qty_to_deduct,
            chi_tiet_phieu=details,
            nv_nhap_lieu=current_user.username
        )
        export_records_to_add.append(new_export)
        
        remaining_qty -= qty_to_deduct
        total_already_exported += qty_to_deduct
        
    # 4. Kiểm tra xem kho có đủ hàng không
    if remaining_qty > 0:
        raise HTTPException(status_code=400, detail=f"Kho không đủ hàng! Cần {payload.so_luong} nhưng kho chỉ còn {payload.so_luong - remaining_qty}.")
        
    db.add_all(export_records_to_add)

def handle_regular_import(db: Session, payload: TransactionDynamicCreate, current_user: User):
    """Nhập kho lô hàng bình thường"""
    new_tx = InventoryTransaction(
        action_code=payload.action_code,
        ma_kho_spl=payload.ma_kho_spl,
        ma_bill=payload.ma_bill,
        search_key=payload.search_key,
        so_luong=payload.so_luong,
        chi_tiet_phieu=payload.details,
        nv_nhap_lieu=current_user.username
    )
    db.add(new_tx)


# ==============================================================================
# API 1: TRẢ VỀ CẤU HÌNH GIAO DIỆN FORM ĐỘNG
# ==============================================================================
@router.get("/api/dynamic-transactions/templates")
def get_allowed_templates(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_perms = get_user_permissions(current_user)
    admin_flag = is_admin(current_user)
    all_templates = db.query(TransactionTemplate).all()
    
    allowed_templates = []
    for tpl in all_templates:
        if admin_flag or tpl.required_permission in user_perms:
            allowed_templates.append({
                "action_code": tpl.action_code,
                "action_name": tpl.action_name,
                "transaction_type": tpl.transaction_type,
                "form_config": tpl.form_config if isinstance(tpl.form_config, list) else json.loads(tpl.form_config or "[]")
            })
    return {"data": allowed_templates}

# ==============================================================================
# API 2: BỘ ĐIỀU PHỐI TẠO PHIẾU (DISPATCHER)
# Tự động tra soát quyền và đẩy vào đúng Thuật toán nghiệp vụ
# ==============================================================================
@router.post("/api/dynamic-transactions")
def create_dynamic_transaction(
    payload: TransactionDynamicCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # 1. Tìm cấu hình & Check quyền
    template = db.query(TransactionTemplate).filter(TransactionTemplate.action_code == payload.action_code).first()
    if not template:
        raise HTTPException(status_code=404, detail="Mã nghiệp vụ không tồn tại!")

    user_perms = get_user_permissions(current_user)
    if not is_admin(current_user) and template.required_permission not in user_perms:
        raise HTTPException(status_code=403, detail="Bạn không có quyền lập loại phiếu này!")

    # ==========================================================
    # 2. CẢNH SÁT GIAO THÔNG (ĐIỀU PHỐI VÀO ĐÚNG THUẬT TOÁN)
    # ==========================================================
    rule = template.logic_rule 
    
    if rule == "VIP_IMPORT":
        handle_vip_import(db, payload, current_user)
        
    elif rule == "VIP_EXPORT":
        handle_vip_export(db, payload, current_user)
        
    elif rule == "FIFO_EXPORT":
        handle_fifo_export(db, payload, current_user)
        
    elif rule == "STANDARD":
        handle_regular_import(db, payload, current_user)
        
    else:
        # Đề phòng lỗi cấu hình
        raise HTTPException(status_code=500, detail=f"Thuật toán {rule} chưa được hỗ trợ!")

    db.commit()
    return {"message": f"Tạo phiếu {template.action_name} thành công!"}