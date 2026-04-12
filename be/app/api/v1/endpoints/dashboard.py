from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.auth import BlockUserRequest, UserItemResponse, UserListResponse
from app.schemas.stats import OTPStatsResponse, OTPVerificationHistoryResponse
from app.services import auth_service, stats_service

router = APIRouter(tags=["Dashboard"])


def _to_user_item_response(user: User) -> UserItemResponse:
    return UserItemResponse(
        id=user.id,
        email=user.email,
        role=user.role_name,
        is_active=user.is_active,
        course_access_active=user.course_access_active,
        course_access_version=user.course_access_version,
        course_access_verified_at=user.course_access_verified_at,
        course_access_revoked_at=user.course_access_revoked_at,
        blocked_at=user.blocked_at,
        blocked_reason=user.blocked_reason,
        blocked_by_user_id=user.blocked_by_user_id,
        last_generated_otp=user.last_generated_otp,
        created_at=user.created_at,
    )


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
    user_items = [_to_user_item_response(user) for user in users]
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
    verified_users, total_key_purchases, total_success = stats_service.get_otp_verification_stats(db)
    response_data = OTPStatsResponse(
        verified_users=verified_users,
        total_key_purchases=total_key_purchases,
        total_successful_verifications=total_success,
    )
    return success_response(data=response_data, message="Lấy thống kê OTP thành công")


@router.get("/otp-verifications/history", response_model=ApiResponse[OTPVerificationHistoryResponse])
def otp_verification_history_dashboard(
    _admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
    user_id: str | None = Query(default=None),
):
    items = stats_service.get_otp_verification_history(db, user_id=user_id)
    response_data = OTPVerificationHistoryResponse(total_users=len(items), items=items)
    return success_response(data=response_data, message="Lấy lịch sử verify OTP thành công")


@router.patch("/users/{user_id}/block", response_model=ApiResponse[UserItemResponse])
@router.patch("/getAllUser/{user_id}/block", response_model=ApiResponse[UserItemResponse])
def block_user_dashboard(
    user_id: str,
    payload: BlockUserRequest,
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    updated_user = auth_service.block_user(
        db,
        user_id=user_id,
        admin_user_id=admin_user.id,
        reason=payload.reason,
    )
    return success_response(data=_to_user_item_response(updated_user), message="Đã khóa người dùng")


@router.patch("/users/{user_id}/unblock", response_model=ApiResponse[UserItemResponse])
@router.patch("/getAllUser/{user_id}/unblock", response_model=ApiResponse[UserItemResponse])
def unblock_user_dashboard(
    user_id: str,
    _admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    updated_user = auth_service.unblock_user(db, user_id=user_id)
    return success_response(data=_to_user_item_response(updated_user), message="Đã mở khóa người dùng")


@router.patch("/users/{user_id}/course-access/revoke", response_model=ApiResponse[UserItemResponse])
@router.patch("/getAllUser/{user_id}/course-access/revoke", response_model=ApiResponse[UserItemResponse])
def revoke_course_access_dashboard(
    user_id: str,
    _admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    updated_user = auth_service.revoke_course_access(db, user_id=user_id)
    return success_response(data=_to_user_item_response(updated_user), message="Đã thu hồi beyond8_course_access")


@router.patch("/users/{user_id}/otp-verified-key/clear", response_model=ApiResponse[UserItemResponse])
@router.patch("/getAllUser/{user_id}/otp-verified-key/clear", response_model=ApiResponse[UserItemResponse])
def clear_verified_otp_key_dashboard(
    user_id: str,
    _admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    updated_user = auth_service.clear_verified_otp_key(db, user_id=user_id)
    return success_response(data=_to_user_item_response(updated_user), message="Đã xóa key OTP đã verify của người dùng")