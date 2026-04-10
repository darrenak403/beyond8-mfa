# Hệ thống Cấp phát OTP 60s

## Cách chạy Backend
1. Mở Terminal và truy cập vào thư mục `backend`:
   ```bash
   cd backend
   ```
2. Cài đặt các thư viện yêu cầu:
   ```bash
   pip install -r requirements.txt
   ```
3. Chạy server (sử dụng port 3636 cho hệ thống thứ 3):
   ```bash
   uvicorn main:app --reload --port 3636
   ```

*Bạn có thể xem API qua Swagger tại:* `http://localhost:3636/docs`

## Cách chạy Frontend Admin
Mở trực tiếp file `frontend_admin/index.html` bằng trình duyệt web. 
Hệ thống Frontend sẽ gọi trực tiếp đến API Backend ở port 3636 một cách tự động.
