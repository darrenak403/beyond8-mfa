from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

import app.services.question_source_service as legacy


class QuestionSourceService:
    """Facade service to provide a single entrypoint for question-source flows."""

    def list_subjects(self, db: Session):
        return legacy.list_subjects(db)
    
    def list_subjects_page(self, db: Session, *, page: int, limit: int):
        return legacy.list_subjects_page(db, page=page, limit=limit)

    async def list_subjects_page_async(self, db: AsyncSession, *, page: int, limit: int):
        return await legacy.list_subjects_page_async(db, page=page, limit=limit)

    def get_admin_subject_sources(self, db: Session, slug: str):
        return legacy.get_admin_subject_sources(db, slug)
    
    def get_admin_subject_sources_page(self, db: Session, slug: str, *, page: int, limit: int):
        return legacy.get_admin_subject_sources_page(db, slug, page=page, limit=limit)

    async def get_admin_subject_sources_page_async(self, db: AsyncSession, slug: str, *, page: int, limit: int):
        return await legacy.get_admin_subject_sources_page_async(db, slug, page=page, limit=limit)

    def get_source_state(self, db: Session, slug: str):
        return legacy.get_source_state(db, slug)

    async def get_source_state_async(self, db: AsyncSession, slug: str):
        return await legacy.get_source_state_async(db, slug)

    def get_subject_bank(self, db: Session, slug: str):
        return legacy.get_subject_bank(db, slug)
    
    def get_subject_bank_page(self, db: Session, slug: str, *, page: int, limit: int):
        return legacy.get_subject_bank_page(db, slug, page=page, limit=limit)

    async def get_subject_bank_page_async(self, db: AsyncSession, slug: str, *, page: int, limit: int):
        return await legacy.get_subject_bank_page_async(db, slug, page=page, limit=limit)

    def get_subject_bank_progress(self, db: Session, *, slug: str, user_id: str):
        return legacy.get_subject_bank_progress(db, slug=slug, user_id=user_id)

    async def get_subject_bank_progress_async(self, db: AsyncSession, *, slug: str, user_id: str):
        return await legacy.get_subject_bank_progress_async(db, slug=slug, user_id=user_id)

    def get_subject_decks(self, db: Session, slug: str, *, user_id: str | None = None):
        return legacy.get_subject_decks(db, slug, user_id=user_id)

    async def get_subject_decks_async(self, db: AsyncSession, slug: str, *, user_id: str | None = None):
        return await legacy.get_subject_decks_async(db, slug, user_id=user_id)

    def get_deck_questions(self, db: Session, slug: str, deck_id: str):
        return legacy.get_deck_questions(db, slug, deck_id)

    def get_deck_questions_page(self, db: Session, slug: str, deck_id: str, *, page: int, limit: int):
        return legacy.get_deck_questions_page(db, slug, deck_id, page=page, limit=limit)

    async def get_deck_questions_page_async(self, db: AsyncSession, slug: str, deck_id: str, *, page: int, limit: int):
        return await legacy.get_deck_questions_page_async(db, slug, deck_id, page=page, limit=limit)

    def check_deck_answer(self, db: Session, *, slug: str, deck_id: str, question_id: int, selected_answer: str):
        return legacy.check_deck_answer(
            db,
            slug=slug,
            deck_id=deck_id,
            question_id=question_id,
            selected_answer=selected_answer,
        )

    async def check_deck_answer_async(
        self, db: AsyncSession, *, slug: str, deck_id: str, question_id: int, selected_answer: str
    ):
        return await legacy.check_deck_answer_async(
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

    async def update_deck_progress_async(
        self,
        db: AsyncSession,
        *,
        slug: str,
        deck_id: str,
        user_id: str,
        current_question: int,
        attempted_question_ordinals: list[int],
    ):
        return await legacy.update_deck_progress_async(
            db,
            slug=slug,
            deck_id=deck_id,
            user_id=user_id,
            current_question=current_question,
            attempted_question_ordinals=attempted_question_ordinals,
        )

    def get_deck_progress(self, db: Session, *, slug: str, deck_id: str, user_id: str):
        return legacy.get_deck_progress(db, slug=slug, deck_id=deck_id, user_id=user_id)

    async def get_deck_progress_async(self, db: AsyncSession, *, slug: str, deck_id: str, user_id: str):
        return await legacy.get_deck_progress_async(db, slug=slug, deck_id=deck_id, user_id=user_id)

    def reset_deck_progress(self, db: Session, *, slug: str, deck_id: str, user_id: str):
        return legacy.reset_deck_progress(db, slug=slug, deck_id=deck_id, user_id=user_id)

    async def reset_deck_progress_async(self, db: AsyncSession, *, slug: str, deck_id: str, user_id: str):
        return await legacy.reset_deck_progress_async(db, slug=slug, deck_id=deck_id, user_id=user_id)

    def update_deck_stats(self, db: Session, *, slug: str, deck_id: str, user_id: str, in_progress: int, completed: int):
        return legacy.update_deck_stats(
            db,
            slug=slug,
            deck_id=deck_id,
            user_id=user_id,
            in_progress=in_progress,
            completed=completed,
        )

    async def update_deck_stats_async(
        self, db: AsyncSession, *, slug: str, deck_id: str, user_id: str, in_progress: int, completed: int
    ):
        return await legacy.update_deck_stats_async(
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

    def merge_deck_into_aggregated_bank_preview(self, db: Session, *, slug: str, deck_source_id: str):
        return legacy.merge_deck_into_aggregated_bank_preview(db, slug=slug, deck_source_id=deck_source_id)

    def merge_deck_into_aggregated_bank(self, db: Session, *, slug: str, deck_source_id: str, uploader_id: str | None):
        return legacy.merge_deck_into_aggregated_bank(
            db, slug=slug, deck_source_id=deck_source_id, uploader_id=uploader_id
        )

    def ensure_admin_subject(self, db: Session, *, slug: str):
        return legacy.ensure_admin_subject(db, slug=slug)


question_source_service = QuestionSourceService()
