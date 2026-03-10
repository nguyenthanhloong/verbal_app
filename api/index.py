import sys
import os

# 1. Lấy đường dẫn của thư mục gốc (vercel_deploy) và thêm vào sys.path
# Điều này giúp Python nhìn thấy thư mục "app" nằm bên ngoài
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. Bây giờ thì import bình thường
from app.main import app