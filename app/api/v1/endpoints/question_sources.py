from fastapi import APIRouter, Depends, File, Path, UploadFile
from fastapi import Form
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, require_course_access
from app.db.session import get_db
from app.models.user import User
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.question_source import (
    AdminSourceSummary,
    AnswerCheckRequest,
    AnswerCheckResponse,
    DeckProgressUpdateRequest,
    DeckProgressResponse,
    DeckStatsUpdateRequest,
    SourceQuestionBulkUpdateRequest,
    SourceStateQuestion,
    SourceStateResponse,
    SubjectDeck,
    SubjectSummary,
    UploadSourceResponse,
)
from app.services import (
    check_deck_answer,
    delete_source,
    get_admin_subject_sources,
    get_deck_questions,
    get_source_state,
    get_subject_bank,
    get_subject_decks,
    ingest_markdown_file,
    list_subjects as service_list_subjects,
    update_deck_progress,
    get_deck_progress,
    update_deck_stats,
    update_source_from_markdown,
    update_source_questions,
)

user_router = APIRouter(prefix="/v1", tags=["Question Sources"])
admin_router = APIRouter(prefix="/v1", tags=["Admin — Question Sources"])
router = APIRouter()


def _upload_source_markdown_impl(
    *,
    db: Session,
    file: UploadFile,
    current_admin: User,
    subject_slug: str | None,
) -> ApiResponse[UploadSourceResponse]:
    data = ingest_markdown_file(db, file, current_admin.id, subject_slug=subject_slug)
    return success_response(data=data, message="Upload and parse markdown succeeded")


@admin_router.post("/admin/question-sources/upload", response_model=ApiResponse[UploadSourceResponse])
def admin_upload_source_markdown(
    file: UploadFile = File(...),
    subject_slug: str | None = Form(default=None, alias="subjectSlug"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return _upload_source_markdown_impl(
        db=db,
        file=file,
        current_admin=current_admin,
        subject_slug=subject_slug,
    )


@admin_router.post(
    "/question-sources/upload",
    response_model=ApiResponse[UploadSourceResponse],
    include_in_schema=False,
    deprecated=True,
)
def legacy_upload_source_markdown(
    file: UploadFile = File(...),
    subject_slug: str | None = Form(default=None, alias="subjectSlug"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return _upload_source_markdown_impl(
        db=db,
        file=file,
        current_admin=current_admin,
        subject_slug=subject_slug,
    )


@user_router.get("/subjects", response_model=ApiResponse[list[SubjectSummary]])
def list_subjects(db: Session = Depends(get_db), _: User = Depends(require_course_access)):
    data = service_list_subjects(db)
    return success_response(data=data)


@admin_router.get("/admin/question-sources/subjects", response_model=ApiResponse[list[SubjectSummary]])
def admin_list_subjects(db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    data = service_list_subjects(db)
    return success_response(data=data)


@admin_router.get("/admin/question-sources/subjects/{slug}/sources", response_model=ApiResponse[list[AdminSourceSummary]])
def admin_subject_sources(slug: str, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    data = get_admin_subject_sources(db, slug)
    return success_response(data=data)


@user_router.get("/subjects/{slug}/source-state", response_model=ApiResponse[SourceStateResponse])
def source_state(slug: str, db: Session = Depends(get_db), _: User = Depends(require_course_access)):
    data = get_source_state(db, slug)
    return success_response(data=data)


@user_router.get("/subjects/{slug}/bank", response_model=ApiResponse[list[SourceStateQuestion]])
def subject_bank(slug: str, db: Session = Depends(get_db), _: User = Depends(require_course_access)):
    data = get_subject_bank(db, slug)
    return success_response(data=data)


@user_router.get("/subjects/{slug}/decks", response_model=ApiResponse[list[SubjectDeck]])
def subject_decks(slug: str, db: Session = Depends(get_db), current_user: User = Depends(require_course_access)):
    data = get_subject_decks(db, slug, user_id=current_user.id)
    return success_response(data=data)


@user_router.get("/subjects/{slug}/decks/{deck_id}/questions", response_model=ApiResponse[list[SourceStateQuestion]])
def subject_deck_questions(slug: str, deck_id: str, db: Session = Depends(get_db), _: User = Depends(require_course_access)):
    data = get_deck_questions(db, slug, deck_id)
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


@admin_router.put(
    "/admin/question-sources/subjects/{slug}/sources/{source_id}/questions",
    response_model=ApiResponse[dict],
)
def admin_update_questions_by_source(
    slug: str,
    source_id: str,
    payload: SourceQuestionBulkUpdateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return _update_questions_by_source_impl(
        db=db,
        slug=slug,
        source_id=source_id,
        payload=payload,
    )


def _update_questions_by_source_impl(
    *,
    db: Session,
    slug: str,
    source_id: str,
    payload: SourceQuestionBulkUpdateRequest,
) -> ApiResponse[dict]:
    data = update_source_questions(
        db,
        slug=slug,
        source_id=source_id,
        questions=[item.model_dump() for item in payload.questions],
    )
    return success_response(data=data, message="Source questions updated successfully")


@admin_router.put(
    "/subjects/{slug}/sources/{source_id}/questions",
    response_model=ApiResponse[dict],
    include_in_schema=False,
    deprecated=True,
)
def legacy_update_questions_by_source(
    slug: str,
    source_id: str,
    payload: SourceQuestionBulkUpdateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return _update_questions_by_source_impl(db=db, slug=slug, source_id=source_id, payload=payload)


@admin_router.put(
    "/admin/question-sources/subjects/{slug}/sources/{source_id}/upload",
    response_model=ApiResponse[UploadSourceResponse],
)
def admin_update_source_by_markdown_upload(
    slug: str,
    source_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return _update_source_by_markdown_upload_impl(db=db, slug=slug, source_id=source_id, file=file)


def _update_source_by_markdown_upload_impl(
    *,
    db: Session,
    slug: str,
    source_id: str,
    file: UploadFile,
) -> ApiResponse[UploadSourceResponse]:
    data = update_source_from_markdown(
        db,
        slug=slug,
        source_id=source_id,
        file=file,
    )
    return success_response(data=data, message="Source markdown updated successfully")


@admin_router.put(
    "/subjects/{slug}/sources/{source_id}/upload",
    response_model=ApiResponse[UploadSourceResponse],
    include_in_schema=False,
    deprecated=True,
)
def legacy_update_source_by_markdown_upload(
    slug: str,
    source_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return _update_source_by_markdown_upload_impl(db=db, slug=slug, source_id=source_id, file=file)


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


@admin_router.delete(
    "/subjects/{slug}/sources/{source_id}",
    response_model=ApiResponse[dict],
    include_in_schema=False,
    deprecated=True,
)
def legacy_delete_source_endpoint(
    slug: str,
    source_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return _delete_source_impl(db=db, slug=slug, source_id=source_id)


router.include_router(user_router)
router.include_router(admin_router)
