from pydantic import BaseModel, Field


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


class AdminSourceSummary(BaseModel):
    sourceId: str
    examCode: str
    fileName: str
    questionCount: int
    isAggregatedBank: bool
    uploadedAt: str | None = None


class SourceStateQuestion(BaseModel):
    id: int
    stem: str
    options: list[dict]
    answer: str


class DeckQuestionsPage(BaseModel):
    """Paginated slice of deck questions; `id` on each item is 1-based index in deck order (same as non-paginated GET)."""

    items: list[SourceStateQuestion]
    page: int
    limit: int
    total: int
    totalPages: int
    hasNext: bool
    hasPrevious: bool


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


class DeckProgressStats(BaseModel):
    total: int
    inProgress: int
    completed: int
    learnedCount: int
    completionRatePercent: int


class SubjectDeck(BaseModel):
    deckId: str
    examCode: str
    fileName: str
    questionCount: int
    stats: DeckProgressStats
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


class DeckStatsUpdateRequest(BaseModel):
    inProgress: int = Field(ge=0, le=10000)
    completed: int = Field(ge=0, le=10000)


class DeckProgressUpdateRequest(BaseModel):
    currentQuestion: int = Field(ge=0, le=10000)
    attemptedQuestionOrdinals: list[int] = Field(default_factory=list, max_length=10000)


class DeckProgressResponse(BaseModel):
    currentQuestion: int
    attemptedQuestionOrdinals: list[int]
    updatedAt: str | None = None


class AnswerCheckRequest(BaseModel):
    selectedAnswer: str = Field(min_length=1)


class AnswerCheckResponse(BaseModel):
    questionId: int
    selectedAnswer: str
    correctAnswers: list[str]
    isCorrect: bool
