from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.core import deps


def test_get_current_user_rejects_course_access_token(monkeypatch) -> None:
    fake_db = Mock()
    monkeypatch.setattr(
        deps,
        "decode_access_token",
        lambda _token: {"sub": "user-1", "role": "course_viewer", "email": "a@example.com"},
    )

    credentials = SimpleNamespace(scheme="Bearer", credentials="token")
    request = SimpleNamespace(cookies={}, headers={})

    with pytest.raises(HTTPException) as exc:
        deps.get_current_user(request=request, db=fake_db, credentials=credentials)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"


def test_get_current_user_seed_admin_ignores_session_rotation(monkeypatch) -> None:
    """admin@gmail.com (seed admin) may stay logged in on multiple devices."""
    fake_db = Mock()
    fake_user = SimpleNamespace(
        id="admin-1",
        is_active=True,
        active_session_id="session-newest",
        email="admin@gmail.com",
    )
    monkeypatch.setattr(
        deps,
        "decode_access_token",
        lambda _token: {"sub": "admin-1", "role": "admin", "email": "admin@gmail.com", "sid": "session-older"},
    )
    monkeypatch.setattr(deps.crud_user, "get_by_id", lambda _db, _id: fake_user)

    request = SimpleNamespace(cookies={"auth_token": "auth-token"}, headers={})
    user = deps.get_current_user(request=request, db=fake_db, credentials=None)
    assert user.id == "admin-1"


def test_get_current_user_accepts_auth_token_cookie(monkeypatch) -> None:
    fake_db = Mock()
    fake_user = SimpleNamespace(id="user-1", is_active=True, active_session_id="session-1")
    monkeypatch.setattr(
        deps,
        "decode_access_token",
        lambda _token: {"sub": "user-1", "role": "user", "email": "a@example.com", "sid": "session-1"},
    )
    monkeypatch.setattr(deps.crud_user, "get_by_id", lambda _db, _id: fake_user)

    credentials = None
    request = SimpleNamespace(cookies={"auth_token": "auth-token"}, headers={})

    user = deps.get_current_user(request=request, db=fake_db, credentials=credentials)
    assert user.id == "user-1"


def test_require_course_access_rejects_mismatched_users() -> None:
    current_user = SimpleNamespace(id="auth-user")
    course_user = SimpleNamespace(id="course-user")

    with pytest.raises(HTTPException) as exc:
        deps.require_course_access(current_user=current_user, course_user=course_user)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid or revoked course access token"


def test_get_current_course_user_accepts_course_header_token(monkeypatch) -> None:
    fake_db = Mock()
    fake_user = SimpleNamespace(
        id="user-1",
        is_active=True,
        course_access_active=True,
        course_access_version=2,
        course_access_revoked_at=None,
    )
    monkeypatch.setattr(
        deps,
        "decode_access_token",
        lambda _token: {"sub": "user-1", "role": "course_viewer", "cav": 2, "iat": 2000},
    )
    monkeypatch.setattr(deps.crud_user, "get_by_id", lambda _db, _id: fake_user)

    request = SimpleNamespace(cookies={}, headers={})
    user = deps.get_current_course_user(request=request, db=fake_db, course_access_token="course-token")
    assert user.id == "user-1"
