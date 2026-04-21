from typing import Any

from fastapi import APIRouter, Depends, File, Path, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, require_course_access
from app.db.session import get_db
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
from app.services import (
    check_deck_answer,
    delete_source,
    get_admin_subject_sources,
    get_deck_questions,
    get_deck_questions_page,
    get_source_state,
    get_subject_bank,
    get_subject_bank_progress,
    get_subject_decks,
    list_subjects as service_list_subjects,
    update_deck_progress,
    get_deck_progress,
    update_deck_stats,
    upsert_source_from_markdown_by_slug,
)

user_router = APIRouter(prefix="/v1", tags=["Question Sources"])
admin_router = APIRouter(prefix="/v1", tags=["Admin — Question Sources"])
router = APIRouter()


@user_router.get(
    "/subjects",
    response_model=ApiResponse[Any],
    summary="List subjects (paginated)",
    description=f"Default `page={DEFAULT_PAGE}`, `limit={DEFAULT_PAGE_SIZE}` (max `limit={MAX_PAGE_SIZE}`).",
)
def list_subjects(
    db: Session = Depends(get_db),
    _: User = Depends(require_course_access),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
):
    full = service_list_subjects(db)
    return success_response(data=paginate_slice(full, page=page, limit=limit))


@admin_router.get(
    "/admin/question-sources/subjects",
    response_model=ApiResponse[Any],
    summary="Admin: list subjects (paginated)",
)
def admin_list_subjects(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
):
    full = service_list_subjects(db)
    return success_response(data=paginate_slice(full, page=page, limit=limit))


@admin_router.get(
    "/admin/question-sources/subjects/{slug}/sources",
    response_model=ApiResponse[Any],
    summary="Admin: list sources for subject (paginated)",
)
def admin_subject_sources(
    slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
):
    full = get_admin_subject_sources(db, slug)
    return success_response(data=paginate_slice(full, page=page, limit=limit))


@user_router.get("/subjects/{slug}/source-state", response_model=ApiResponse[SourceStateResponse])
def source_state(slug: str, db: Session = Depends(get_db), _: User = Depends(require_course_access)):
    data = get_source_state(db, slug)
    return success_response(data=data)


@user_router.get(
    "/subjects/{slug}/bank",
    response_model=ApiResponse[Any],
    summary="Subject bank questions (full list or paginated)",
    description=(
        "Without `page`: returns `data` as a full array (legacy). "
        "With `page`: returns paginated object; `limit` optional (default 10, max "
        f"{MAX_PAGE_SIZE}), controlled by the client."
    ),
)
def subject_bank(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_course_access),
    page: int | None = Query(default=None, ge=1),
    limit: int | None = Query(default=None, ge=1, le=MAX_PAGE_SIZE),
):
    data = get_subject_bank(db, slug)
    if page is None:
        return success_response(data=data)
    eff_limit = DEFAULT_PAGE_SIZE if limit is None else limit
    paginated = paginate_slice(data, page=page, limit=eff_limit)
    progress = get_subject_bank_progress(db, slug=slug, user_id=current_user.id)
    return success_response(data={**paginated, "progress": progress})


@user_router.get(
    "/subjects/{slug}/decks",
    response_model=ApiResponse[Any],
    summary="List decks for subject (paginated)",
    description=f"Default `page={DEFAULT_PAGE}`, `limit={DEFAULT_PAGE_SIZE}`.",
)
def subject_decks(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_course_access),
    page: int = Query(default=DEFAULT_PAGE, ge=1),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
):
    full = get_subject_decks(db, slug, user_id=current_user.id)
    return success_response(data=paginate_slice(full, page=page, limit=limit))


@user_router.get(
    "/subjects/{slug}/decks/{deck_id}/questions",
    response_model=ApiResponse[Any],
    summary="List deck questions (full or paginated)",
    description=(
        "Without `page`: returns `data` as a full list (legacy). "
        "With `page`: returns `data` as an object with `items`, `page`, `limit`, `total`, "
        "`totalPages`, `hasNext`, `hasPrevious`. When `page` is set, `limit` defaults to 1 (one question per page)."
    ),
)
def subject_deck_questions(
    slug: str,
    deck_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_course_access),
    page: int | None = Query(default=None, ge=1),
    limit: int | None = Query(default=None, ge=1, le=50),
):
    if page is None:
        data = get_deck_questions(db, slug, deck_id)
        return success_response(data=data)
    effective_limit = 1 if limit is None else limit
    data = get_deck_questions_page(db, slug, deck_id, page=page, limit=effective_limit)
    return success_response(data=data)


@user_router.post(
    "/subjects/{slug}/decks/{deck_id}/questions/{question_id}/check",
    response_model=ApiResponse[AnswerCheckResponse],
)
def subject_deck_question_check(
    slug: str,
    deck_id: str,
    question_id: int = Path(ge=1),
    payload: AnswerCheckRequest = ...,
    db: Session = Depends(get_db),
    _: User = Depends(require_course_access),
):
    data = check_deck_answer(
        db,
        slug=slug,
        deck_id=deck_id,
        question_id=question_id,
        selected_answer=payload.selectedAnswer,
    )
    return success_response(data=data, message="Checked answer successfully")


@user_router.put("/subjects/{slug}/decks/{deck_id}/progress", response_model=ApiResponse[dict])
def subject_deck_progress_update(
    slug: str,
    deck_id: str,
    payload: DeckProgressUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_course_access),
):
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
def subject_deck_progress_get(
    slug: str,
    deck_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_course_access),
):
    data = get_deck_progress(
        db,
        slug=slug,
        deck_id=deck_id,
        user_id=current_user.id,
    )
    return success_response(data=data)


@user_router.put("/subjects/{slug}/decks/{deck_id}/stats", response_model=ApiResponse[dict])
def subject_deck_stats_update(
    slug: str,
    deck_id: str,
    payload: DeckStatsUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_course_access),
):
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
