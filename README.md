# Beyond8 Auth API - Backend Service

Hệ thống cung cấp service xác thực (Auth) và hệ thống sinh mã OTP (dạng Stateless OTP Auto-rotate) cho hệ sinh thái khóa học Beyond8.

👉 **Nếu bạn là Frontend Developer**, vui lòng xem hướng dẫn chi tiết về API và luồng tích hợp tại file: **[FE_INTEGRATION_PLAN.md](./FE_INTEGRATION_PLAN.md)**

---

## 1. Kiến trúc hệ thống
Hệ thống được xây dựng bằng thiết kế **Stateless OTP với HMAC time-window**:
- **Không lưu OTP "rác" vào database:** Quá trình hàm `generate_otp()` chạy thuần túy logic HMAC, không tốn bất kỳ operation Write nào xuống DB.
- **Auto-rotate:** Lưu lại `rotate_count` trong database (singleton table `otp_state`). Mỗi lần một tài khoản xác thực mã thành công, biến `rotate_count` tăng một đơn vị lập tức làm thay đổi khóa OTP hiện hành của toàn hệ thống, khiến OTP cũ bị tiêu hủy và trở nên vô nghĩa với những người dùng phía sau.
- **Bảo mật tuyệt đối:** Audit log chỉ luu đúng bản ghi vào bảng `otp_verifications` **DUY NHẤT** khi một phiên kích hoạt thành công (dùng Unique ID trên time-window để chống race conditions / double spend).

## 2. Các tham số Môi trường (.env)

Tạo file `.env` ở root directory:

```env
APP_NAME=Beyond8 Auth Service
API_PREFIX=/api

DATABASE_URL=postgresql+psycopg2://postgres.<ref>:<password>@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres

JWT_SECRET_KEY=replace-with-strong-secret
JWT_ALGORITHM=HS256
COURSE_ACCESS_TOKEN_EXPIRE_DAYS=30

KEY_PREFIX=BY8
OTP_TTL_SECONDS=60
OTP_REFRESH_COOLDOWN_SECONDS=60

CORS_ORIGINS=http://127.0.0.1:5500,http://localhost:5500,http://localhost:3000
```

## 3. Khởi tạo Backend Cục bộ (Local commands)

Hệ thống nên được đưa vào venv để khởi chạy:

```bash
# Nằm trong thư mục gốc dự án
.venv\Scripts\pip.exe install -r requirements.txt
.venv\Scripts\python.exe run_migration.py       # Tự động đẩy DB lên trạng thái mới nhất
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 3636
```
