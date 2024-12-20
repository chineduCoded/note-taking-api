from sqlmodel import SQLModel
from typing import List

class ErrorResponse(SQLModel):
    status: str
    message: str
    status_code: int

class ValidationErrorDetail(SQLModel):
    field: str
    message: str

class ValidationErrorResponse(SQLModel):
    errors: List[ValidationErrorDetail]