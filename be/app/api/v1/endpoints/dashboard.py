from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.auth import UserItemResponse, UserListResponse
from app.schemas.stats import OTPStatsResponse
from app.services import auth_service, stats_service

router = APIRouter(tags=["Dashboard"])


def _build_user_list_response(
    db: Session,
    offset: int,
    limit: int,
    search: str | None = None,
) -> UserListResponse:
    users, total_users = auth_service.get_all_users(
        db,
        offset=offset,
        limit=limit,
        search=search,
    )
    user_items = [
        UserItemResponse(
            id=user.id,
            email=user.email,
            role=user.role_name,
            is_active=user.is_active,
            created_at=user.created_at,
        )
        for user in users
    ]
    return UserListResponse(total_users=total_users, offset=offset, limit=limit, users=user_items)


@router.get("/users", response_model=ApiResponse[UserListResponse])
@router.get("/getAllUser", response_model=ApiResponse[UserListResponse])
def get_all_users_dashboard(
    _admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    search: str | None = Query(default=None, max_length=255),
):
    response_data = _build_user_list_response(
        db,
        offset=offset,
        limit=limit,
        search=search,
    )
    return success_response(data=response_data, message="Lấy danh sách người dùng thành công")


@router.get("/otp-verifications", response_model=ApiResponse[OTPStatsResponse])
def otp_verification_stats_dashboard(
    _admin: User = Depends(get_current_admin), db: Session = Depends(get_db)
):
    verified_users, total_success = stats_service.get_otp_verification_stats(db)
    response_data = OTPStatsResponse(
        verified_users=verified_users,
        total_successful_verifications=total_success,
    )
    return success_response(data=response_data, message="Lấy thống kê OTP thành công")