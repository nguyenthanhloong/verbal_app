from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import warehouse, admin, auth, users, inventory
from .database import engine, Base

# (Tuỳ chọn) Tự động tạo bảng nếu chưa có, nhưng bạn đã tạo bằng SQL rồi thì có thể bỏ qua dòng này
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SpeedUp Warehouse API",
    description="Hệ thống API quản lý kho và phân quyền động",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc" 
)

# Cấu hình CORS cho VueJS (Thường chạy ở cổng 5173 hoặc 8080)
origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "*" # Cho phép tất cả (chỉ dùng lúc dev)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nhúng các API Router vào hệ thống
app.include_router(auth.router)      # <--- QUAN TRỌNG: Thêm dòng này để có API Login
app.include_router(users.router)
app.include_router(warehouse.router)
app.include_router(admin.router)
# app.include_router(inventory.router)

@app.get("/", tags=["Health Check"])
def root():
    return {"status": "API normal"}