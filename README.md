# Beyond8 Auth — Hệ thống Cấp phát OTP

Dịch vụ xác thực nội bộ dựa trên **TOTP (Time-based One-Time Password)** với chu kỳ 60 giây. Admin đăng nhập bằng email, lấy mã OTP và chia sẻ cho người dùng để xác minh quyền truy cập. Hệ thống _không sử dụng database_, hoàn toàn stateless và được triển khai trên **Vercel**.

---

## Cấu trúc thư mục

```
learning_source_auth/
├── be/
│   └── index.py          # FastAPI backend — API sinh và xác thực OTP
├── fe/
│   └── index.html        # Frontend Admin — giao diện đăng nhập & hiển thị OTP
├── public/
│   └── logo.png          # Logo thương hiệu
├── .env                  # Biến môi trường (local only, không commit)
├── .gitignore
├── requirements.txt      # Thư viện Python
└── vercel.json           # Cấu hình routing Vercel
```

---

## Yêu cầu hệ thống

- Python `>= 3.9`
- pip

---

## Cài đặt & Chạy Local

### 1. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 2. Tạo file `.env`

Tạo file `.env` ở thư mục gốc (hoặc sao chép từ `.env.example` nếu có):

```env
ADMIN_TOKEN=your_secret_admin_token
MASTER_SECRET=your_base32_totp_secret
ALLOWED_EMAILS=admin1@example.com,admin2@example.com
```

| Biến              | Mô tả                                                                 |
|-------------------|-----------------------------------------------------------------------|
| `ADMIN_TOKEN`     | Token bí mật dùng để xác thực các API call từ Frontend               |
| `MASTER_SECRET`   | Chuỗi Base32 dùng làm seed cho thuật toán TOTP (dùng chung 1 secret) |
| `ALLOWED_EMAILS`  | Danh sách email được phép đăng nhập, phân cách bằng dấu phẩy         |

> ⚠️ **Không commit file `.env` lên Git.** File này đã được thêm vào `.gitignore`.

### 3. Khởi động Backend

```bash
py -m uvicorn be.index:app --reload --port 3636
```

Swagger UI có thể xem tại: `http://localhost:3636/api/docs`

### 4. Mở Frontend

Mở trực tiếp file `fe/index.html` bằng trình duyệt.  
Frontend sẽ tự động phát hiện môi trường local và gọi API tại `http://127.0.0.1:3636`.

---

## API Endpoints

| Method | Endpoint              | Auth Required      | Mô tả                              |
|--------|-----------------------|--------------------|------------------------------------|
| `POST` | `/api/auth/login`     | Không              | Xác thực email, trả về Admin Token |
| `GET`  | `/api/otp/generate`   | `x-admin-token`    | Sinh mã OTP hiện tại + thời gian còn lại |
| `POST` | `/api/otp/verify`     | Không              | Kiểm tra tính hợp lệ của một mã OTP |

### Ví dụ — Sinh OTP

```bash
curl -X GET http://localhost:3636/api/otp/generate \
  -H "x-admin-token: your_secret_admin_token"
```

**Response:**
```json
{
  "otp": "482931",
  "expires_in": 43
}
```

### Ví dụ — Xác thực OTP

```bash
curl -X POST "http://localhost:3636/api/otp/verify?otp=482931"
```

**Response:**
```json
{
  "valid": true,
  "message": "Chào mừng đến với Beyond8"
}
```

---

## Deploy lên Vercel

### Bước 1 — Cấu hình biến môi trường trên Vercel

Vào **Vercel Dashboard → Project → Settings → Environment Variables** và thêm:

```
ADMIN_TOKEN      = <giá trị bí mật>
MASTER_SECRET    = <chuỗi Base32>
ALLOWED_EMAILS   = email1@example.com,email2@example.com
```

### Bước 2 — Deploy

```bash
vercel --prod
```

Hoặc kết nối repo GitHub để Vercel tự động deploy khi push lên `main`.

### Routing sau khi deploy

| URL                        | Đích                    |
|----------------------------|-------------------------|
| `/`                        | `fe/index.html`         |
| `/login`                   | `fe/index.html`         |
| `/admin/key`               | `fe/index.html`         |
| `/api/*`                   | `be/index.py` (FastAPI) |

---

## Luồng hoạt động

```
[Admin]
  │
  ├─ Nhập email → POST /api/auth/login
  │       └─ Nhận admin_token → Lưu vào Cookie (30 ngày)
  │
  └─ GET /api/otp/generate (kèm x-admin-token)
          └─ Hiển thị OTP 6 số + Countdown 60s
                  │
                  └─ Chia sẻ OTP cho [Khách hàng / Hệ thống 3]
                              │
                              └─ POST /api/otp/verify?otp=XXXXXX
                                      └─ Kết quả: valid / invalid
```

---

## Thư viện sử dụng

| Thư viện         | Phiên bản  | Mục đích                         |
|------------------|------------|----------------------------------|
| `fastapi`        | 0.110.0    | Web framework API                |
| `uvicorn`        | 0.29.0     | ASGI server                      |
| `pyotp`          | 2.9.0      | Tạo và xác thực mã TOTP          |
| `python-dotenv`  | 1.0.1      | Đọc biến môi trường từ `.env`    |
