from typing import Optional
from sqlmodel import SQLModel


class GrammarCheckResponse(SQLModel):
    has_errors: bool
    total_issues: int
    errors: Optional[list] = []
    message: Optional[str] = None