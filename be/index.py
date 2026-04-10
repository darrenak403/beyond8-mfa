# py -m uvicorn be.index:app --reload --port 3636
import os
import pyotp
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
ALLOWED_EMAILS = [e.strip() for e in os.getenv("ALLOWED_EMAILS", "").split(",")] if os.getenv("ALLOWED_EMAILS") else []

class LoginRequest(BaseModel):
    email: str

# pyotp.TOTP obj với interval 60s
totp = pyotp.TOTP(MASTER_SECRET, interval=60)

app = FastAPI(
    title="OTP Manager Service", 
    description="Hệ thống cấp phát OTP 60s",
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
    """API Tạo OTP lấy từ Master Secret (Chỉ dành cho Admin)"""
    otp_code = totp.now()
    time_remaining = 60 - (int(time.time()) % 60)
    return {
        "otp": otp_code,
        "expires_in": int(time_remaining)
    }

@app.post("/api/otp/verify", tags=["OTP"])
def verify_otp(otp: str):
    """API Check OTP (Client/Hệ thống 3 có thể gọi qua Method POST + URL Params)"""
    is_valid = totp.verify(otp)
    if is_valid:
        return {"valid": True, "message": "Chào mừng đến với Beyond8"}
    return {"valid": False, "message": "Liên hệ Admin để cấp lại OTP"}

if __name__ == "__main__":
    import uvicorn
    # Chạy ở port 3636 khi test local
    uvicorn.run("api.index:app", host="0.0.0.0", port=3636, reload=True)
