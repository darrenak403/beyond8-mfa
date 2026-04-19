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

    with pytest.raises(HTTPException) as exc:
        deps.get_current_user(db=fake_db, credentials=credentials)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"
