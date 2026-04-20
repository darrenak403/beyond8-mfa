import hashlib
import logging
import math
import re
import unicodedata

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.crud import crud_question_source
from app.services.cache_service import cache_service

_SUBJECT_PATTERN = re.compile(r"^[A-Z]{3,4}[0-9]{3}[A-Z]?$")
_TERM_PATTERN = re.compile(r"^(SP|SU|FA)$")
_YEAR_PATTERN = re.compile(r"^(\d{2}|\d{4})$")
_TYPE_PATTERN = re.compile(r"^(FE|RE|TE1|TE2|BLOCK5|C1FE|C2FE|FINAL)$")
_QUESTION_START = re.compile(r"^\s*(?:(?:C[ÂA]U)|QUESTION)?\s*\d+\s*[\).:\-]\s*(.+)$", flags=re.IGNORECASE)
_OPTION_LINE = re.compile(r"^\s*([A-D])[\).:\-]\s*(.+)$", flags=re.IGNORECASE)
_ANSWER_LINE = re.compile(r"^\s*(?:(?:Đ|D)[ÁA]P\s*Á?N|ANSWER)\s*[:\-]\s*(.+)$", flags=re.IGNORECASE)
_INLINE_ANSWER = re.compile(r"\s*(?:(?:Đ|D)[ÁA]P\s*Á?N|ANSWER)\s*[:\-]\s*([A-D](?:\s*[,;/]\s*[A-D])*)\s*$", flags=re.IGNORECASE)
_MAX_UPLOAD_BYTES = 5 * 1024 * 1024
_CACHE_SUBJECTS_TTL_SECONDS = 600
_CACHE_SUBJECT_READ_TTL_SECONDS = 300
_CACHE_DECK_LIST_TTL_SECONDS = 120
_CACHE_DECK_QUESTIONS_TTL_SECONDS = 600
logger = logging.getLogger(__name__)


def _error(status_code: int, code: str, message: str, details: dict | None = None) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"error": {"code": code, "message": message, "details": details or {}}})


def _normalize_filename(filename: str) -> str:
    normalized = unicodedata.normalize("NFKC", filename)
    normalized = re.sub(r"\.md$", "", normalized, flags=re.IGNORECASE).upper().replace("_", " ")
    normalized = re.sub(r"\s*-\s*", " - ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _to_year(raw_year: str) -> int:
    return int(f"20{raw_year}") if len(raw_year) == 2 else int(raw_year)


def _is_aggregated_bank_filename(file_name: str) -> bool:
    normalized = unicodedata.normalize("NFKC", file_name).strip().lower()
    return normalized == "cau-hoi-tong-hop.md" or normalized == "cau-hoi-tong-hop"


def _subject_code_from_slug(subject_slug: str) -> str:
    if subject_slug.lower() == "prn232":
        return "PRN232"
    return subject_slug.upper()


def _cache_global_subjects_version() -> int:
    return cache_service.get_int("qs:subjects:ver", default=1)


def _cache_subject_version(slug: str) -> int:
    return cache_service.get_int(f"qs:subject:{slug}:ver", default=1)


def _cache_user_decks_version(slug: str, user_id: str) -> int:
    return cache_service.get_int(f"qs:subject:{slug}:user:{user_id}:decks:ver", default=1)


def _invalidate_subject_catalog() -> None:
    cache_service.bump_version("qs:subjects:ver")


def _invalidate_subject_reads(slug: str) -> None:
    cache_service.bump_version(f"qs:subject:{slug}:ver")


def _invalidate_user_decks(slug: str, user_id: str) -> None:
    cache_service.bump_version(f"qs:subject:{slug}:user:{user_id}:decks:ver")


def _schedule_after_commit(db: Session, callback) -> None:
    callbacks = db.info.setdefault("cache_after_commit_callbacks", [])
    callbacks.append(callback)
    if db.info.get("cache_after_commit_registered"):
        return
    db.info["cache_after_commit_registered"] = True

    @event.listens_for(db, "after_commit")
    def _after_commit(session: Session) -> None:  # pragma: no cover - integration behavior
        pending = session.info.pop("cache_after_commit_callbacks", [])
        for item in pending:
            try:
                item()
            except Exception as exc:
                # Cache invalidation failure must never break request flow.
                logger.warning("Cache invalidation callback failed: %s", exc, exc_info=True)

    @event.listens_for(db, "after_rollback")
    def _after_rollback(session: Session) -> None:  # pragma: no cover - integration behavior
        session.info.pop("cache_after_commit_callbacks", None)


def detect_subject_and_exam(file_name: str) -> dict:
    normalized = _normalize_filename(file_name)
    tokens = [tok for tok in re.split(r"[\s\-]+", normalized) if tok]
    subject = next((tok for tok in tokens if _SUBJECT_PATTERN.match(tok)), None)
    if subject is None:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "UNRECOGNIZED_FILENAME_PATTERN", "Cannot detect subject/exam from filename.")
    term = next((tok for tok in tokens if _TERM_PATTERN.match(tok)), None)
    year_token = next((tok for tok in tokens if _YEAR_PATTERN.match(tok)), None)
    exam_type = next((tok for tok in tokens if _TYPE_PATTERN.match(tok)), None)
    if not term or not year_token or not exam_type:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "UNRECOGNIZED_FILENAME_PATTERN", "Cannot detect subject/exam from filename.")
    year = _to_year(year_token)
    subject_slug = "prn232" if subject in {"PRN231", "PRN232"} else subject.lower()
    return {
        "subjectCode": subject,
        "subjectSlug": subject_slug,
        "term": term,
        "year": year,
        "type": exam_type,
        "examCode": f"{term}-{year}-{exam_type}",
    }


def detect_subject_and_exam_with_fallback(file_name: str, fallback_subject_slug: str | None = None) -> dict:
    if _is_aggregated_bank_filename(file_name):
        if not fallback_subject_slug:
            raise _error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "SUBJECT_SLUG_REQUIRED_FOR_AGGREGATED_FILE",
                "subjectSlug is required when uploading cau-hoi-tong-hop.md.",
            )
        subject_slug = fallback_subject_slug.strip().lower()
        if not subject_slug:
            raise _error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "SUBJECT_SLUG_REQUIRED_FOR_AGGREGATED_FILE",
                "subjectSlug is required when uploading cau-hoi-tong-hop.md.",
            )
        return {
            "subjectCode": _subject_code_from_slug(subject_slug),
            "subjectSlug": subject_slug,
            "term": "AGG",
            "year": 0,
            "type": "BANK",
            "examCode": "AGG-BANK",
        }
    return detect_subject_and_exam(file_name)


def parse_questions(markdown_text: str) -> tuple[list[dict], list[str]]:
    lines = [line.rstrip() for line in markdown_text.splitlines()]
    entries: list[dict] = []
    warnings: list[str] = []
    current: dict | None = None
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        question_match = _QUESTION_START.match(line)
        if question_match:
            if current is not None:
                entries.append(current)
            stem_text = question_match.group(1).strip()
            inline_answer_match = _INLINE_ANSWER.search(stem_text)
            answer_text = ""
            answers: list[str] = []
            if inline_answer_match:
                answer_text = inline_answer_match.group(1).strip().upper()
                answers = [item.strip().upper() for item in re.split(r"[;,/]+", answer_text) if item.strip()]
                stem_text = _INLINE_ANSWER.sub("", stem_text).strip()
            current = {"stem": stem_text, "options": [], "answer_text": answer_text, "answers": answers}
            continue
        if current is None:
            continue
        option_match = _OPTION_LINE.match(line)
        if option_match:
            current["options"].append({"label": option_match.group(1).upper(), "text": option_match.group(2).strip()})
            continue
        answer_match = _ANSWER_LINE.match(line)
        if answer_match:
            current["answer_text"] = answer_match.group(1).strip().upper()
            current["answers"] = [item.strip().upper() for item in re.split(r"[;,/]+", current["answer_text"]) if item.strip()]
            continue
        current["stem"] = f"{current['stem']} {line}".strip()
        warnings.append(f"Question parsing consumed unmatched line at question #{len(entries) + 1}: {line[:80]}")
    if current is not None:
        entries.append(current)

    if not entries:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "INVALID_MARKDOWN_FORMAT", "No valid questions parsed from markdown file.")

    normalized: list[dict] = []
    for idx, item in enumerate(entries, start=1):
        if not item["options"]:
            warnings.append(f"Question #{idx} has no options.")
        if not item["answer_text"]:
            warnings.append(f"Question #{idx} has no explicit answer line.")
        hash_source = f"{item['stem']}|{item['options']}|{item['answer_text']}".encode("utf-8")
        normalized_hash = f"sha256:{hashlib.sha256(hash_source).hexdigest()}"
        normalized.append(
            {
                "ordinal": idx,
                "stem": item["stem"],
                "options": item["options"],
                "answers": item["answers"],
                "answer_text": item["answer_text"],
                "normalized_hash": normalized_hash,
            }
        )
    return normalized, warnings


def ingest_markdown_file(
    db: Session, file: UploadFile, uploader_id: str | None, subject_slug: str | None = None
) -> dict:
    if not file.filename or not file.filename.lower().endswith(".md"):
        raise _error(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "INVALID_FILE_TYPE", "Only .md files are accepted.")
    raw_bytes = file.file.read(_MAX_UPLOAD_BYTES + 1)
    if len(raw_bytes) > _MAX_UPLOAD_BYTES:
        raise _error(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "FILE_TOO_LARGE", "File exceeds 5MB limit.")
    metadata = detect_subject_and_exam_with_fallback(file.filename, subject_slug)
    checksum = f"sha256:{hashlib.sha256(raw_bytes).hexdigest()}"
    subject = crud_question_source.get_or_create_subject(
        db, slug=metadata["subjectSlug"], code=metadata["subjectCode"]
    )
    existing = crud_question_source.get_source_by_checksum(
        db, subject_id=subject.id, exam_code=metadata["examCode"], checksum_sha256=checksum
    )
    if existing is not None:
        return {
            "sourceId": existing.id,
            "subjectSlug": metadata["subjectSlug"],
            "subjectCode": metadata["subjectCode"],
            "examCode": metadata["examCode"],
            "fileName": existing.file_name,
            "checksum": existing.checksum_sha256,
            "questionCount": existing.question_count,
            "warnings": existing.parse_warnings or [],
            "deduplicated": True,
        }

    markdown_text = raw_bytes.decode("utf-8", errors="ignore")
    questions, warnings = parse_questions(markdown_text)
    source = crud_question_source.create_source(
        db,
        subject_id=subject.id,
        exam_code=metadata["examCode"],
        file_name=file.filename,
        checksum_sha256=checksum,
        uploaded_by=uploader_id,
        warnings=warnings,
        question_count=len(questions),
    )
    crud_question_source.replace_source_questions(db, source_id=source.id, payload=questions)
    _schedule_after_commit(
        db,
        lambda: (_invalidate_subject_catalog(), _invalidate_subject_reads(metadata["subjectSlug"])),
    )
    return {
        "sourceId": source.id,
        "subjectSlug": metadata["subjectSlug"],
        "subjectCode": metadata["subjectCode"],
        "examCode": metadata["examCode"],
        "fileName": file.filename,
        "checksum": checksum,
        "questionCount": len(questions),
        "warnings": warnings,
        "deduplicated": False,
    }


def list_subjects(db: Session) -> list[dict]:
    version = _cache_global_subjects_version()
    cache_key = f"qs:subjects:v{version}"
    cached = cache_service.get_json(cache_key)
    if isinstance(cached, list):
        return cached
    payload = [{"slug": row.slug, "code": row.code, "hint": "Mon luyen de"} for row in crud_question_source.list_subjects(db)]
    cache_service.set_json(cache_key, payload, _CACHE_SUBJECTS_TTL_SECONDS)
    return payload


def get_admin_subject_sources(db: Session, slug: str) -> list[dict]:
    normalized_slug = slug.lower()
    version = _cache_subject_version(normalized_slug)
    cache_key = f"qs:admin:subject:{normalized_slug}:sources:v{version}"
    cached = cache_service.get_json(cache_key)
    if isinstance(cached, list):
        return cached
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    sources = crud_question_source.list_sources_by_subject(db, subject.id)
    payload = [
        {
            "sourceId": source.id,
            # FE wants Exam column to display file name without `.md`.
            "examCode": re.sub(r"\.md$", "", source.file_name, flags=re.IGNORECASE),
            "fileName": source.file_name,
            "questionCount": int(source.question_count or 0),
            "isAggregatedBank": _is_aggregated_bank_filename(source.file_name),
            "uploadedAt": source.uploaded_at.isoformat() if source.uploaded_at else None,
        }
        for source in sources
    ]
    cache_service.set_json(cache_key, payload, _CACHE_SUBJECT_READ_TTL_SECONDS)
    return payload


def get_source_state(db: Session, slug: str) -> dict:
    normalized_slug = slug.lower()
    version = _cache_subject_version(normalized_slug)
    cache_key = f"qs:subject:{normalized_slug}:source-state:v{version}"
    cached = cache_service.get_json(cache_key)
    if isinstance(cached, dict):
        return cached
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    sources = crud_question_source.list_sources_by_subject(db, subject.id)
    if not sources:
        payload = {"bankQuestions": [], "deckQuestions": [], "files": [], "hocTheoDeLayout": "markdownFiles"}
        cache_service.set_json(cache_key, payload, _CACHE_SUBJECT_READ_TTL_SECONDS)
        return payload
    bank_source = next((item for item in sources if _is_aggregated_bank_filename(item.file_name)), None) or sources[0]
    deck_sources = [item for item in sources if not _is_aggregated_bank_filename(item.file_name)]

    load_ids = [bank_source.id, *[s.id for s in deck_sources]]
    questions_by_source = crud_question_source.list_questions_payload_by_source_ids(db, load_ids)

    bank_questions = questions_by_source.get(bank_source.id, [])
    bank_formatted = [
        {"id": idx, "stem": item["stem"], "options": item["options"], "answer": item["answer"]}
        for idx, item in enumerate(bank_questions, start=1)
    ]
    deck_questions: list[dict] = []
    files: list[dict] = []
    running_index = 0
    for source in deck_sources:
        questions = questions_by_source.get(source.id, [])
        start = running_index
        next_questions = [
            {"id": idx + running_index + 1, "stem": item["stem"], "options": item["options"], "answer": item["answer"]}
            for idx, item in enumerate(questions)
        ]
        deck_questions.extend(next_questions)
        running_index = len(deck_questions)
        end = running_index - 1
        has_questions = len(questions) > 0
        files.append(
            {
                "deckId": source.id,
                "fileName": source.file_name,
                "isEmpty": not has_questions,
                "questionCount": int(source.question_count or 0),
                "range": {"start": start, "end": end} if has_questions else {"start": 0, "end": 0},
            }
        )

    payload = {
        "bankQuestions": bank_formatted,
        "deckQuestions": deck_questions,
        "files": files,
        "hocTheoDeLayout": "markdownFiles",
    }
    cache_service.set_json(cache_key, payload, _CACHE_SUBJECT_READ_TTL_SECONDS)
    return payload


def get_subject_bank(db: Session, slug: str) -> list[dict]:
    normalized_slug = slug.lower()
    version = _cache_subject_version(normalized_slug)
    cache_key = f"qs:subject:{normalized_slug}:bank:v{version}"
    cached = cache_service.get_json(cache_key)
    if isinstance(cached, list):
        return cached
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    sources = crud_question_source.list_sources_by_subject(db, subject.id)
    if not sources:
        cache_service.set_json(cache_key, [], _CACHE_SUBJECT_READ_TTL_SECONDS)
        return []
    source = next((item for item in sources if _is_aggregated_bank_filename(item.file_name)), None) or sources[0]
    questions = crud_question_source.list_source_questions_payload(db, source.id)
    payload = [{"id": idx, "stem": item["stem"], "options": item["options"], "answer": item["answer"]} for idx, item in enumerate(questions, start=1)]
    cache_service.set_json(cache_key, payload, _CACHE_SUBJECT_READ_TTL_SECONDS)
    return payload


def _build_deck_stats(
    total_questions: int,
    current_question_ordinal: int,
    completed_attempts: int,
) -> dict:
    safe_total = max(total_questions, 0)
    safe_current = max(current_question_ordinal, 0)
    safe_completed_attempts = max(completed_attempts, 0)
    if safe_total > 0:
        safe_current = min(safe_current, safe_total)
        computed_rate = int(round((safe_current / safe_total) * 100))
    else:
        safe_current = 0
        computed_rate = 0
    return {
        "total": safe_total,
        "inProgress": safe_current,
        "completed": safe_completed_attempts,
        "completionRatePercent": max(0, min(computed_rate, 100)),
    }


def _normalize_attempted_ordinals(raw_ordinals: object, *, question_count: int) -> list[int]:
    if not isinstance(raw_ordinals, list):
        return []
    normalized = sorted({value for value in raw_ordinals if isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= question_count})
    return normalized


def get_subject_decks(db: Session, slug: str, *, user_id: str | None = None) -> list[dict]:
    normalized_slug = slug.lower()
    if user_id:
        subject_version = _cache_subject_version(normalized_slug)
        user_version = _cache_user_decks_version(normalized_slug, user_id)
        cache_key = f"qs:subject:{normalized_slug}:user:{user_id}:decks:sv{subject_version}:uv{user_version}"
    else:
        version = _cache_subject_version(normalized_slug)
        cache_key = f"qs:subject:{normalized_slug}:decks:v{version}"
    cached = cache_service.get_json(cache_key)
    if isinstance(cached, list):
        return cached
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    sources = crud_question_source.list_sources_by_subject(db, subject.id)
    deck_sources = [source for source in sources if not _is_aggregated_bank_filename(source.file_name)]
    stats_by_source_id: dict[str, dict] = {}
    if user_id:
        stats_by_source_id = crud_question_source.list_user_stats_by_source_ids(
            db, user_id=user_id, source_ids=[item.id for item in deck_sources]
        )
    result: list[dict] = []
    for source in deck_sources:
        total_questions = int(source.question_count or 0)
        user_stats = stats_by_source_id.get(source.id, {})
        current_question_ordinal = int(
            user_stats.get("current_question_ordinal", user_stats.get("in_progress_count", 0))
        )
        completed_attempts = int(user_stats.get("completed_attempts", user_stats.get("completed_count", 0)))
        result.append(
            {
                "deckId": source.id,
                "examCode": source.exam_code,
                "fileName": source.file_name,
                "questionCount": total_questions,
                "stats": _build_deck_stats(total_questions, current_question_ordinal, completed_attempts),
                "uploadedAt": source.uploaded_at.isoformat() if source.uploaded_at else None,
            }
        )
    cache_service.set_json(cache_key, result, _CACHE_DECK_LIST_TTL_SECONDS)
    return result


def get_deck_questions(db: Session, slug: str, deck_id: str) -> list[dict]:
    normalized_slug = slug.lower()
    version = _cache_subject_version(normalized_slug)
    cache_key = f"qs:subject:{normalized_slug}:deck:{deck_id}:questions:v{version}"
    cached = cache_service.get_json(cache_key)
    if isinstance(cached, list):
        return cached
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    source = crud_question_source.get_source_by_id(db, subject_id=subject.id, source_id=deck_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "DECK_NOT_FOUND", "Deck not found for subject.")
    questions = crud_question_source.list_source_questions_payload(db, source.id)
    payload = [{"id": idx, "stem": item["stem"], "options": item["options"], "answer": item["answer"]} for idx, item in enumerate(questions, start=1)]
    cache_service.set_json(cache_key, payload, _CACHE_DECK_QUESTIONS_TTL_SECONDS)
    return payload


def get_deck_questions_page(db: Session, slug: str, deck_id: str, *, page: int, limit: int) -> dict:
    """Paginated deck questions (no full-deck Redis cache; uses DB slice + subject question_count for total)."""
    normalized_slug = slug.lower()
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    source = crud_question_source.get_source_by_id(db, subject_id=subject.id, source_id=deck_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "DECK_NOT_FOUND", "Deck not found for subject.")

    total = int(source.question_count or 0)
    if total <= 0:
        total_pages = 0
        items: list[dict] = []
    else:
        total_pages = max(1, math.ceil(total / limit))
        offset = (page - 1) * limit
        slice_rows = crud_question_source.list_source_questions_payload_slice(
            db, source.id, offset=offset, limit=limit
        )
        items = [
            {"id": offset + idx + 1, "stem": item["stem"], "options": item["options"], "answer": item["answer"]}
            for idx, item in enumerate(slice_rows)
        ]

    has_next = total > 0 and page < total_pages
    has_previous = page > 1 and total > 0

    return {
        "items": items,
        "page": page,
        "limit": limit,
        "total": total,
        "totalPages": total_pages,
        "hasNext": has_next,
        "hasPrevious": has_previous,
    }


def update_deck_stats(
    db: Session,
    *,
    slug: str,
    deck_id: str,
    user_id: str,
    in_progress: int,
    completed: int,
) -> dict:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    source = crud_question_source.get_source_by_id(db, subject_id=subject.id, source_id=deck_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "DECK_NOT_FOUND", "Deck not found for subject.")

    total_questions = int(source.question_count or 0)
    if in_progress + completed > total_questions:
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "INVALID_DECK_STATS",
            "inProgress + completed cannot exceed total questions of this deck.",
            details={
                "total": total_questions,
                "inProgress": in_progress,
                "completed": completed,
            },
        )

    completion_rate_percent = 0
    if total_questions > 0:
        completion_rate_percent = int(round((in_progress / total_questions) * 100))
    current_stats = crud_question_source.list_user_stats_by_source_ids(
        db, user_id=user_id, source_ids=[source.id]
    ).get(source.id, {})
    attempted_question_ordinals = _normalize_attempted_ordinals(
        current_stats.get("attempted_question_ordinals", []),
        question_count=total_questions,
    )

    crud_question_source.upsert_source_user_stats(
        db,
        source_id=source.id,
        user_id=user_id,
        current_question_ordinal=in_progress,
        attempted_question_ordinals=attempted_question_ordinals,
        completed_attempts=completed,
        in_progress_count=in_progress,
        completed_count=completed,
        completion_rate_percent=completion_rate_percent,
    )
    subject_slug = subject.slug
    _schedule_after_commit(db, lambda: _invalidate_user_decks(subject_slug, user_id))

    return {
        "deckId": source.id,
        "subjectSlug": subject.slug,
        "stats": _build_deck_stats(total_questions, in_progress, completed),
    }


def update_deck_progress(
    db: Session,
    *,
    slug: str,
    deck_id: str,
    user_id: str,
    current_question: int,
    attempted_question_ordinals: list[int],
) -> dict:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    source = crud_question_source.get_source_by_id(db, subject_id=subject.id, source_id=deck_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "DECK_NOT_FOUND", "Deck not found for subject.")

    total_questions = int(source.question_count or 0)
    invalid_ordinals = [
        value
        for value in attempted_question_ordinals
        if not isinstance(value, int) or isinstance(value, bool) or value < 1 or value > total_questions
    ]
    if invalid_ordinals:
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "INVALID_ATTEMPTED_QUESTION_ORDINALS",
            "attemptedQuestionOrdinals must be within 1..questionCount.",
            details={"questionCount": total_questions, "invalidOrdinals": invalid_ordinals},
        )
    clamped_current_question = min(max(current_question, 0), total_questions)
    normalized_attempted_ordinals = _normalize_attempted_ordinals(
        attempted_question_ordinals,
        question_count=total_questions,
    )

    current_stats = crud_question_source.list_user_stats_by_source_ids(
        db, user_id=user_id, source_ids=[source.id]
    ).get(source.id, {})
    previous_current = int(
        current_stats.get("current_question_ordinal", current_stats.get("in_progress_count", 0))
    )
    completed_attempts = int(current_stats.get("completed_attempts", current_stats.get("completed_count", 0)))
    if total_questions > 0 and clamped_current_question >= total_questions and previous_current < total_questions:
        completed_attempts += 1

    completion_rate_percent = 0
    if total_questions > 0:
        completion_rate_percent = int(round((clamped_current_question / total_questions) * 100))

    crud_question_source.upsert_source_user_stats(
        db,
        source_id=source.id,
        user_id=user_id,
        current_question_ordinal=clamped_current_question,
        attempted_question_ordinals=normalized_attempted_ordinals,
        completed_attempts=completed_attempts,
        in_progress_count=clamped_current_question,
        completed_count=completed_attempts,
        completion_rate_percent=completion_rate_percent,
    )
    subject_slug = subject.slug
    _schedule_after_commit(db, lambda: _invalidate_user_decks(subject_slug, user_id))
    return {
        "deckId": source.id,
        "subjectSlug": subject.slug,
        "stats": _build_deck_stats(total_questions, clamped_current_question, completed_attempts),
        "currentQuestion": clamped_current_question,
        "attemptedQuestionOrdinals": normalized_attempted_ordinals,
    }


def get_deck_progress(
    db: Session,
    *,
    slug: str,
    deck_id: str,
    user_id: str,
) -> dict:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    source = crud_question_source.get_source_by_id(db, subject_id=subject.id, source_id=deck_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "DECK_NOT_FOUND", "Deck not found for subject.")

    total_questions = int(source.question_count or 0)
    current_stats = crud_question_source.list_user_stats_by_source_ids(
        db, user_id=user_id, source_ids=[source.id]
    ).get(source.id)
    if current_stats is None:
        return {
            "currentQuestion": 0,
            "attemptedQuestionOrdinals": [],
            "updatedAt": None,
        }

    current_question = min(
        max(int(current_stats.get("current_question_ordinal", 0)), 0),
        total_questions,
    )
    attempted_question_ordinals = _normalize_attempted_ordinals(
        current_stats.get("attempted_question_ordinals", []),
        question_count=total_questions,
    )
    updated_at = current_stats.get("updated_at")
    return {
        "currentQuestion": current_question,
        "attemptedQuestionOrdinals": attempted_question_ordinals,
        "updatedAt": updated_at.isoformat() if updated_at else None,
    }


def check_deck_answer(
    db: Session,
    *,
    slug: str,
    deck_id: str,
    question_id: int,
    selected_answer: str,
) -> dict:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    source = crud_question_source.get_source_by_id(db, subject_id=subject.id, source_id=deck_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "DECK_NOT_FOUND", "Deck not found for subject.")

    question = crud_question_source.get_question_by_ordinal(db, source_id=source.id, ordinal=question_id)
    if question is None:
        raise _error(status.HTTP_404_NOT_FOUND, "QUESTION_NOT_FOUND", "Question not found for deck.")

    selected = selected_answer.strip().upper()
    if not selected:
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "INVALID_SELECTED_ANSWER",
            "selectedAnswer must not be empty.",
        )

    correct_answers = [str(item).strip().upper() for item in (question.answers_json or []) if str(item).strip()]
    if not correct_answers and question.answer_text:
        correct_answers = [part.strip().upper() for part in re.split(r"[;,/]+", question.answer_text) if part.strip()]
    is_correct = selected in correct_answers
    return {
        "questionId": question_id,
        "selectedAnswer": selected,
        "correctAnswers": correct_answers,
        "isCorrect": is_correct,
    }


def update_source_questions(db: Session, slug: str, source_id: str, questions: list[dict]) -> dict:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")

    source = crud_question_source.get_source_by_id(db, subject_id=subject.id, source_id=source_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SOURCE_NOT_FOUND", "Source not found for subject.")

    if not questions:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "INVALID_QUESTIONS_PAYLOAD", "Questions payload must not be empty.")

    normalized: list[dict] = []
    warnings: list[str] = []
    for idx, item in enumerate(questions, start=1):
        stem = (item.get("stem") or "").strip()
        options = item.get("options") or []
        answer_text = (item.get("answer") or "").strip()
        if not stem:
            raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "INVALID_QUESTIONS_PAYLOAD", f"Question #{idx} is missing stem.")
        if not options:
            warnings.append(f"Question #{idx} has no options.")
        if not answer_text:
            warnings.append(f"Question #{idx} has no explicit answer.")
        answers = [part.strip().upper() for part in re.split(r"[;,/]+", answer_text) if part.strip()]
        normalized_options = [{"label": str(op.get("label", "")).strip(), "text": str(op.get("text", "")).strip()} for op in options]
        hash_source = f"{stem}|{normalized_options}|{answer_text}".encode("utf-8")
        normalized_hash = f"sha256:{hashlib.sha256(hash_source).hexdigest()}"
        normalized.append(
            {
                "ordinal": idx,
                "stem": stem,
                "options": normalized_options,
                "answers": answers,
                "answer_text": answer_text,
                "normalized_hash": normalized_hash,
            }
        )

    crud_question_source.replace_source_questions(db, source_id=source.id, payload=normalized)
    crud_question_source.update_source_question_stats(
        db, source=source, question_count=len(normalized), warnings=warnings
    )
    subject_slug = subject.slug
    _schedule_after_commit(db, lambda: (_invalidate_subject_catalog(), _invalidate_subject_reads(subject_slug)))
    return {
        "sourceId": source.id,
        "subjectSlug": subject.slug,
        "examCode": source.exam_code,
        "fileName": source.file_name,
        "questionCount": len(normalized),
        "warnings": warnings,
    }


def update_source_from_markdown(
    db: Session,
    *,
    slug: str,
    source_id: str,
    file: UploadFile,
) -> dict:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")

    source = crud_question_source.get_source_by_id(db, subject_id=subject.id, source_id=source_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SOURCE_NOT_FOUND", "Source not found for subject.")

    if not file.filename or not file.filename.lower().endswith(".md"):
        raise _error(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "INVALID_FILE_TYPE", "Only .md files are accepted.")

    raw_bytes = file.file.read(_MAX_UPLOAD_BYTES + 1)
    if len(raw_bytes) > _MAX_UPLOAD_BYTES:
        raise _error(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "FILE_TOO_LARGE", "File exceeds 5MB limit.")

    metadata = detect_subject_and_exam_with_fallback(file.filename, slug)
    if metadata["subjectSlug"] != slug.lower():
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "SUBJECT_MISMATCH",
            "Uploaded markdown does not match target subject.",
        )

    markdown_text = raw_bytes.decode("utf-8", errors="ignore")
    parsed_questions, parse_warnings = parse_questions(markdown_text)
    checksum = f"sha256:{hashlib.sha256(raw_bytes).hexdigest()}"
    existing = crud_question_source.get_source_by_checksum(
        db, subject_id=subject.id, exam_code=metadata["examCode"], checksum_sha256=checksum
    )
    if existing is not None and existing.id != source.id:
        raise _error(
            status.HTTP_409_CONFLICT,
            "DUPLICATE_SOURCE",
            "A source with the same exam code and checksum already exists.",
            details={"existingSourceId": existing.id},
        )

    source.exam_code = metadata["examCode"]
    source.file_name = file.filename
    source.checksum_sha256 = checksum
    source.parse_warnings = parse_warnings
    source.question_count = len(parsed_questions)
    db.add(source)

    crud_question_source.replace_source_questions(db, source_id=source.id, payload=parsed_questions)
    db.flush()
    subject_slug = subject.slug
    _schedule_after_commit(db, lambda: (_invalidate_subject_catalog(), _invalidate_subject_reads(subject_slug)))

    return {
        "sourceId": source.id,
        "subjectSlug": subject.slug,
        "subjectCode": subject.code,
        "examCode": source.exam_code,
        "fileName": source.file_name,
        "checksum": source.checksum_sha256,
        "questionCount": source.question_count,
        "warnings": parse_warnings,
        "deduplicated": False,
    }


def upsert_source_from_markdown_by_slug(
    db: Session,
    *,
    slug: str,
    file: UploadFile,
    uploader_id: str | None,
) -> dict:
    """
    Simple admin flow: upload `.md` with explicit subject slug.

    Behavior:
    - Subject slug is the source-of-truth; if subject does not exist, create it.
    - New upload creates a new source row under that subject.
    - Exact duplicate (same examCode + checksum) returns existing source with deduplicated=True.
    - For mistaken upload, admin should hard-delete source, then upload again.
    """
    normalized_slug = slug.strip().lower()
    if not normalized_slug:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "INVALID_SUBJECT_SLUG", "Subject slug is required.")
    subject = crud_question_source.get_or_create_subject(
        db, slug=normalized_slug, code=_subject_code_from_slug(normalized_slug)
    )

    if not file.filename or not file.filename.lower().endswith(".md"):
        raise _error(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "INVALID_FILE_TYPE", "Only .md files are accepted.")

    raw_bytes = file.file.read(_MAX_UPLOAD_BYTES + 1)
    if len(raw_bytes) > _MAX_UPLOAD_BYTES:
        raise _error(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "FILE_TOO_LARGE", "File exceeds 5MB limit.")

    metadata = detect_subject_and_exam_with_fallback(file.filename, normalized_slug)

    checksum = f"sha256:{hashlib.sha256(raw_bytes).hexdigest()}"
    same_checksum = crud_question_source.get_source_by_checksum(
        db, subject_id=subject.id, exam_code=metadata["examCode"], checksum_sha256=checksum
    )
    if same_checksum is not None:
        return {
            "sourceId": same_checksum.id,
            "subjectSlug": subject.slug,
            "subjectCode": subject.code,
            "examCode": same_checksum.exam_code,
            "fileName": same_checksum.file_name,
            "checksum": same_checksum.checksum_sha256,
            "questionCount": int(same_checksum.question_count or 0),
            "warnings": same_checksum.parse_warnings or [],
            "deduplicated": True,
        }

    markdown_text = raw_bytes.decode("utf-8", errors="ignore")
    parsed_questions, parse_warnings = parse_questions(markdown_text)
    source = crud_question_source.create_source(
        db,
        subject_id=subject.id,
        exam_code=metadata["examCode"],
        file_name=file.filename,
        checksum_sha256=checksum,
        uploaded_by=uploader_id,
        warnings=parse_warnings,
        question_count=len(parsed_questions),
    )

    crud_question_source.replace_source_questions(db, source_id=source.id, payload=parsed_questions)
    db.flush()
    subject_slug = subject.slug
    _schedule_after_commit(db, lambda: (_invalidate_subject_catalog(), _invalidate_subject_reads(subject_slug)))
    return {
        "sourceId": source.id,
        "subjectSlug": subject.slug,
        "subjectCode": subject.code,
        "examCode": source.exam_code,
        "fileName": source.file_name,
        "checksum": source.checksum_sha256,
        "questionCount": source.question_count,
        "warnings": parse_warnings,
        "deduplicated": False,
    }


def delete_source(db: Session, *, slug: str, source_id: str) -> dict:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")

    source = crud_question_source.get_source_by_id(db, subject_id=subject.id, source_id=source_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SOURCE_NOT_FOUND", "Source not found for subject.")

    source_file_name = source.file_name
    crud_question_source.hard_delete_source(db, source_id=source.id)
    subject_slug = subject.slug
    _schedule_after_commit(db, lambda: (_invalidate_subject_catalog(), _invalidate_subject_reads(subject_slug)))
    return {
        "sourceId": source_id,
        "subjectSlug": subject.slug,
        "fileName": source_file_name,
        "deleted": True,
        "hardDeleted": True,
    }
