import sys
import os

# Fix for Vercel/Root execution: ensure project root is on PYTHONPATH for `app.*` imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.crud import crud_otp, crud_question_source, crud_role, crud_user
from app.middleware.docs_basic_auth import DocsBasicAuthMiddleware
from app.db.session import SessionLocal
from app.schemas.api_response import error_response


@asynccontextmanager
async def lifespan(_: FastAPI):
    should_bootstrap = settings.run_startup_bootstrap and os.getenv("VERCEL") != "1"

    if SessionLocal is not None and should_bootstrap:
        db = SessionLocal()
        try:
            crud_user.ensure_block_columns(db)
            crud_user.ensure_course_access_columns(db)
            crud_user.ensure_otp_columns(db)
            crud_otp.ensure_otp_verification_columns(db)
            crud_question_source.ensure_tables(db)
            crud_role.ensure_seed_roles(db)
            crud_user.get_or_create(db, settings.seed_admin_email.lower(), "admin")
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    yield

app = FastAPI(
    title=settings.app_name,
    docs_url="/api/docs" if settings.api_docs_enabled else None,
    openapi_url="/api/openapi.json" if settings.api_docs_enabled else None,
    redoc_url="/api/redoc" if settings.api_docs_enabled else None,
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
async def root_health():
    return {"service": settings.app_name, "status": "ok"}

if not settings.database_url:
    raise RuntimeError("DATABASE_URL is required for Supabase Postgres connection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.docs_basic_auth_enabled:
    app.add_middleware(
        DocsBasicAuthMiddleware,
        username=settings.docs_basic_auth_user.strip(),
        password=settings.docs_basic_auth_password.strip(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    payload = error_response(
        message="Dữ liệu đầu vào không hợp lệ",
        code=422,
        data=exc.errors(),
    )
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        response = JSONResponse(status_code=exc.status_code, content=exc.detail)
    else:
        message = exc.detail if isinstance(exc.detail, str) else "Yêu cầu thất bại"
        payload = error_response(message=message, code=exc.status_code, data=None)
        response = JSONResponse(status_code=exc.status_code, content=payload.model_dump())

    auth_clear_details = {"Could not validate credentials", "Tài khoản đã bị khóa"}
    should_clear_auth_cookie = exc.status_code == 401 or (exc.status_code == 403 and exc.detail in auth_clear_details)
    if should_clear_auth_cookie:
        response.delete_cookie("auth_token", path="/")
        response.delete_cookie("refresh_token", path="/")

    return response


@app.exception_handler(Exception)
async def global_exception_handler(_: Request, exc: Exception):
    payload = error_response(message="Lỗi hệ thống nghiêm trọng", code=500, data=None)
    return JSONResponse(status_code=500, content=payload.model_dump())

app.include_router(api_router, prefix=settings.api_prefix)
