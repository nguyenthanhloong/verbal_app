

import os
import sys

# Lấy đường dẫn tuyệt đối của thư mục 'api' hiện tại
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ép Python phải ưu tiên tìm kiếm code trong thư mục 'api' này trước
sys.path.insert(0, current_dir)

# Bây giờ Python đã nhìn thấy thư mục 'app' nằm ngay cạnh index.py
from app.main import app