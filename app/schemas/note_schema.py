from sqlmodel import SQLModel, Field

class NoteBase(SQLModel):
    title: str = Field(nullable=False, index=True)
    content: str = Field(nullable=False)


class NoteCreate(NoteBase):
    pass

class NoteSaveResponse(SQLModel):
    note_id: int
    message: str

class NotePublic(NoteBase):
    note_id: int
    created_at: str