# FE Integration Plan (User Flow + Cookie Strategy)

Tài liệu này mô tả cách frontend tương tác với backend auth/otp một cách ổn định, dễ debug và dễ mở rộng sau này.

## 1. Mục tiêu tích hợp

- Phân biệt rõ token đăng nhập và token course access.
- Quản lý cookie phía FE để UX ổn định.
- Đảm bảo revoke token từ backend có hiệu lực ngay, kể cả khi FE vẫn giữ cookie.

## 2. Token model hiện tại

Backend đang sử dụng 2 JWT:

1. access_token (login token)

- Nhận từ `POST /api/auth/login`.
- Claim chính: `sub`, `role`, `email`, `iat`, `exp`.
- Dùng cho API cần `get_current_user` hoặc `get_current_admin`.

2. beyond8_course_access (course token)

- Nhận từ `POST /api/otp/verify` khi verify OTP thành công.
- Claim chính: `sub`, `role=course_viewer`, `email`, `iat`, `exp`, `course_access_ttl_days`, `course_access_expires_at`, `cav`.
- Dùng cho API cần `get_current_course_user`.
- `cav` là course_access_version để backend revoke ngay lập tức.

## 3. Phân quyền API

### Public (không cần token)

- `POST /api/auth/signup`
- `POST /api/auth/login`

### User đã đăng nhập

- `GET /api/auth/session-status`
- `POST /api/otp/verify`

### Course access token (beyond8_course_access)

- `GET /api/otp/course-access/status`

### Admin only

- `GET /api/otp/generate`
- `GET /api/stats/otp-verifications`
- `GET /api/stats/otp-verifications/history`
- `GET /api/users`
- `PATCH /api/users/{user_id}/block`
- `PATCH /api/users/{user_id}/unblock`
- `PATCH /api/users/{user_id}/course-access/revoke`

## 4. Request / Response mẫu

### 4.1 POST /api/auth/signup

Request:

```json
{
  "email": "user@example.com"
}
```

Response:

```json
{
  "success": true,
  "data": true,
  "message": "Đăng ký thành công",
  "code": 200
}
```

### 4.2 POST /api/auth/login

Request:

```json
{
  "email": "user@example.com"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "role": "user",
    "email": "user@example.com"
  },
  "message": "Đăng nhập thành công",
  "code": 200
}
```

### 4.3 GET /api/auth/session-status

Request:

```http
GET /api/auth/session-status
Authorization: Bearer <auth_token>
```

Response:

```json
{
  "success": true,
  "data": {
    "user_id": "4634bedf-078c-42e8-8947-63bb...",
    "email": "user@example.com",
    "role": "user",
    "is_active": true
  },
  "message": "Phiên đăng nhập hợp lệ",
  "code": 200
}
```

### 4.4 POST /api/otp/verify

Request:

```http
POST /api/otp/verify
Authorization: Bearer <auth_token>
Content-Type: application/json
```

```json
{
  "email": "user@example.com",
  "otp": "BY8-1234-ABCD-EFGH"
}
```

Response khi hợp lệ:

```json
{
  "success": true,
  "data": {
    "valid": true,
    "message": "Xác minh thành công. OTP đã được làm mới ngay lập tức.",
    "next_otp_expires_in": 42,
    "token": "eyJhbGciOiJIUzI1NiIs..."
  },
  "message": "Xác minh OTP thành công",
  "code": 200
}
```

Response khi không hợp lệ:

```json
{
  "success": true,
  "data": {
    "valid": false,
    "message": "OTP không hợp lệ.",
    "next_otp_expires_in": null,
    "token": null
  },
  "message": "OTP không hợp lệ.",
  "code": 200
}
```

### 4.5 GET /api/otp/course-access/status

Request:

```http
GET /api/otp/course-access/status
Authorization: Bearer <beyond8_course_access>
```

Response:

```json
{
  "success": true,
  "data": {
    "active": true,
    "user_id": "4634bedf-078c-42e8-8947-63bb...",
    "email": "user@example.com"
  },
  "message": "Course access token hợp lệ",
  "code": 200
}
```

### 4.6 GET /api/otp/generate

Request:

```http
GET /api/otp/generate
Authorization: Bearer <admin_auth_token>
```

Response:

```json
{
  "success": true,
  "data": {
    "otp": "BY8-1234-ABCD-EFGH",
    "expires_in": 42,
    "version": 15
  },
  "message": "Lấy OTP thành công",
  "code": 200
}
```

### 4.7 GET /api/stats/otp-verifications

Request:

```http
GET /api/stats/otp-verifications
Authorization: Bearer <admin_auth_token>
```

Response:

```json
{
  "success": true,
  "data": {
    "verified_users": 12,
    "total_successful_verifications": 28
  },
  "message": "Lấy thống kê OTP thành công",
  "code": 200
}
```

### 4.8 GET /api/stats/otp-verifications/history

Request:

```http
GET /api/stats/otp-verifications/history?user_id=4634bedf-078c-42e8-8947-63bb...
Authorization: Bearer <admin_auth_token>
```

Response:

```json
{
  "success": true,
  "data": {
    "total_users": 1,
    "items": [
      {
        "user_id": "4634bedf-078c-42e8-8947-63bb...",
        "email": "user@example.com",
        "verification_count": 3,
        "last_verified_at": "2026-04-11T12:16:16.441721+00:00"
      }
    ]
  },
  "message": "Lấy lịch sử verify OTP thành công",
  "code": 200
}
```

### 4.9 GET /api/users

Request:

```http
GET /api/users?offset=0&limit=100&search=user@example.com
Authorization: Bearer <admin_auth_token>
```

Response:

```json
{
  "success": true,
  "data": {
    "total_users": 1,
    "offset": 0,
    "limit": 100,
    "users": [
      {
        "id": "4634bedf-078c-42e8-8947-63bb...",
        "email": "user@example.com",
        "role": "user",
        "is_active": true,
        "blocked_at": null,
        "blocked_reason": null,
        "blocked_by_user_id": null,
        "created_at": "2026-04-11T12:16:16.441721+00:00"
      }
    ]
  },
  "message": "Lấy danh sách người dùng thành công",
  "code": 200
}
```

### 4.10 PATCH /api/users/{user_id}/block

Request:

```http
PATCH /api/users/4634bedf-078c-42e8-8947-63bb.../block
Authorization: Bearer <admin_auth_token>
Content-Type: application/json
```

```json
{
  "reason": "Vi phạm quy định"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "4634bedf-078c-42e8-8947-63bb...",
    "email": "user@example.com",
    "role": "user",
    "is_active": false,
    "blocked_at": "2026-04-11T12:20:00+00:00",
    "blocked_reason": "Vi phạm quy định",
    "blocked_by_user_id": "admin-id-here",
    "created_at": "2026-04-11T12:16:16.441721+00:00"
  },
  "message": "Đã khóa người dùng",
  "code": 200
}
```

### 4.11 PATCH /api/users/{user_id}/unblock

Request:

```http
PATCH /api/users/4634bedf-078c-42e8-8947-63bb.../unblock
Authorization: Bearer <admin_auth_token>
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "4634bedf-078c-42e8-8947-63bb...",
    "email": "user@example.com",
    "role": "user",
    "is_active": true,
    "blocked_at": null,
    "blocked_reason": null,
    "blocked_by_user_id": null,
    "created_at": "2026-04-11T12:16:16.441721+00:00"
  },
  "message": "Đã mở khóa người dùng",
  "code": 200
}
```

### 4.12 PATCH /api/users/{user_id}/course-access/revoke

Request:

```http
PATCH /api/users/4634bedf-078c-42e8-8947-63bb.../course-access/revoke
Authorization: Bearer <admin_auth_token>
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "4634bedf-078c-42e8-8947-63bb...",
    "email": "user@example.com",
    "role": "user",
    "is_active": true,
    "blocked_at": null,
    "blocked_reason": null,
    "blocked_by_user_id": null,
    "created_at": "2026-04-11T12:16:16.441721+00:00"
  },
  "message": "Đã thu hồi beyond8_course_access",
  "code": 200
}
```

### 4.13 Mẫu error response chung

Khi thiếu token, token hết hạn, hoặc bị revoke, backend trả dạng:

```json
{
  "success": false,
  "data": null,
  "message": "Could not validate credentials",
  "code": 401
}
```

## 5. Luồng hoạt động khuyến nghị cho USER

### B1. Login

- FE gọi `POST /api/auth/login` với email.
- Lưu `access_token` vào cookie `auth_token`.

### B2. Verify OTP để mở khóa course

- FE gọi `POST /api/otp/verify` với Bearer `auth_token`.
- Nếu `valid=true` và có `token`, lưu token đó vào cookie `beyond8_course_access`.

### B3. Truy cập nội dung course

- FE dùng `beyond8_course_access` gọi `GET /api/otp/course-access/status` (hoặc các API course khác trong tương lai).
- Nếu 401 -> coi như token hết hạn/bị revoke, xóa cookie và điều hướng về màn hình verify OTP.

## 6. Luồng revoke key (admin)

- Admin gọi `PATCH /api/users/{user_id}/course-access/revoke`.
- Backend tăng `course_access_version` + cập nhật thời điểm revoke.
- Mọi `beyond8_course_access` cũ của user đó lập tức không hợp lệ nữa.
- FE dù có lưu cookie cũ vẫn bị backend trả 401.

## 7. Cookie strategy trên FE

Do backend hiện trả token qua JSON (chưa set-cookie httpOnly), FE đang phải set cookie bằng JS.

### Cookie để dùng

- `auth_token`: login JWT
- `beyond8_course_access`: course JWT

### Option set cookie (nếu dùng document.cookie)

- `Path=/`
- `SameSite=Lax`
- `Secure` (bắt buộc khi deploy HTTPS)
- Đặt `Max-Age` theo `exp` để tránh cookie sống lâu hơn token

Ví dụ helper:

```js
function setTokenCookie(name, token, expUnix) {
  const now = Math.floor(Date.now() / 1000)
  const maxAge = Math.max(0, expUnix - now)
  const secure = location.protocol === 'https:' ? '; Secure' : ''
  document.cookie = `${name}=${encodeURIComponent(token)}; Path=/; Max-Age=${maxAge}; SameSite=Lax${secure}`
}

function clearCookie(name) {
  document.cookie = `${name}=; Path=/; Max-Age=0; SameSite=Lax`
}
```

## 8. Các check bắt buộc trên FE

1. Sau khi decode `beyond8_course_access`, check thời gian:

- Ưu tiên `course_access_expires_at`, fallback `exp`.
- Nếu hết hạn -> xóa cookie ngay, không đợi backend báo lỗi.

2. Trước khi vào trang course:

- Gọi `GET /api/otp/course-access/status`.
- Nếu 401 -> xóa `beyond8_course_access` và chuyển sang luồng verify OTP.

3. Nếu call API bằng course token bị 401:

- Xóa cookie course
- Hiện thông báo: "Key đã hết hạn hoặc đã bị thu hồi. Vui lòng verify OTP lại."

## 9. Khuyến nghị gửi Authorization header

```js
function getCookie(name) {
  const kv = document.cookie.split('; ').find((x) => x.startsWith(`${name}=`))
  return kv ? decodeURIComponent(kv.split('=').slice(1).join('=')) : null
}

async function apiFetch(path, {useCourseToken = false, ...init} = {}) {
  const token = useCourseToken ? getCookie('beyond8_course_access') : getCookie('auth_token')

  const headers = new Headers(init.headers || {})
  if (token) headers.set('Authorization', `Bearer ${token}`)
  headers.set('Content-Type', 'application/json')

  const res = await fetch(path, {...init, headers})

  if (res.status === 401 && useCourseToken) {
    clearCookie('beyond8_course_access')
  }

  return res
}
```

## 10. Lưu ý bảo mật

- Khi nào backend hỗ trợ set-cookie httpOnly, nên chuyển sang httpOnly cho `auth_token` và `beyond8_course_access`.
- Trong giai đoạn hiện tại (cookie do FE set), cần hạn chế XSS:
  - sanitize input
  - không render HTML user-generated trực tiếp
  - bật CSP nếu có thể
- Luôn tin backend là nguồn sự thật cuối cùng: FE chỉ để UX, quyền truy cập phải do backend quyết định.

## 11. Checklist tích hợp nhanh

- Login xong có `auth_token`.
- Verify OTP thành công có `beyond8_course_access`.
- Vào trang course gọi `GET /api/otp/course-access/status` pass.
- Admin revoke -> user gọi lại status nhận 401.
- FE gặp 401 thì xóa cookie course và bắt user verify lại.
