import sys
import os

# Fix for Vercel/Root execution: Ensure the 'be' directory is in PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.crud import crud_role, crud_user
from app.db.session import SessionLocal
from app.schemas.api_response import error_response


@asynccontextmanager
async def lifespan(_: FastAPI):
    if SessionLocal is not None:
        db = SessionLocal()
        try:
            crud_user.ensure_block_columns(db)
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
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

if not settings.database_url:
    raise RuntimeError("DATABASE_URL is required for Supabase Postgres connection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    message = exc.detail if isinstance(exc.detail, str) else "Yêu cầu thất bại"
    payload = error_response(message=message, code=exc.status_code, data=None)
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(Exception)
async def global_exception_handler(_: Request, exc: Exception):
    payload = error_response(message="Lỗi hệ thống nghiêm trọng", code=500, data=None)
    return JSONResponse(status_code=500, content=payload.model_dump())

app.include_router(api_router, prefix=settings.api_prefix)
