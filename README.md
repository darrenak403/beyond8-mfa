# Beyond8 Auth API - Tài liệu Flow Mới Cho FE

Tài liệu này mô tả contract mới giữa backend và frontend để team FE implement.

## 1. Mục tiêu flow mới

- Chỉ có 1 backend auth/otp dùng chung.
- Trang admin dùng để login và lấy OTP hiện hành.
- Hệ thống FE học viên gọi verify OTP để nhận token truy cập khóa học.
- OTP là one-time-use: verify thành công thì OTP cũ bị consume, OTP mới được tạo ngay.
- Không còn `course_key`, không còn `x-admin-token`, không còn API legacy kiểu query OTP cũ.

## 2. Base URL

- Local: `http://127.0.0.1:3636`
- API prefix: `/api`
- Swagger: `http://127.0.0.1:3636/api/docs`

## 3. Chuẩn response chung

Tất cả endpoint trả theo envelope:

```json
{
  "success": true,
  "data": {},
  "message": "Success",
  "code": 200
}
```

Lưu ý cho FE:

- `success` phản ánh mức HTTP xử lý request.
- Với verify OTP, trạng thái đúng/sai OTP nằm ở `data.valid`.

## 4. Flow A - Admin FE

### Bước A1: Login admin

Endpoint:

- `POST /api/auth/login`
- `POST /api/auth/signin` (alias)

Body:

```json
{
  "email": "admin@gmail.com"
}
```

Response thành công:

```json
{
  "success": true,
  "data": {
    "access_token": "<jwt_admin>",
    "token_type": "bearer",
    "role": "admin",
    "email": "admin@gmail.com"
  },
  "message": "Đăng nhập thành công",
  "code": 200
}
```

Lỗi thường gặp:

- `401`: email không có quyền admin.
- `422`: body sai format email.

### Bước A2: Lấy OTP hiện hành

Endpoint:

- `GET /api/otp/generate`

Header bắt buộc:

- `Authorization: Bearer <jwt_admin>`

Response:

```json
{
  "success": true,
  "data": {
    "otp": "BY8-ABCD-EFGH-JKLM",
    "expires_in": 60,
    "version": 12
  },
  "message": "Lấy OTP thành công",
  "code": 200
}
```

Lỗi thường gặp:

- `401`: thiếu token hoặc token không hợp lệ.
- `403`: token không phải admin.

## 5. Flow B - FE học viên (external system)

### Bước B1: Verify OTP để lấy token học

Endpoint:

- `POST /api/otp/verify`

Body:

```json
{
  "email": "student@example.com",
  "otp": "BY8-ABCD-EFGH-JKLM"
}
```

Trường hợp OTP đúng:

```json
{
  "success": true,
  "data": {
    "valid": true,
    "message": "Xác minh thành công. OTP đã được làm mới ngay lập tức.",
    "next_otp_expires_in": 60,
    "token": "<jwt_course_access_30d>"
  },
  "message": "Xác minh OTP thành công",
  "code": 200
}
```

Trường hợp OTP sai hoặc hết hạn:

```json
{
  "success": true,
  "data": {
    "valid": false,
    "message": "OTP không hợp lệ",
    "next_otp_expires_in": null,
    "token": null
  },
  "message": "OTP không hợp lệ",
  "code": 200
}
```

Lưu ý quan trọng cho FE học viên:

- Không kiểm tra thành công chỉ bằng HTTP 200.
- Bắt buộc kiểm tra `data.valid === true` rồi mới dùng `data.token`.
- Token từ verify có TTL 30 ngày.

## 6. Stats cho dashboard admin

Endpoint:

- `GET /api/stats/otp-verifications`

Header:

- `Authorization: Bearer <jwt_admin>`

Response:

```json
{
  "success": true,
  "data": {
    "verified_users": 15,
    "total_successful_verifications": 42
  },
  "message": "Lấy thống kê OTP thành công",
  "code": 200
}
```

## 7. CORS và tích hợp local

Đảm bảo domain FE nằm trong `CORS_ORIGINS` của backend.

Ví dụ local:

- `http://127.0.0.1:5500`
- `http://localhost:5500`
- `http://localhost:3000`

## 8. Biến môi trường backend

Tạo `.env` ở root:

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

## 9. Chạy backend nhanh

```bash
C:/Users/ACER/AppData/Local/Python/bin/python3.14.exe -m pip install -r requirements.txt
C:/Users/ACER/AppData/Local/Python/bin/python3.14.exe -m alembic upgrade head
C:/Users/ACER/AppData/Local/Python/bin/python3.14.exe -m uvicorn app.main:app --host 127.0.0.1 --port 3636
```

Nếu bị báo cổng 3636 đang dùng, tắt tiến trình cũ hoặc đổi sang cổng khác (ví dụ 3637).

## 10. Checklist FE implement

Admin FE:

- Gọi login bằng email admin.
- Lưu `data.access_token` (cookie hoặc storage theo chính sách FE).
- Gọi generate OTP với Bearer token.
- Nếu API trả 401/403 thì logout và quay về màn hình login.

FE học viên:

- Gọi verify với `{email, otp}`.
- Nếu `data.valid === true`, lưu `data.token` vào key FE mong muốn (ví dụ `beyond-course-access`).
- Nếu `data.valid === false`, hiển thị `data.message` cho người dùng nhập lại OTP.
