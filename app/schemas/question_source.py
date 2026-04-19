from pydantic import BaseModel


class UploadSourceResponse(BaseModel):
    sourceId: str
    subjectSlug: str
    subjectCode: str
    examCode: str
    fileName: str
    checksum: str
    questionCount: int
    warnings: list[str]
    deduplicated: bool = False


class SubjectSummary(BaseModel):
    slug: str
    code: str
    hint: str


class SourceStateQuestion(BaseModel):
    id: int
    stem: str
    options: list[dict]
    answer: str


class SourceFileMeta(BaseModel):
    class SourceRange(BaseModel):
        start: int
        end: int

    fileName: str
    isEmpty: bool
    questionCount: int
    range: SourceRange


class SourceStateResponse(BaseModel):
    bankQuestions: list[SourceStateQuestion]
    deckQuestions: list[SourceStateQuestion]
    files: list[SourceFileMeta]
    hocTheoDeLayout: str


class SubjectDeck(BaseModel):
    deckId: str
    examCode: str
    fileName: str
    questionCount: int
    uploadedAt: str | None = None


class SourceQuestionOptionInput(BaseModel):
    label: str
    text: str


class SourceQuestionUpdateInput(BaseModel):
    stem: str
    options: list[SourceQuestionOptionInput]
    answer: str


class SourceQuestionBulkUpdateRequest(BaseModel):
    questions: list[SourceQuestionUpdateInput]
