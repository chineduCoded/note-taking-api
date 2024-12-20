from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, status, Form, UploadFile, File, Depends
from sqlmodel import Session

from app.utils.cache_redis import CacheHandler
from app.db import get_session
from app.models import Note
from app.schemas.note_schema import NoteCreate, NoteSaveResponse
from app.schemas.grammar_schema import GrammarCheckResponse
from app.utils.generate_cache_key import generate_cache_key
from app.utils.language_code import LanguageCode
from app.utils.note_util import NoteUtilities
from app.interfaces.grammar_checker import GrammarChecker
from app.dependencies import get_grammar_checker

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()
cache = CacheHandler(redis_host="localhost", redis_port=6379, expiry_time=300)


@router.post("/notes/check-grammar", response_model=GrammarCheckResponse, summary="Grammar check endpoint")
async def grammar_check(
    *,
    md_file: Optional[UploadFile] = File(None),
    md_text: Optional[str] = Form(default=None),
    lang: LanguageCode = Form(LanguageCode.AUTO),
    grammar_checker: Annotated[GrammarChecker, Depends(get_grammar_checker)]
):
    """
    #### Grammar check endpoint for markdown content

    #### Supports:

    - Markdown file upload
    - Markdown text input
    - Language-specific grammar checking

    #### Args:
    - md_file (UploadFile): Markdown file uploaded (optional). Default is None
    - md_text (str): Markdown text input (optional). Default is None
    - lang (LanguageCode): Language code to use for grammar checking. Default is "auto".
        
    #### Returns:
    - Structured grammar check results
    """
    
    # Process markdown content
    content = await NoteUtilities.process_markdown_content(md_file, md_text)

    try:

        cache_key = generate_cache_key(content, "file" if md_file else "text")
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        # Perform grammar check
        grammar_result = grammar_checker.check_grammar(content, lang)

        cache.set(cache_key, grammar_result.model_dump())

        return grammar_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )


@router.post("/notes/save", response_model=NoteSaveResponse, summary="Save note")
async def save_note(note: NoteCreate, session: SessionDep):
    """Save note text"""
    db_note = Note.model_validate(note)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return {
        "note_id": db_note.id,
        "message": "Note saved successfully"
    }


@router.get("/notes/list")
async def get_notes():
    """Get all notes"""
    return "notes"


@router.get("/notes/{note_id}/render")
async def render_markdown(note_id: int):
    """HTML rendering of markdown"""
    return {"html": "html_rendered_markdown"}