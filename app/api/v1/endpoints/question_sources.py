from fastapi import APIRouter, Depends, File, UploadFile
from fastapi import Form
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.question_source import (
    SourceQuestionBulkUpdateRequest,
    SourceStateQuestion,
    SourceStateResponse,
    SubjectDeck,
    SubjectSummary,
    UploadSourceResponse,
)
from app.services import (
    delete_source,
    get_deck_questions,
    get_source_state,
    get_subject_bank,
    get_subject_decks,
    ingest_markdown_file,
    list_subjects as service_list_subjects,
    update_source_from_markdown,
    update_source_questions,
)

router = APIRouter(prefix="/v1", tags=["Question Sources"])


@router.post("/question-sources/upload", response_model=ApiResponse[UploadSourceResponse])
def upload_source_markdown(
    file: UploadFile = File(...),
    subject_slug: str | None = Form(default=None, alias="subjectSlug"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    data = ingest_markdown_file(db, file, current_admin.id, subject_slug=subject_slug)
    return success_response(data=data, message="Upload and parse markdown succeeded")


@router.get("/subjects", response_model=ApiResponse[list[SubjectSummary]])
def list_subjects(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    data = service_list_subjects(db)
    return success_response(data=data)


@router.get("/subjects/{slug}/source-state", response_model=ApiResponse[SourceStateResponse])
def source_state(slug: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    data = get_source_state(db, slug)
    return success_response(data=data)


@router.get("/subjects/{slug}/bank", response_model=ApiResponse[list[SourceStateQuestion]])
def subject_bank(slug: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    data = get_subject_bank(db, slug)
    return success_response(data=data)


@router.get("/subjects/{slug}/decks", response_model=ApiResponse[list[SubjectDeck]])
def subject_decks(slug: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    data = get_subject_decks(db, slug)
    return success_response(data=data)


@router.get("/subjects/{slug}/decks/{deck_id}/questions", response_model=ApiResponse[list[SourceStateQuestion]])
def subject_deck_questions(slug: str, deck_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    data = get_deck_questions(db, slug, deck_id)
    return success_response(data=data)


@router.put("/subjects/{slug}/sources/{source_id}/questions", response_model=ApiResponse[dict])
def update_questions_by_source(
    slug: str,
    source_id: str,
    payload: SourceQuestionBulkUpdateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    data = update_source_questions(
        db,
        slug=slug,
        source_id=source_id,
        questions=[item.model_dump() for item in payload.questions],
    )
    return success_response(data=data, message="Source questions updated successfully")


@router.put("/subjects/{slug}/sources/{source_id}/upload", response_model=ApiResponse[UploadSourceResponse])
def update_source_by_markdown_upload(
    slug: str,
    source_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    data = update_source_from_markdown(
        db,
        slug=slug,
        source_id=source_id,
        file=file,
    )
    return success_response(data=data, message="Source markdown updated successfully")


@router.delete("/subjects/{slug}/sources/{source_id}", response_model=ApiResponse[dict])
def delete_source_endpoint(
    slug: str,
    source_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    data = delete_source(db, slug=slug, source_id=source_id)
    return success_response(data=data, message="Source deleted permanently")
