from fastapi import UploadFile
from sqlalchemy.orm import Session

import app.services.question_source_service as legacy


class QuestionSourceService:
    """Facade service to provide a single entrypoint for question-source flows."""

    def list_subjects(self, db: Session):
        return legacy.list_subjects(db)

    def get_admin_subject_sources(self, db: Session, slug: str):
        return legacy.get_admin_subject_sources(db, slug)

    def get_source_state(self, db: Session, slug: str):
        return legacy.get_source_state(db, slug)

    def get_subject_bank(self, db: Session, slug: str):
        return legacy.get_subject_bank(db, slug)

    def get_subject_bank_progress(self, db: Session, *, slug: str, user_id: str):
        return legacy.get_subject_bank_progress(db, slug=slug, user_id=user_id)

    def get_subject_decks(self, db: Session, slug: str, *, user_id: str | None = None):
        return legacy.get_subject_decks(db, slug, user_id=user_id)

    def get_deck_questions(self, db: Session, slug: str, deck_id: str):
        return legacy.get_deck_questions(db, slug, deck_id)

    def get_deck_questions_page(self, db: Session, slug: str, deck_id: str, *, page: int, limit: int):
        return legacy.get_deck_questions_page(db, slug, deck_id, page=page, limit=limit)

    def check_deck_answer(self, db: Session, *, slug: str, deck_id: str, question_id: int, selected_answer: str):
        return legacy.check_deck_answer(
            db,
            slug=slug,
            deck_id=deck_id,
            question_id=question_id,
            selected_answer=selected_answer,
        )

    def update_deck_progress(
        self,
        db: Session,
        *,
        slug: str,
        deck_id: str,
        user_id: str,
        current_question: int,
        attempted_question_ordinals: list[int],
    ):
        return legacy.update_deck_progress(
            db,
            slug=slug,
            deck_id=deck_id,
            user_id=user_id,
            current_question=current_question,
            attempted_question_ordinals=attempted_question_ordinals,
        )

    def get_deck_progress(self, db: Session, *, slug: str, deck_id: str, user_id: str):
        return legacy.get_deck_progress(db, slug=slug, deck_id=deck_id, user_id=user_id)

    def update_deck_stats(self, db: Session, *, slug: str, deck_id: str, user_id: str, in_progress: int, completed: int):
        return legacy.update_deck_stats(
            db,
            slug=slug,
            deck_id=deck_id,
            user_id=user_id,
            in_progress=in_progress,
            completed=completed,
        )

    def upsert_source_from_markdown_by_slug(self, db: Session, *, slug: str, file: UploadFile, uploader_id: str | None):
        return legacy.upsert_source_from_markdown_by_slug(
            db,
            slug=slug,
            file=file,
            uploader_id=uploader_id,
        )

    def delete_source(self, db: Session, *, slug: str, source_id: str):
        return legacy.delete_source(db, slug=slug, source_id=source_id)


question_source_service = QuestionSourceService()
