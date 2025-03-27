import os

import django
from django.db import connections

# Định nghĩa biến môi trường DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Khởi tạo Django
django.setup()

# Lấy danh sách bảng từ database
with connections["default"].cursor() as cursor:
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [row[0] for row in cursor.fetchall()]

# In danh sách bảng
print("\n".join(tables))  # noqa: T201
