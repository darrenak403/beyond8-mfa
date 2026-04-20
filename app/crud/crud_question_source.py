import json
import uuid

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.question_source import ParseStatus, QuestionSource
from app.models.subject import Subject


class CRUDQuestionSource:
    def ensure_tables(self, db: Session) -> None:
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS subjects (
                    id VARCHAR(36) PRIMARY KEY,
                    slug VARCHAR(64) UNIQUE NOT NULL,
                    code VARCHAR(32) UNIQUE NOT NULL,
                    name VARCHAR(255),
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS question_sources (
                    id VARCHAR(36) PRIMARY KEY,
                    subject_id VARCHAR(36) NOT NULL REFERENCES subjects(id),
                    exam_code VARCHAR(64) NOT NULL,
                    file_name VARCHAR(255) NOT NULL,
                    checksum_sha256 VARCHAR(71) NOT NULL,
                    raw_storage_key VARCHAR(255),
                    uploaded_by VARCHAR(255),
                    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    parse_status VARCHAR(16) NOT NULL,
                    parse_warnings JSONB NOT NULL DEFAULT '[]'::jsonb,
                    question_count INTEGER NOT NULL DEFAULT 0,
                    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
                    deleted_reason TEXT
                )
                """
            )
        )
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS questions (
                    id VARCHAR(36) PRIMARY KEY,
                    source_id VARCHAR(36) NOT NULL REFERENCES question_sources(id),
                    ordinal INTEGER NOT NULL,
                    stem TEXT NOT NULL,
                    options_json JSONB NOT NULL DEFAULT '[]'::jsonb,
                    answers_json JSONB NOT NULL DEFAULT '[]'::jsonb,
                    answer_text TEXT NOT NULL,
                    normalized_hash VARCHAR(71) NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS question_source_user_stats (
                    id VARCHAR(36) PRIMARY KEY,
                    source_id VARCHAR(36) NOT NULL REFERENCES question_sources(id) ON DELETE CASCADE,
                    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    in_progress_count INTEGER NOT NULL DEFAULT 0,
                    completed_count INTEGER NOT NULL DEFAULT 0,
                    current_question_ordinal INTEGER NOT NULL DEFAULT 0,
                    attempted_question_ordinals JSONB NOT NULL DEFAULT '[]'::jsonb,
                    completed_attempts INTEGER NOT NULL DEFAULT 0,
                    completion_rate_percent INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    UNIQUE(source_id, user_id)
                )
                """
            )
        )
        db.execute(
            text(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_question_sources_subject_exam_checksum "
                "ON question_sources(subject_id, exam_code, checksum_sha256)"
            )
        )
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_questions_source_id ON questions(source_id)"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_questions_normalized_hash ON questions(normalized_hash)"))
        db.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_questions_source_ordinal ON questions(source_id, ordinal)"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_question_source_user_stats_user_id ON question_source_user_stats(user_id)"))
        db.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_question_source_user_stats_source_id ON question_source_user_stats(source_id)"
            )
        )
        db.execute(
            text(
                "ALTER TABLE question_source_user_stats "
                "ADD COLUMN IF NOT EXISTS current_question_ordinal INTEGER NOT NULL DEFAULT 0"
            )
        )
        db.execute(
            text(
                "ALTER TABLE question_source_user_stats "
                "ADD COLUMN IF NOT EXISTS attempted_question_ordinals JSONB NOT NULL DEFAULT '[]'::jsonb"
            )
        )
        db.execute(
            text(
                "ALTER TABLE question_source_user_stats "
                "ADD COLUMN IF NOT EXISTS completed_attempts INTEGER NOT NULL DEFAULT 0"
            )
        )

    def get_or_create_subject(self, db: Session, *, slug: str, code: str) -> Subject:
        subject = db.execute(select(Subject).where(Subject.slug == slug)).scalar_one_or_none()
        if subject is not None:
            return subject
        try:
            with db.begin_nested():
                subject = Subject(slug=slug, code=code, name=code)
                db.add(subject)
                db.flush()
                return subject
        except IntegrityError:
            existing = db.execute(select(Subject).where(Subject.slug == slug)).scalar_one_or_none()
            if existing is None:
                raise
            return existing

    def get_source_by_checksum(self, db: Session, *, subject_id: str, exam_code: str, checksum_sha256: str) -> QuestionSource | None:
        return db.execute(
            select(QuestionSource).where(
                QuestionSource.subject_id == subject_id,
                QuestionSource.exam_code == exam_code,
                QuestionSource.checksum_sha256 == checksum_sha256,
                QuestionSource.is_deleted.is_(False),
            )
        ).scalar_one_or_none()

    def create_source(
        self,
        db: Session,
        *,
        subject_id: str,
        exam_code: str,
        file_name: str,
        checksum_sha256: str,
        uploaded_by: str | None,
        warnings: list[str],
        question_count: int,
    ) -> QuestionSource:
        source = QuestionSource(
            subject_id=subject_id,
            exam_code=exam_code,
            file_name=file_name,
            checksum_sha256=checksum_sha256,
            uploaded_by=uploaded_by,
            parse_status=ParseStatus.SUCCESS.value,
            parse_warnings=warnings,
            question_count=question_count,
        )
        db.add(source)
        db.flush()
        return source

    def replace_source_questions(self, db: Session, *, source_id: str, payload: list[dict]) -> None:
        db.execute(text("DELETE FROM questions WHERE source_id = :source_id"), {"source_id": source_id})
        for item in payload:
            db.add(
                Question(
                    source_id=source_id,
                    ordinal=item["ordinal"],
                    stem=item["stem"],
                    options_json=item["options"],
                    answers_json=item["answers"],
                    answer_text=item["answer_text"],
                    normalized_hash=item["normalized_hash"],
                )
            )
        db.flush()

    def list_subjects(self, db: Session) -> list[Subject]:
        return list(db.execute(select(Subject).where(Subject.is_active.is_(True)).order_by(Subject.code.asc())).scalars().all())

    def get_subject_by_slug(self, db: Session, slug: str) -> Subject | None:
        return db.execute(select(Subject).where(Subject.slug == slug, Subject.is_active.is_(True))).scalar_one_or_none()

    def get_latest_source(self, db: Session, subject_id: str) -> QuestionSource | None:
        return db.execute(
            select(QuestionSource)
            .where(
                QuestionSource.subject_id == subject_id,
                QuestionSource.parse_status == ParseStatus.SUCCESS.value,
                QuestionSource.is_deleted.is_(False),
            )
            .order_by(QuestionSource.uploaded_at.desc(), QuestionSource.id.desc())
            .limit(1)
        ).scalar_one_or_none()

    def list_source_questions(self, db: Session, source_id: str) -> list[Question]:
        return list(db.execute(select(Question).where(Question.source_id == source_id).order_by(Question.ordinal.asc())).scalars().all())

    def list_source_questions_payload(self, db: Session, source_id: str) -> list[dict]:
        rows = db.execute(
            select(Question.ordinal, Question.stem, Question.options_json, Question.answer_text)
            .where(Question.source_id == source_id)
            .order_by(Question.ordinal.asc())
        ).all()
        return [
            {
                "ordinal": int(row.ordinal or 0),
                "stem": row.stem,
                "options": row.options_json or [],
                "answer": row.answer_text,
            }
            for row in rows
        ]

    def list_source_questions_payload_slice(self, db: Session, source_id: str, *, offset: int, limit: int) -> list[dict]:
        """Ordered slice by ordinal for pagination (offset/limit)."""
        if limit <= 0:
            return []
        rows = db.execute(
            select(Question.ordinal, Question.stem, Question.options_json, Question.answer_text)
            .where(Question.source_id == source_id)
            .order_by(Question.ordinal.asc())
            .offset(max(0, offset))
            .limit(limit)
        ).all()
        return [
            {
                "ordinal": int(row.ordinal or 0),
                "stem": row.stem,
                "options": row.options_json or [],
                "answer": row.answer_text,
            }
            for row in rows
        ]

    def list_questions_by_source_ids(self, db: Session, source_ids: list[str]) -> dict[str, list[Question]]:
        """Load questions for many sources in one round-trip (avoids N+1 per source)."""
        if not source_ids:
            return {}
        ordered_unique = list(dict.fromkeys(source_ids))
        rows = list(
            db.execute(
                select(Question)
                .where(Question.source_id.in_(ordered_unique))
                .order_by(Question.source_id.asc(), Question.ordinal.asc())
            ).scalars().all()
        )
        grouped: dict[str, list[Question]] = {sid: [] for sid in ordered_unique}
        for question in rows:
            grouped[question.source_id].append(question)
        return grouped

    def list_questions_payload_by_source_ids(self, db: Session, source_ids: list[str]) -> dict[str, list[dict]]:
        """Load lightweight question payload for many sources in one round-trip."""
        if not source_ids:
            return {}
        ordered_unique = list(dict.fromkeys(source_ids))
        rows = db.execute(
            select(Question.source_id, Question.ordinal, Question.stem, Question.options_json, Question.answer_text)
            .where(Question.source_id.in_(ordered_unique))
            .order_by(Question.source_id.asc(), Question.ordinal.asc())
        ).all()
        grouped: dict[str, list[dict]] = {sid: [] for sid in ordered_unique}
        for row in rows:
            grouped[row.source_id].append(
                {
                    "ordinal": int(row.ordinal or 0),
                    "stem": row.stem,
                    "options": row.options_json or [],
                    "answer": row.answer_text,
                }
            )
        return grouped

    def list_sources_by_subject(self, db: Session, subject_id: str) -> list[QuestionSource]:
        return list(
            db.execute(
                select(QuestionSource)
                .where(
                    QuestionSource.subject_id == subject_id,
                    QuestionSource.parse_status == ParseStatus.SUCCESS.value,
                    QuestionSource.is_deleted.is_(False),
                )
                .order_by(QuestionSource.uploaded_at.desc(), QuestionSource.id.desc())
            ).scalars().all()
        )

    def get_source_by_id(self, db: Session, *, subject_id: str, source_id: str) -> QuestionSource | None:
        return db.execute(
            select(QuestionSource).where(
                QuestionSource.id == source_id,
                QuestionSource.subject_id == subject_id,
                QuestionSource.parse_status == ParseStatus.SUCCESS.value,
                QuestionSource.is_deleted.is_(False),
            )
        ).scalar_one_or_none()

    def update_source_question_stats(self, db: Session, *, source: QuestionSource, question_count: int, warnings: list[str]) -> None:
        source.question_count = question_count
        source.parse_warnings = warnings
        db.add(source)
        db.flush()

    def hard_delete_source(self, db: Session, *, source_id: str) -> None:
        db.execute(text("DELETE FROM questions WHERE source_id = :source_id"), {"source_id": source_id})
        db.execute(text("DELETE FROM question_sources WHERE id = :source_id"), {"source_id": source_id})
        db.flush()

    def list_user_stats_by_source_ids(self, db: Session, *, user_id: str, source_ids: list[str]) -> dict[str, dict]:
        if not source_ids:
            return {}
        rows = db.execute(
            text(
                """
                SELECT
                    source_id,
                    in_progress_count,
                    completed_count,
                    current_question_ordinal,
                    attempted_question_ordinals,
                    completed_attempts,
                    completion_rate_percent,
                    updated_at
                FROM question_source_user_stats
                WHERE user_id = :user_id AND source_id = ANY(:source_ids)
                """
            ),
            {"user_id": user_id, "source_ids": source_ids},
        ).mappings().all()
        result: dict[str, dict] = {}
        for row in rows:
            source_id = str(row["source_id"])
            result[source_id] = {
                "in_progress_count": int(row["in_progress_count"] or 0),
                "completed_count": int(row["completed_count"] or 0),
                "current_question_ordinal": int(row["current_question_ordinal"] or 0),
                "attempted_question_ordinals": list(row.get("attempted_question_ordinals") or []),
                "completed_attempts": int(row["completed_attempts"] or 0),
                "completion_rate_percent": int(row["completion_rate_percent"] or 0),
                "updated_at": row.get("updated_at"),
            }
        return result

    def upsert_source_user_stats(
        self,
        db: Session,
        *,
        source_id: str,
        user_id: str,
        current_question_ordinal: int,
        attempted_question_ordinals: list[int],
        completed_attempts: int,
        in_progress_count: int,
        completed_count: int,
        completion_rate_percent: int,
    ) -> None:
        db.execute(
            text(
                """
                INSERT INTO question_source_user_stats (
                    id,
                    source_id,
                    user_id,
                    current_question_ordinal,
                    attempted_question_ordinals,
                    completed_attempts,
                    in_progress_count,
                    completed_count,
                    completion_rate_percent
                ) VALUES (
                    :id,
                    :source_id,
                    :user_id,
                    :current_question_ordinal,
                    CAST(:attempted_question_ordinals AS JSONB),
                    :completed_attempts,
                    :in_progress_count,
                    :completed_count,
                    :completion_rate_percent
                )
                ON CONFLICT (source_id, user_id)
                DO UPDATE SET
                    current_question_ordinal = EXCLUDED.current_question_ordinal,
                    attempted_question_ordinals = EXCLUDED.attempted_question_ordinals,
                    completed_attempts = EXCLUDED.completed_attempts,
                    in_progress_count = EXCLUDED.in_progress_count,
                    completed_count = EXCLUDED.completed_count,
                    completion_rate_percent = EXCLUDED.completion_rate_percent,
                    updated_at = NOW()
                """
            ),
            {
                "id": str(uuid.uuid4()),
                "source_id": source_id,
                "user_id": user_id,
                "current_question_ordinal": current_question_ordinal,
                "attempted_question_ordinals": json.dumps(attempted_question_ordinals),
                "completed_attempts": completed_attempts,
                "in_progress_count": in_progress_count,
                "completed_count": completed_count,
                "completion_rate_percent": completion_rate_percent,
            },
        )
        db.flush()

    def get_question_by_ordinal(self, db: Session, *, source_id: str, ordinal: int) -> Question | None:
        return db.execute(
            select(Question).where(Question.source_id == source_id, Question.ordinal == ordinal)
        ).scalar_one_or_none()


crud_question_source = CRUDQuestionSource()
