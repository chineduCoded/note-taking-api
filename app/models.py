from datetime import datetime, timezone
from sqlmodel import Field
from app.schemas.note_schema import NoteBase

class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc))