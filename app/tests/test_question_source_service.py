from fastapi import HTTPException
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock

from app.services import question_source_service
from app.services.question_source_service import (
    check_deck_answer,
    detect_subject_and_exam,
    detect_subject_and_exam_with_fallback,
    get_deck_progress,
    get_subject_decks,
    ingest_markdown_file,
    parse_questions,
    update_deck_progress,
    update_deck_stats,
)


def test_detect_subject_and_exam_success() -> None:
    payload = detect_subject_and_exam("PRN232 - SP 2025 - FE.md")
    assert payload["subjectSlug"] == "prn232"
    assert payload["examCode"] == "SP-2025-FE"


def test_detect_subject_and_exam_invalid_filename() -> None:
    try:
        detect_subject_and_exam("abc.md")
    except HTTPException as exc:
        assert exc.status_code == 422
        assert exc.detail["error"]["code"] == "UNRECOGNIZED_FILENAME_PATTERN"
    else:
        raise AssertionError("Expected HTTPException for invalid filename")


def test_parse_questions_extracts_basic_fields() -> None:
    markdown = """
    Câu 1: Python là gì?
    A. Ngôn ngữ lập trình
    B. Món ăn
    Đáp án: A
    """
    questions, warnings = parse_questions(markdown)
    assert len(questions) == 1
    assert questions[0]["stem"] == "Python là gì?"
    assert questions[0]["options"][0]["label"] == "A"
    assert warnings == []


def test_parse_questions_extracts_inline_answer_from_stem() -> None:
    markdown = """
    Câu 1: Theo Mác-Lênin lực lượng cơ bản của xã hội là gì? Đáp án: A
    A. Quần chúng nhân dân
    B. Giai cấp nông dân
    C. Lãnh tụ
    D. Vĩ nhân
    """
    questions, _ = parse_questions(markdown)
    assert len(questions) == 1
    assert questions[0]["stem"].endswith("là gì?")
    assert questions[0]["answer_text"] == "A"


def test_ingest_markdown_file_persists_via_crud_path(monkeypatch) -> None:
    fake_subject = SimpleNamespace(id="subject-1")
    fake_source = SimpleNamespace(id="source-1")
    fake_crud = Mock()
    fake_crud.get_or_create_subject.return_value = fake_subject
    fake_crud.get_source_by_checksum.return_value = None
    fake_crud.create_source.return_value = fake_source
    monkeypatch.setattr(question_source_service, "crud_question_source", fake_crud)

    content = b"Cau 1: What is Python?\nA. Language\nB. Animal\nDap an: A\n"
    upload = SimpleNamespace(filename="PRN232 - SP 2025 - FE.md", file=BytesIO(content))

    result = ingest_markdown_file(db=Mock(), file=upload, uploader_id="admin-1")

    assert result["sourceId"] == "source-1"
    assert result["deduplicated"] is False
    fake_crud.create_source.assert_called_once()
    fake_crud.replace_source_questions.assert_called_once()


def test_detect_aggregated_file_requires_subject_slug() -> None:
    try:
        detect_subject_and_exam_with_fallback("cau-hoi-tong-hop.md", None)
    except HTTPException as exc:
        assert exc.status_code == 422
        assert exc.detail["error"]["code"] == "SUBJECT_SLUG_REQUIRED_FOR_AGGREGATED_FILE"
    else:
        raise AssertionError("Expected HTTPException for missing subjectSlug")


def test_get_subject_decks_excludes_aggregated_bank(monkeypatch) -> None:
    fake_subject = SimpleNamespace(id="subject-1")
    aggregated = SimpleNamespace(
        id="src-bank", exam_code="AGG-BANK", file_name="cau-hoi-tong-hop.md", question_count=200, uploaded_at=None
    )
    deck = SimpleNamespace(
        id="src-deck", exam_code="FA-2024-FE", file_name="PMG201c - FA 2024 - FE.md", question_count=50, uploaded_at=None
    )
    fake_crud = Mock()
    fake_crud.get_subject_by_slug.return_value = fake_subject
    fake_crud.list_sources_by_subject.return_value = [aggregated, deck]
    monkeypatch.setattr(question_source_service, "crud_question_source", fake_crud)

    decks = get_subject_decks(Mock(), "pmg201c")
    assert len(decks) == 1
    assert decks[0]["deckId"] == "src-deck"
    assert decks[0]["stats"]["total"] == 50
    assert decks[0]["stats"]["inProgress"] == 0
    assert decks[0]["stats"]["completed"] == 0


def test_update_deck_stats_validates_total(monkeypatch) -> None:
    fake_subject = SimpleNamespace(id="subject-1", slug="pmg201c")
    fake_source = SimpleNamespace(id="src-deck", question_count=50)
    fake_crud = Mock()
    fake_crud.get_subject_by_slug.return_value = fake_subject
    fake_crud.get_source_by_id.return_value = fake_source
    monkeypatch.setattr(question_source_service, "crud_question_source", fake_crud)

    result = update_deck_stats(
        Mock(),
        slug="pmg201c",
        deck_id="src-deck",
        user_id="user-1",
        in_progress=2,
        completed=3,
    )
    assert result["stats"]["total"] == 50
    assert result["stats"]["completionRatePercent"] == 4  # inProgress/total = 2/50 = 4%

    try:
        update_deck_stats(
            Mock(),
            slug="pmg201c",
            deck_id="src-deck",
            user_id="user-1",
            in_progress=40,
            completed=20,
        )
    except HTTPException as exc:
        assert exc.status_code == 422
        assert exc.detail["error"]["code"] == "INVALID_DECK_STATS"
    else:
        raise AssertionError("Expected HTTPException when deck stats exceed total questions")


def test_update_deck_progress_increments_completed_attempts(monkeypatch) -> None:
    fake_subject = SimpleNamespace(id="subject-1", slug="pmg201c")
    fake_source = SimpleNamespace(id="src-deck", question_count=50)
    fake_crud = Mock()
    fake_crud.get_subject_by_slug.return_value = fake_subject
    fake_crud.get_source_by_id.return_value = fake_source
    fake_crud.list_user_stats_by_source_ids.return_value = {
        "src-deck": {"current_question_ordinal": 49, "completed_attempts": 0}
    }
    monkeypatch.setattr(question_source_service, "crud_question_source", fake_crud)

    result = update_deck_progress(
        Mock(),
        slug="pmg201c",
        deck_id="src-deck",
        user_id="user-1",
        current_question=50,
        attempted_question_ordinals=[5, 2, 2, 1],
    )
    assert result["stats"]["completionRatePercent"] == 100
    assert result["stats"]["completed"] == 1
    assert result["attemptedQuestionOrdinals"] == [1, 2, 5]
    fake_crud.upsert_source_user_stats.assert_called_once()


def test_update_deck_progress_rejects_invalid_attempted_ordinals(monkeypatch) -> None:
    fake_subject = SimpleNamespace(id="subject-1", slug="pmg201c")
    fake_source = SimpleNamespace(id="src-deck", question_count=5)
    fake_crud = Mock()
    fake_crud.get_subject_by_slug.return_value = fake_subject
    fake_crud.get_source_by_id.return_value = fake_source
    fake_crud.list_user_stats_by_source_ids.return_value = {}
    monkeypatch.setattr(question_source_service, "crud_question_source", fake_crud)

    try:
        update_deck_progress(
            Mock(),
            slug="pmg201c",
            deck_id="src-deck",
            user_id="user-1",
            current_question=3,
            attempted_question_ordinals=[1, 2, 9],
        )
    except HTTPException as exc:
        assert exc.status_code == 422
        assert exc.detail["error"]["code"] == "INVALID_ATTEMPTED_QUESTION_ORDINALS"
    else:
        raise AssertionError("Expected HTTPException for invalid attempted ordinals")


def test_get_deck_progress_filters_invalid_ordinals(monkeypatch) -> None:
    fake_subject = SimpleNamespace(id="subject-1", slug="pmg201c")
    fake_source = SimpleNamespace(id="src-deck", question_count=5)
    fake_updated_at = SimpleNamespace(isoformat=lambda: "2026-04-20T03:10:00+00:00")
    fake_crud = Mock()
    fake_crud.get_subject_by_slug.return_value = fake_subject
    fake_crud.get_source_by_id.return_value = fake_source
    fake_crud.list_user_stats_by_source_ids.return_value = {
        "src-deck": {
            "current_question_ordinal": 8,
            "attempted_question_ordinals": [5, 3, 3, 10, 0],
            "updated_at": fake_updated_at,
        }
    }
    monkeypatch.setattr(question_source_service, "crud_question_source", fake_crud)

    result = get_deck_progress(
        Mock(),
        slug="pmg201c",
        deck_id="src-deck",
        user_id="user-1",
    )
    assert result["currentQuestion"] == 5
    assert result["attemptedQuestionOrdinals"] == [3, 5]
    assert result["updatedAt"] == "2026-04-20T03:10:00+00:00"


def test_check_deck_answer_returns_correctness(monkeypatch) -> None:
    fake_subject = SimpleNamespace(id="subject-1", slug="pmg201c")
    fake_source = SimpleNamespace(id="src-deck", question_count=50)
    fake_question = SimpleNamespace(answers_json=["B"], answer_text="B")
    fake_crud = Mock()
    fake_crud.get_subject_by_slug.return_value = fake_subject
    fake_crud.get_source_by_id.return_value = fake_source
    fake_crud.get_question_by_ordinal.return_value = fake_question
    monkeypatch.setattr(question_source_service, "crud_question_source", fake_crud)

    correct = check_deck_answer(
        Mock(),
        slug="pmg201c",
        deck_id="src-deck",
        question_id=3,
        selected_answer="b",
    )
    assert correct["isCorrect"] is True
    assert correct["correctAnswers"] == ["B"]
