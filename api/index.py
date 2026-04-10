# py -m uvicorn api.index:app --reload --port 3636
import os
import pyotp
import time
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load config từ file .env (Dành cho chạy local)
load_dotenv()

# Lấy KEY từ môi trường (Vercel), nếu chạy local không có thì dùng giá trị mặc định
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin_key_123")
MASTER_SECRET = os.getenv("MASTER_SECRET", "JBSWY3DPEHPK3PXP")

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
        return {"valid": True, "message": "OTP hợp lệ"}
    return {"valid": False, "message": "OTP đã hết hạn"}

if __name__ == "__main__":
    import uvicorn
    # Chạy ở port 3636 khi test local
    uvicorn.run("api.index:app", host="0.0.0.0", port=3636, reload=True)
