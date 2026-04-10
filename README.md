# Beyond8 Auth API - Tài liệu Flow Cho Frontend (Stateless OTP System)

Tài liệu này mô tả kiến trúc mới và luồng hoạt động (flow) giữa backend và frontend để team FE dễ dàng implement. Hệ thống mới sử dụng cơ chế **Stateless OTP với HMAC time-window** để tăng tính bảo mật và tối ưu hóa database.

## 1. Mục tiêu và Cơ chế hoạt động

- **Chỉ có 1 backend auth/otp dùng chung.**
- **OTP Stateless:** Backend không lưu OTP vào database khi generate. OTP được tạo dựa trên thuật toán mã hóa (HMAC) + khung thời gian (time-window).
- **Auto-rotate (Làm mới ngay khi dùng):** Ngay sau khi một user nhập OTP chính xác và lấy token học, OTP đó sẽ **bị vô hiệu hóa hoàn toàn đối với những người khác**. Backend chuyển sang phiên bản OTP mới ngay lập tức.
- **Polling phía Admin:** Vì OTP có thể bị vô hiệu hóa bất kỳ lúc nào bởi user, giao diện Admin FE cầm phải liên tục kiểm tra định kì xem phiên bản của OTP có bị thay đổi không.

## 2. Base URL

- **Local:** `http://127.0.0.1:3636`
- **Sản phẩm (Production):** `https://mfa.beyond8.io.vn/`
- **Swagger Docs:** `http://127.0.0.1:3636/docs`

## 3. Chuẩn response chung

Tất cả endpoint trả về theo chuẩn JSON envelop sau:

```json
{
  "success": true,
  "data": {},
  "message": "Nội dung phản hồi",
  "code": 200
}
```

- `success`: phản ánh việc gọi API thành công hay lỗi logic hệ thống.
- Validation và error cụ thể được mô tả trong `data` hoặc `message`.

---

## 4. Flow A - Giao diện Admin (Cấp phát mã OTP)

Admin app chịu trách nhiệm sinh OTP để chia sẻ (qua màn hình màn hình trình chiếu hoặc đọc cho học viên).

### Bước A1: Login Admin

- **Endpoint:** `POST /api/auth/login` (hoặc `/api/auth/signin`)
- **Body:**
  ```json
  {"email": "admin@gmail.com"}
  ```
- FE cần lưu `data.access_token` vào Cookie với tên **`auth_token`** và dùng làm Bearer token để gọi các API lấy OTP.

### Bước A2: Lấy OTP hiện hành và Polling

- **Endpoint:** `GET /api/otp/generate`
- **Header:** `Authorization: Bearer <jwt_admin>`
- **Response:**
  ```json
  {
    "success": true,
    "data": {
      "otp": "BY8-ABCD-EFGH-JKLM",
      "expires_in": 37,
      "version": 45
    },
    ...
  }
  ```

**[QUAN TRỌNG DÀNH CHO FE ADMIN]:**
Vì đây là stateless OTP và có cơ chế Auto-rotate khi có người dùng, FE cần làm 2 việc song song:

1. **Chạy Progress Bar / Countdown:**
   - Sử dụng giá trị `expires_in` (số giây còn lại của mã). Không được hardcode là 60s, vì tuỳ thời điểm admin mở trang, thời gian `expires_in` có thể từ 1 tới 60.
   - Khi `expires_in` lùi về 0 -> Gọi API `GET /api/otp/generate` lần nữa để làm mới.

2. **Polling định kỳ (5 giây / lần) để theo dõi "version" OTP:**
   - Dùng setInterval 5s gọi API `/api/otp/generate` một cách ngầm (background fetch).
   - Biến `version` (hoặc rotate_count) đại diện cho số hiệu của time-window đó. Nếu user xác nhận thành công mã OTP -> Backend tự tăng version lên.
   - Khi polling nhận về payload, FE so sánh `newPayload.version !== oldPayload.version`:
     - Nếu khác: Nghĩa là OTP cũ đã bị user dùng. FE phải đổi nội dung hiển thị sang OTP mới tương ứng, reset timer với `expires_in` mới, và flash màn hình nhẹ để admin biết mã vừa bị "ăn".

_(Các xử lí này đã có sẵn code mẫu ở file `fe/index.html` trong mã nguồn backend)_.

---

## 5. Flow B - Giao diện FE Khách hàng / Học viên

Đây là giao diện user khách, lấy mã từ Admin và điền vào form để nhận quyền xem khoá học.

### Bước B1: Gửi OTP để Verify

- **Endpoint:** `POST /api/otp/verify`
- **Body:**
  ```json
  {
    "email": "hocvien@example.com",
    "otp": "BY8-ABCD-EFGH-JKLM"
  }
  ```

**Phản hồi thành công (khi OTP đúng và chưa ai dùng):**

```json
{
  "success": true,
  "data": {
    "valid": true,
    "message": "Xác minh thành công. OTP đã được làm mới ngay lập tức.",
    "next_otp_expires_in": 58,
    "token": "<jwt_course_access_30d>"
  },
  "message": "Xác minh OTP thành công"
}
```

_-> FE học viên lưu `token` này vào Cookie với tên **`beyond8_course_access`** (thời gian sống là 1 tháng). Khi user có cookie \`beyond8_course_access\` này thì hệ thống mới cho phép join vào các môn học để học._

**Phản hồi thất bại (khi OTP sai, hoặc OTP ĐÃ BỊ AI ĐÓ DÙNG CHƯỚC ĐÓ VÀI GIÂY):**

```json
{
  "success": true,
  "data": {
    "valid": false,
    "message": "OTP này đã được sử dụng. Vui lòng lấy OTP mới từ admin.",
    "next_otp_expires_in": 55,
    "token": null
  },
  "message": "OTP này đã được sử dụng. Vui lòng lấy OTP mới từ admin."
}
```

_-> FE khách hàng cần kiểm tra cứng `data.valid === true` chứ không phụ thuộc vào `success` của package chung. Sau đó show `data.message` ra toast error._

---

## 6. Commands chuẩn cho quá trình Init

Backend Python chạy port mặc định theo setup môi trường ảo:

```bash
# Nằm trong thư mục gốc dự án
.venv\Scripts\pip.exe install -r requirements.txt
.venv\Scripts\python.exe run_migration.py       # (Hoặc alembic upgrade head nếu biết dùng)
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 3636
```

Cập nhật lại file `.env` nếu chạy local:

```env
CORS_ORIGINS=http://127.0.0.1:5500,http://localhost:5500,http://localhost:3000
```
