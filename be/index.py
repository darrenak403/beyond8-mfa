# py -m uvicorn be.index:app --reload --port 3636
import os
import hmac
import hashlib
import time
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load config từ file .env (Dành cho chạy local)
load_dotenv()

# Lấy biến môi trường
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")
MASTER_SECRET = os.getenv("MASTER_SECRET", "")
KEY_PREFIX = os.getenv("KEY_PREFIX", "BY8")
ALLOWED_EMAILS = [e.strip() for e in os.getenv("ALLOWED_EMAILS", "").split(",")] if os.getenv("ALLOWED_EMAILS") else []

class LoginRequest(BaseModel):
    email: str

# Bộ ký tự an toàn: loại bỏ 0/O, 1/I/L để tránh nhầm lẫn khi đọc
SAFE_CHARS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"

def _generate_key_for_bucket(bucket: int) -> str:
    """Sinh license key từ HMAC-SHA256 cho một time bucket cụ thể."""
    h = hmac.new(MASTER_SECRET.encode(), str(bucket).encode(), hashlib.sha256)
    digest = h.digest()
    # Lấy 12 bytes đầu, map sang SAFE_CHARS
    chars = [SAFE_CHARS[b % len(SAFE_CHARS)] for b in digest[:12]]
    key = "".join(chars)
    # Format: PREFIX-XXXX-XXXX-XXXX
    return f"{KEY_PREFIX}-{key[0:4]}-{key[4:8]}-{key[8:12]}"

def generate_license_key() -> tuple[str, int]:
    """Trả về (license_key, seconds_remaining)."""
    bucket = int(time.time()) // 60
    key = _generate_key_for_bucket(bucket)
    time_remaining = 60 - (int(time.time()) % 60)
    return key, int(time_remaining)

def verify_license_key(provided_key: str) -> bool:
    """Kiểm tra key hiện tại hoặc key của bucket trước (grace period ~5s cuối chu kỳ)."""
    current_bucket = int(time.time()) // 60
    for bucket in [current_bucket, current_bucket - 1]:
        if _generate_key_for_bucket(bucket) == provided_key.upper().strip():
            return True
    return False

app = FastAPI(
    title="OTP Manager Service",
    description="Hệ thống cấp phát License Key 60s",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/auth/login", tags=["Auth"])
def login(request: LoginRequest):
    """API xác thực email và trả về Token (Nếu có trong DS)"""
    if request.email in ALLOWED_EMAILS:
        return {"token": ADMIN_TOKEN}
    raise HTTPException(status_code=401, detail="Email không được phép truy cập")

def verify_admin(x_admin_token: str = Header(...)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.get("/api/otp/generate", tags=["OTP"])
def generate_otp(is_admin: bool = Depends(verify_admin)):
    """API Tạo License Key từ Master Secret (Chỉ dành cho Admin)"""
    key, time_remaining = generate_license_key()
    return {
        "otp": key,
        "expires_in": time_remaining
    }

@app.post("/api/otp/verify", tags=["OTP"])
def verify_otp(otp: str):
    """API Check License Key (Client/Hệ thống 3 có thể gọi qua Method POST + URL Params)"""
    is_valid = verify_license_key(otp)
    if is_valid:
        return {"valid": True, "message": "Chào mừng đến với Beyond8"}
    return {"valid": False, "message": "Liên hệ Admin để cấp lại mã truy cập"}

if __name__ == "__main__":
    import uvicorn
    # Chạy ở port 3636 khi test local
    uvicorn.run("be.index:app", host="0.0.0.0", port=3636, reload=True)
