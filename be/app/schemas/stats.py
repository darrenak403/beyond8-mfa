from pydantic import BaseModel


class OTPStatsResponse(BaseModel):
    verified_users: int
    total_successful_verifications: int
