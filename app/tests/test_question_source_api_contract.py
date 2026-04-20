"""HTTP contract tests for question-source user APIs (no real DB).

Uses httpx.AsyncClient + ASGITransport because Starlette TestClient can break
on newer httpx (sync Client no longer accepts ``app=`` from TestClient).
"""

import asyncio
from unittest.mock import Mock

import httpx
import pytest
from fastapi import HTTPException, status

from app.api.v1.endpoints import question_sources as qs
from app.core import deps
from app.db.session import get_db
from app.main import app


class _FakeUser:
    id = "00000000-0000-0000-0000-000000000001"
    is_active = True

    @property
    def role_name(self) -> str:
        return "user"


def _install_overrides() -> None:
    def _mock_get_db():
        yield Mock()

    app.dependency_overrides[deps.require_course_access] = lambda: _FakeUser()
    app.dependency_overrides[get_db] = _mock_get_db


def _clear_overrides() -> None:
    app.dependency_overrides.clear()


async def _request(method: str, path: str, **kwargs):
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        return await ac.request(method, path, **kwargs)


def _run(method: str, path: str, **kwargs):
    return asyncio.run(_request(method, path, **kwargs))


@pytest.fixture(autouse=True)
def _overrides_cleanup():
    _install_overrides()
    yield
    _clear_overrides()


def test_get_subjects_empty(monkeypatch):
    monkeypatch.setattr(qs, "service_list_subjects", lambda _db: [])
    response = _run("GET", "/api/v1/subjects")
    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is True
    data = body.get("data")
    assert isinstance(data, dict)
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["limit"] == 10


def test_get_subjects_nonempty(monkeypatch):
    monkeypatch.setattr(
        qs,
        "service_list_subjects",
        lambda _db: [{"slug": "pmg201c", "code": "PMG201C", "hint": "Mon luyen de"}],
    )
    response = _run("GET", "/api/v1/subjects")
    assert response.status_code == 200
    data = response.json().get("data")
    assert isinstance(data, dict)
    assert data["items"][0]["slug"] == "pmg201c"
    assert data["total"] == 1
    assert data["hasNext"] is False


def test_get_decks_ok(monkeypatch):
    def _decks(_db, slug, user_id=None):
        assert slug == "pmg201c"
        assert user_id == _FakeUser.id
        return [
            {
                "deckId": "d1",
                "examCode": "FA-2024-FE",
                "fileName": "PMG201c - FA 2024 - FE.md",
                "questionCount": 2,
                "stats": {
                    "total": 2,
                    "inProgress": 0,
                    "completed": 0,
                    "completionRatePercent": 0,
                },
                "uploadedAt": None,
            }
        ]

    monkeypatch.setattr(qs, "get_subject_decks", _decks)
    response = _run("GET", "/api/v1/subjects/pmg201c/decks")
    assert response.status_code == 200
    assert response.json()["data"]["items"][0]["deckId"] == "d1"
    assert response.json()["data"]["total"] == 1


def test_get_bank_empty(monkeypatch):
    monkeypatch.setattr(qs, "get_subject_bank", lambda _db, _slug: [])
    response = _run("GET", "/api/v1/subjects/pmg201c/bank")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_get_bank_paginated(monkeypatch):
    monkeypatch.setattr(
        qs,
        "get_subject_bank",
        lambda _db, _slug: [
            {"id": 1, "stem": "A", "options": [], "answer": "A"},
            {"id": 2, "stem": "B", "options": [], "answer": "B"},
        ],
    )
    response = _run("GET", "/api/v1/subjects/pmg201c/bank?page=1&limit=1")
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, dict)
    assert len(data["items"]) == 1
    assert data["items"][0]["stem"] == "A"
    assert data["total"] == 2
    assert data["hasNext"] is True


def test_get_deck_questions_ok(monkeypatch):
    monkeypatch.setattr(
        qs,
        "get_deck_questions",
        lambda _db, slug, deck_id: [
            {"id": 1, "stem": "Q1", "options": [{"label": "A", "text": "Yes"}], "answer": "A"},
        ],
    )
    response = _run("GET", "/api/v1/subjects/pmg201c/decks/d1/questions")
    assert response.status_code == 200
    assert response.json()["data"][0]["stem"] == "Q1"


def test_get_deck_questions_paginated_page1_limit1(monkeypatch):
    monkeypatch.setattr(
        qs,
        "get_deck_questions_page",
        lambda _db, slug, deck_id, page, limit: {
            "items": [{"id": 1, "stem": "Q1", "options": [{"label": "A", "text": "Yes"}], "answer": "A"}],
            "page": 1,
            "limit": 1,
            "total": 3,
            "totalPages": 3,
            "hasNext": True,
            "hasPrevious": False,
        },
    )
    response = _run("GET", "/api/v1/subjects/pmg201c/decks/d1/questions?page=1&limit=1")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["data"], dict)
    assert body["data"]["page"] == 1
    assert body["data"]["limit"] == 1
    assert body["data"]["total"] == 3
    assert body["data"]["totalPages"] == 3
    assert body["data"]["hasNext"] is True
    assert body["data"]["hasPrevious"] is False
    assert len(body["data"]["items"]) == 1
    assert body["data"]["items"][0]["id"] == 1
    assert body["data"]["items"][0]["stem"] == "Q1"


def test_get_deck_questions_paginated_page_default_limit(monkeypatch):
    """When `page` is set and `limit` omitted, service receives limit=1."""

    def _page(_db, slug, deck_id, *, page, limit):
        assert page == 2
        assert limit == 1
        return {
            "items": [{"id": 2, "stem": "Q2", "options": [], "answer": "B"}],
            "page": 2,
            "limit": 1,
            "total": 2,
            "totalPages": 2,
            "hasNext": False,
            "hasPrevious": True,
        }

    monkeypatch.setattr(qs, "get_deck_questions_page", _page)
    response = _run("GET", "/api/v1/subjects/pmg201c/decks/d1/questions?page=2")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["items"][0]["id"] == 2
    assert data["hasNext"] is False
    assert data["hasPrevious"] is True


def test_get_deck_questions_paginated_beyond_last_page(monkeypatch):
    monkeypatch.setattr(
        qs,
        "get_deck_questions_page",
        lambda _db, slug, deck_id, page, limit: {
            "items": [],
            "page": 99,
            "limit": 1,
            "total": 2,
            "totalPages": 2,
            "hasNext": False,
            "hasPrevious": True,
        },
    )
    response = _run("GET", "/api/v1/subjects/pmg201c/decks/d1/questions?page=99&limit=1")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["items"] == []
    assert data["hasNext"] is False


def test_get_source_state_ok(monkeypatch):
    monkeypatch.setattr(
        qs,
        "get_source_state",
        lambda _db, slug: {
            "bankQuestions": [],
            "deckQuestions": [],
            "files": [],
            "hocTheoDeLayout": "markdownFiles",
        },
    )
    response = _run("GET", "/api/v1/subjects/pmg201c/source-state")
    assert response.status_code == 200
    assert response.json()["data"]["hocTheoDeLayout"] == "markdownFiles"


def test_subject_not_found_decks(monkeypatch):
    def _boom(_db, slug, user_id=None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "SUBJECT_NOT_FOUND", "message": "Subject not found.", "details": {}}},
        )

    monkeypatch.setattr(qs, "get_subject_decks", _boom)
    response = _run("GET", "/api/v1/subjects/nope/decks")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "SUBJECT_NOT_FOUND"


def test_check_answer_ok(monkeypatch):
    def _check(_db, **kwargs):
        qid = kwargs["question_id"]
        sel = kwargs["selected_answer"]
        return {
            "questionId": qid,
            "selectedAnswer": sel,
            "correctAnswers": ["A"],
            "isCorrect": True,
        }

    monkeypatch.setattr(qs, "check_deck_answer", _check)
    response = _run(
        "POST",
        "/api/v1/subjects/pmg201c/decks/d1/questions/1/check",
        json={"selectedAnswer": "A"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["isCorrect"] is True


def test_put_deck_progress_ok(monkeypatch):
    def _update(_db, **kwargs):
        assert kwargs["attempted_question_ordinals"] == [1, 2, 2, 3]
        return {"ok": True}

    monkeypatch.setattr(qs, "update_deck_progress", _update)
    response = _run(
        "PUT",
        "/api/v1/subjects/pmg201c/decks/d1/progress",
        json={"currentQuestion": 3, "attemptedQuestionOrdinals": [1, 2, 2, 3]},
    )
    assert response.status_code == 200


def test_get_deck_progress_ok(monkeypatch):
    monkeypatch.setattr(
        qs,
        "get_deck_progress",
        lambda _db, **kwargs: {
            "currentQuestion": 12,
            "attemptedQuestionOrdinals": [1, 2, 3],
            "updatedAt": "2026-04-20T03:10:00+00:00",
        },
    )
    response = _run("GET", "/api/v1/subjects/pmg201c/decks/d1/progress")
    assert response.status_code == 200
    assert response.json()["data"]["attemptedQuestionOrdinals"] == [1, 2, 3]


def test_put_deck_stats_ok(monkeypatch):
    monkeypatch.setattr(qs, "update_deck_stats", lambda _db, **kwargs: {"ok": True})
    response = _run(
        "PUT",
        "/api/v1/subjects/pmg201c/decks/d1/stats",
        json={"inProgress": 1, "completed": 0},
    )
    assert response.status_code == 200
