from app.services.auth_service import auth_service
from app.services.otp_service import otp_service
from app.services.question_source_service import (
    check_deck_answer,
    detect_subject_and_exam,
    detect_subject_and_exam_with_fallback,
    delete_source,
    get_admin_subject_sources,
    get_deck_questions,
    get_source_state,
    get_subject_bank,
    get_subject_decks,
    ingest_markdown_file,
    list_subjects,
    parse_questions,
    update_deck_progress,
    update_deck_stats,
    update_source_questions,
    update_source_from_markdown,
)
from app.services.stats_service import stats_service

__all__ = [
    "auth_service",
    "otp_service",
    "stats_service",
    "ingest_markdown_file",
    "list_subjects",
    "get_source_state",
    "get_subject_bank",
    "get_subject_decks",
    "get_deck_questions",
    "detect_subject_and_exam",
    "detect_subject_and_exam_with_fallback",
    "check_deck_answer",
    "delete_source",
    "get_admin_subject_sources",
    "parse_questions",
    "update_deck_progress",
    "update_deck_stats",
    "update_source_questions",
    "update_source_from_markdown",
]
