from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .routers import notes
from .db import create_db_and_tables
from app.schemas.errors_schema import ValidationErrorDetail, ValidationErrorResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # Clean up code here

app = FastAPI(lifespan=lifespan, title="Notes Taking API", version="0.1.0")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = error["loc"][-1]
        msg = error["msg"]
        errors.append(ValidationErrorDetail(field=field, message=msg))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ValidationErrorResponse(errors=errors).model_dump(),
    )

@app.get("/")
async def read_root():
    return {"status": "Running"}

app.include_router(notes.router, tags=["notes"])
