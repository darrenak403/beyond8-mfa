import hashlib
import re
import unicodedata

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.crud import crud_question_source

_SUBJECT_PATTERN = re.compile(r"^[A-Z]{3,4}[0-9]{3}[A-Z]?$")
_TERM_PATTERN = re.compile(r"^(SP|SU|FA)$")
_YEAR_PATTERN = re.compile(r"^(\d{2}|\d{4})$")
_TYPE_PATTERN = re.compile(r"^(FE|RE|TE1|TE2|BLOCK5|C1FE|C2FE|FINAL)$")
_QUESTION_START = re.compile(r"^\s*(?:(?:C[ÂA]U)|QUESTION)?\s*\d+\s*[\).:\-]\s*(.+)$", flags=re.IGNORECASE)
_OPTION_LINE = re.compile(r"^\s*([A-D])[\).:\-]\s*(.+)$", flags=re.IGNORECASE)
_ANSWER_LINE = re.compile(r"^\s*(?:(?:Đ|D)[ÁA]P\s*Á?N|ANSWER)\s*[:\-]\s*(.+)$", flags=re.IGNORECASE)
_INLINE_ANSWER = re.compile(r"\s*(?:(?:Đ|D)[ÁA]P\s*Á?N|ANSWER)\s*[:\-]\s*([A-D](?:\s*[,;/]\s*[A-D])*)\s*$", flags=re.IGNORECASE)
_MAX_UPLOAD_BYTES = 5 * 1024 * 1024


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
    return [{"slug": row.slug, "code": row.code, "hint": "Mon luyen de"} for row in crud_question_source.list_subjects(db)]


def get_source_state(db: Session, slug: str) -> dict:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    sources = crud_question_source.list_sources_by_subject(db, subject.id)
    if not sources:
        return {"bankQuestions": [], "deckQuestions": [], "files": [], "hocTheoDeLayout": "markdownFiles"}
    bank_source = next((item for item in sources if _is_aggregated_bank_filename(item.file_name)), None) or sources[0]
    deck_sources = [item for item in sources if not _is_aggregated_bank_filename(item.file_name)]

    bank_questions = crud_question_source.list_source_questions(db, bank_source.id)
    bank_formatted = [
        {"id": idx, "stem": item.stem, "options": item.options_json or [], "answer": item.answer_text}
        for idx, item in enumerate(bank_questions, start=1)
    ]
    deck_questions: list[dict] = []
    for source in deck_sources:
        questions = crud_question_source.list_source_questions(db, source.id)
        deck_questions.extend(
            {"id": idx + len(deck_questions), "stem": item.stem, "options": item.options_json or [], "answer": item.answer_text}
            for idx, item in enumerate(questions, start=1)
        )

    return {
        "bankQuestions": bank_formatted,
        "deckQuestions": deck_questions,
        "files": [
            {
                "fileName": source.file_name,
                "isEmpty": source.question_count == 0,
                "questionCount": source.question_count,
                "range": {"start": 0, "end": max(source.question_count - 1, 0)},
            }
            for source in sources
        ],
        "hocTheoDeLayout": "markdownFiles",
    }


def get_subject_bank(db: Session, slug: str) -> list[dict]:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    sources = crud_question_source.list_sources_by_subject(db, subject.id)
    if not sources:
        return []
    source = next((item for item in sources if _is_aggregated_bank_filename(item.file_name)), None) or sources[0]
    questions = crud_question_source.list_source_questions(db, source.id)
    return [{"id": idx, "stem": item.stem, "options": item.options_json or [], "answer": item.answer_text} for idx, item in enumerate(questions, start=1)]


def get_subject_decks(db: Session, slug: str) -> list[dict]:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    sources = crud_question_source.list_sources_by_subject(db, subject.id)
    result: list[dict] = []
    for source in sources:
        if _is_aggregated_bank_filename(source.file_name):
            continue
        result.append(
            {
                "deckId": source.id,
                "examCode": source.exam_code,
                "fileName": source.file_name,
                "questionCount": source.question_count,
                "uploadedAt": source.uploaded_at.isoformat() if source.uploaded_at else None,
            }
        )
    return result


def get_deck_questions(db: Session, slug: str, deck_id: str) -> list[dict]:
    subject = crud_question_source.get_subject_by_slug(db, slug)
    if subject is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SUBJECT_NOT_FOUND", "Subject not found.")
    source = crud_question_source.get_source_by_id(db, subject_id=subject.id, source_id=deck_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "DECK_NOT_FOUND", "Deck not found for subject.")
    questions = crud_question_source.list_source_questions(db, source.id)
    return [{"id": idx, "stem": item.stem, "options": item.options_json or [], "answer": item.answer_text} for idx, item in enumerate(questions, start=1)]


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

    source.exam_code = metadata["examCode"]
    source.file_name = file.filename
    source.checksum_sha256 = checksum
    source.parse_warnings = parse_warnings
    source.question_count = len(parsed_questions)
    db.add(source)

    crud_question_source.replace_source_questions(db, source_id=source.id, payload=parsed_questions)
    db.flush()

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
    return {
        "sourceId": source_id,
        "subjectSlug": subject.slug,
        "fileName": source_file_name,
        "deleted": True,
        "hardDeleted": True,
    }
