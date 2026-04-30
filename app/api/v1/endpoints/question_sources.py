from typing import Any

from fastapi import APIRouter, Depends, File, Path, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_admin, require_course_access
from app.db.session import get_async_db, get_db
from app.models.user import User
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.question_source import (
    AnswerCheckRequest,
    AnswerCheckResponse,
    DeckProgressUpdateRequest,
    DeckProgressResponse,
    DeckStatsUpdateRequest,
    SourceStateQuestion,
    SourceStateResponse,
    UploadSourceResponse,
)
from app.utils.pagination import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, paginate_slice
from app.services.question_source_facade import question_source_service

# Keep dependency overrides stable for existing tests/clients while async service
# migration happens under the hood.
get_async_db = get_db

user_router = APIRouter(tags=["Question Sources"])
admin_router = APIRouter(tags=["Admin — Question Sources"])
router = APIRouter()

# Backward-compatible aliases for existing contract tests that monkeypatch
# endpoint-level symbols directly.
service_list_subjects = question_source_service.list_subjects
service_list_subjects_page = question_source_service.list_subjects_page
service_list_subjects_page_async = question_source_service.list_subjects_page_async
get_admin_subject_sources = question_source_service.get_admin_subject_sources
get_admin_subject_sources_page = question_source_service.get_admin_subject_sources_page
get_admin_subject_sources_page_async = question_source_service.get_admin_subject_sources_page_async
get_source_state = question_source_service.get_source_state
get_source_state_async = question_source_service.get_source_state_async
get_subject_bank = question_source_service.get_subject_bank
get_subject_bank_page = question_source_service.get_subject_bank_page
get_subject_bank_page_async = question_source_service.get_subject_bank_page_async
get_subject_bank_progress = question_source_service.get_subject_bank_progress
get_subject_bank_progress_async = question_source_service.get_subject_bank_progress_async
get_subject_decks = question_source_service.get_subject_decks
get_subject_decks_async = question_source_service.get_subject_decks_async
get_deck_questions = question_source_service.get_deck_questions
get_deck_questions_page = question_source_service.get_deck_questions_page
get_deck_questions_page_async = question_source_service.get_deck_questions_page_async
check_deck_answer = question_source_service.check_deck_answer
check_deck_answer_async = question_source_service.check_deck_answer_async
update_deck_progress = question_source_service.update_deck_progress
update_deck_progress_async = question_source_service.update_deck_progress_async
get_deck_progress = question_source_service.get_deck_progress
get_deck_progress_async = question_source_service.get_deck_progress_async
reset_deck_progress = question_source_service.reset_deck_progress
reset_deck_progress_async = question_source_service.reset_deck_progress_async
update_deck_stats = question_source_service.update_deck_stats
update_deck_stats_async = question_source_service.update_deck_stats_async
upsert_source_from_markdown_by_slug = question_source_service.upsert_source_from_markdown_by_slug
delete_source = question_source_service.delete_source


@user_router.get(
    "/subjects",
    response_model=ApiResponse[Any],
    summary="List subjects (paginated)",
    description=f"Default `page={DEFAULT_PAGE}`, `limit={DEFAULT_PAGE_SIZE}` (max `limit={MAX_PAGE_SIZE}`).",
)
async def list_subjects(
    db: Session = Depends(get_async_db),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        data = await service_list_subjects_page_async(db, page=page, limit=limit)
    else:
        data = service_list_subjects_page(db, page=page, limit=limit)
    return success_response(data=data)


@admin_router.get(
    "/admin/question-sources/subjects",
    response_model=ApiResponse[Any],
    summary="Admin: list subjects (paginated)",
)
async def admin_list_subjects(
    db: Session = Depends(get_async_db),
    _: User = Depends(get_current_admin),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        data = await service_list_subjects_page_async(db, page=page, limit=limit)
    else:
        data = service_list_subjects_page(db, page=page, limit=limit)
    return success_response(data=data)


@admin_router.get(
    "/admin/question-sources/subjects/{slug}/sources",
    response_model=ApiResponse[Any],
    summary="Admin: list sources for subject (paginated)",
)
async def admin_subject_sources(
    slug: str,
    db: Session = Depends(get_async_db),
    _: User = Depends(get_current_admin),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        data = await get_admin_subject_sources_page_async(db, slug, page=page, limit=limit)
    else:
        data = get_admin_subject_sources_page(db, slug, page=page, limit=limit)
    return success_response(data=data)


@user_router.get("/subjects/{slug}/source-state", response_model=ApiResponse[SourceStateResponse])
async def source_state(slug: str, db: Session = Depends(get_async_db), _: User = Depends(require_course_access)):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        data = await get_source_state_async(db, slug)
    else:
        data = get_source_state(db, slug)
    return success_response(data=data)


@user_router.get(
    "/subjects/{slug}/bank",
    response_model=ApiResponse[Any],
    summary="Subject bank questions (paginated)",
)
async def subject_bank(
    slug: str,
    db: Session = Depends(get_async_db),
    current_user: User = Depends(require_course_access),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        paginated = await get_subject_bank_page_async(db, slug, page=page, limit=limit)
        progress = await get_subject_bank_progress_async(db, slug=slug, user_id=current_user.id)
    else:
        paginated = get_subject_bank_page(db, slug, page=page, limit=limit)
        progress = get_subject_bank_progress(db, slug=slug, user_id=current_user.id)
    return success_response(data={**paginated, "progress": progress})


@user_router.get(
    "/subjects/{slug}/decks",
    response_model=ApiResponse[Any],
    summary="List decks for subject (paginated)",
    description=f"Default `page={DEFAULT_PAGE}`, `limit={DEFAULT_PAGE_SIZE}`.",
)
async def subject_decks(
    slug: str,
    db: Session = Depends(get_async_db),
    current_user: User = Depends(require_course_access),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        full = await get_subject_decks_async(db, slug, user_id=current_user.id)
    else:
        full = get_subject_decks(db, slug, user_id=current_user.id)
    return success_response(data=paginate_slice(full, page=page, limit=limit))


@user_router.get(
    "/subjects/{slug}/decks/{deck_id}/questions",
    response_model=ApiResponse[Any],
    summary="List deck questions (paginated)",
)
async def subject_deck_questions(
    slug: str,
    deck_id: str,
    db: Session = Depends(get_async_db),
    _: User = Depends(require_course_access),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=1, ge=1, le=50),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        data = await get_deck_questions_page_async(db, slug, deck_id, page=page, limit=limit)
    else:
        data = get_deck_questions_page(db, slug, deck_id, page=page, limit=limit)
    return success_response(data=data)


@user_router.post(
    "/subjects/{slug}/decks/{deck_id}/questions/{question_id}/check",
    response_model=ApiResponse[AnswerCheckResponse],
)
async def subject_deck_question_check(
    slug: str,
    deck_id: str,
    question_id: int = Path(ge=1),
    payload: AnswerCheckRequest = ...,
    db: Session = Depends(get_async_db),
    _: User = Depends(require_course_access),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        data = await check_deck_answer_async(
            db,
            slug=slug,
            deck_id=deck_id,
            question_id=question_id,
            selected_answer=payload.selectedAnswer,
        )
    else:
        data = check_deck_answer(
            db,
            slug=slug,
            deck_id=deck_id,
            question_id=question_id,
            selected_answer=payload.selectedAnswer,
        )
    return success_response(data=data, message="Checked answer successfully")


@user_router.put("/subjects/{slug}/decks/{deck_id}/progress", response_model=ApiResponse[dict])
async def subject_deck_progress_update(
    slug: str,
    deck_id: str,
    payload: DeckProgressUpdateRequest,
    db: Session = Depends(get_async_db),
    current_user: User = Depends(require_course_access),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        data = await update_deck_progress_async(
            db,
            slug=slug,
            deck_id=deck_id,
            user_id=current_user.id,
            current_question=payload.currentQuestion,
            attempted_question_ordinals=payload.attemptedQuestionOrdinals,
        )
    else:
        data = update_deck_progress(
            db,
            slug=slug,
            deck_id=deck_id,
            user_id=current_user.id,
            current_question=payload.currentQuestion,
            attempted_question_ordinals=payload.attemptedQuestionOrdinals,
        )
    return success_response(data=data, message="Deck progress updated successfully")


@user_router.get("/subjects/{slug}/decks/{deck_id}/progress", response_model=ApiResponse[DeckProgressResponse])
async def subject_deck_progress_get(
    slug: str,
    deck_id: str,
    db: Session = Depends(get_async_db),
    current_user: User = Depends(require_course_access),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        data = await get_deck_progress_async(db, slug=slug, deck_id=deck_id, user_id=current_user.id)
    else:
        data = get_deck_progress(db, slug=slug, deck_id=deck_id, user_id=current_user.id)
    return success_response(data=data)


@user_router.post("/subjects/{slug}/decks/{deck_id}/progress/reset", response_model=ApiResponse[dict])
async def subject_deck_progress_reset(
    slug: str,
    deck_id: str,
    db: Session = Depends(get_async_db),
    current_user: User = Depends(require_course_access),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        data = await reset_deck_progress_async(db, slug=slug, deck_id=deck_id, user_id=current_user.id)
    else:
        data = reset_deck_progress(db, slug=slug, deck_id=deck_id, user_id=current_user.id)
    return success_response(data=data, message="Deck progress reset successfully")


@user_router.put("/subjects/{slug}/decks/{deck_id}/stats", response_model=ApiResponse[dict])
async def subject_deck_stats_update(
    slug: str,
    deck_id: str,
    payload: DeckStatsUpdateRequest,
    db: Session = Depends(get_async_db),
    current_user: User = Depends(require_course_access),
):
    if settings.enable_async_database and isinstance(db, AsyncSession):
        data = await update_deck_stats_async(
            db,
            slug=slug,
            deck_id=deck_id,
            user_id=current_user.id,
            in_progress=payload.inProgress,
            completed=payload.completed,
        )
    else:
        data = update_deck_stats(
            db,
            slug=slug,
            deck_id=deck_id,
            user_id=current_user.id,
            in_progress=payload.inProgress,
            completed=payload.completed,
        )
    return success_response(data=data, message="Deck stats updated successfully")


@admin_router.post(
    "/admin/question-sources/subjects/{slug}/upload",
    response_model=ApiResponse[UploadSourceResponse],
    summary="Simple upsert source by slug + markdown file",
)
def admin_upsert_source_by_slug_upload(
    slug: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    data = upsert_source_from_markdown_by_slug(
        db,
        slug=slug,
        file=file,
        uploader_id=current_admin.id,
    )
    return success_response(data=data, message="Source upserted by slug upload successfully")


@admin_router.delete("/admin/question-sources/subjects/{slug}/sources/{source_id}", response_model=ApiResponse[dict])
def admin_delete_source_endpoint(
    slug: str,
    source_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return _delete_source_impl(db=db, slug=slug, source_id=source_id)


def _delete_source_impl(*, db: Session, slug: str, source_id: str) -> ApiResponse[dict]:
    data = delete_source(db, slug=slug, source_id=source_id)
    return success_response(data=data, message="Source deleted permanently")


router.include_router(user_router)
router.include_router(admin_router)
