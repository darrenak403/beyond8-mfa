import asyncio
from datetime import datetime, timedelta, timezone

import httpx
import pytest

from app.core import deps
from app.core.config import settings
from app.main import app

REISSUE_PATH = f"{settings.api_prefix}/otp/course-access/reissue"


class _FakeUser:
    def __init__(
        self,
        *,
        course_access_active: bool,
        course_access_period_expires_at,
        course_access_version: int = 3,
        active_session_id: str | None = "session-1",
    ) -> None:
        self.id = "user-1"
        self.email = "u@example.com"
        self.course_access_active = course_access_active
        self.course_access_period_expires_at = course_access_period_expires_at
        self.course_access_version = course_access_version
        self.active_session_id = active_session_id


def _install_override(user: _FakeUser) -> None:
    app.dependency_overrides[deps.get_current_user] = lambda: user


def _clear_overrides() -> None:
    app.dependency_overrides.clear()


async def _post(**kwargs):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        return await ac.post(REISSUE_PATH, **kwargs)


def _run(**kwargs):
    return asyncio.run(_post(**kwargs))


@pytest.fixture(autouse=True)
def _overrides_cleanup():
    yield
    _clear_overrides()


def test_reissue_returns_token_when_course_access_still_active():
    expires_at = datetime.now(timezone.utc) + timedelta(days=10)
    user = _FakeUser(course_access_active=True, course_access_period_expires_at=expires_at)
    _install_override(user)

    response = _run()

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["token"]
    # Không ghi DB / không rotate: version giữ nguyên giá trị của user hiện tại.
    assert user.course_access_version == 3


def test_reissue_rejects_when_period_expired():
    expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    user = _FakeUser(course_access_active=True, course_access_period_expires_at=expires_at)
    _install_override(user)

    response = _run()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "COURSE_ACCESS_EXPIRED"


def test_reissue_rejects_when_no_period_recorded():
    user = _FakeUser(course_access_active=True, course_access_period_expires_at=None)
    _install_override(user)

    response = _run()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "COURSE_ACCESS_EXPIRED"


def test_reissue_rejects_when_course_access_revoked():
    expires_at = datetime.now(timezone.utc) + timedelta(days=10)
    user = _FakeUser(course_access_active=False, course_access_period_expires_at=expires_at)
    _install_override(user)

    response = _run()

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "COURSE_ACCESS_REVOKED"


def test_reissue_requires_valid_auth_token():
    # Không override get_current_user -> phụ thuộc thật chạy, thiếu credentials -> 401.
    response = _run()

    assert response.status_code == 401
