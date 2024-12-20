import re
from typing import Optional

from fastapi import UploadFile, HTTPException, status
import magic
from mistune import create_markdown
from mistune.renderers.html import HTMLRenderer


class NoteUtilities:
    """
    Utility functions for note operations
    """
    
    @staticmethod
    async def validate_markdown_file(md_file: UploadFile):
        """
        Comprehensive markdown file validation
        
        Args:
            md_file (UploadFile): Uploaded file to validate
        
        Raises:
            HTTPException: If file fails validation
        """
        # Validate file extension
        ALLOWED_EXTENSIONS = ('.md', '.markdown', '.mdown', '.mkdn')
        if not any(md_file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only markdown files are allowed"
            )
        
        # Validate file MIME type using python-magic
        file_mime = magic.from_buffer(await md_file.read(2048), mime=True)
        allowed_mimes = [
            'text/markdown', 
            'text/x-markdown', 
            'text/plain'
        ]
        if file_mime not in allowed_mimes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Must be a markdown file"
            )
        
        # Reset file pointer
        await md_file.seek(0)
        
        # File size validation
        max_file_size = 5 * 1024 * 1024  # 5 MB
        file_size = len(await md_file.read())
        await md_file.seek(0)
        
        if file_size > max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File exceeds 5MB limit"
            )
    
    @staticmethod
    async def process_markdown_content(
        md_file: Optional[UploadFile] = None, 
        md_text: Optional[str] = None
    ) -> str:
        """
        Process markdown content from file or text input
        
        Args:
            md_file (Optional[UploadFile]): Markdown file
            md_text (Optional[str]): Markdown text
        
        Returns:
            str: Processed markdown content
        
        Raises:
            HTTPException: If no content or invalid content
        """
        if not md_file and not md_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either markdown file or text must be provided"
            )
        
        if md_file:
            # Validate markdown file
            await NoteUtilities.validate_markdown_file(md_file)
            
            # Read file content
            try:
                content = await md_file.read()
                content = content.decode('utf-8')
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File must be UTF-8 encoded"
                )
        else:
            # Validate markdown text
            if not NoteUtilities.is_valid_markdown(md_text):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid markdown content"
                )
            content = md_text
        
        return content
    
    @staticmethod
    def is_valid_markdown(text: str) -> bool:
        """
        Validate markdown content. Ensures the text includes markdown elements.
        
        Args:
            text (str): Markdown text to validate.
        
        Returns:
            bool: Whether the text is valid markdown.
        """
        if not text.strip():
            return False

        # Regex to detect basic markdown syntax
        markdown_patterns = [
            r"^#{1,6}\s",  # Headers (e.g., # Header, ## Subheader)
            r"(\*|-)\s",  # Unordered lists
            r"\d+\.\s",  # Ordered lists
            r"\[.*\]\(.*\)",  # Links (e.g., [text](url))
            r"`.*?`",  # Inline code
            r"\*\*.*?\*\*",  # Bold text
            r"\*.*?\*",  # Italic text
        ]

        if not any(re.search(pattern, text, re.MULTILINE) for pattern in markdown_patterns):
            return False

        try:
            markdown = create_markdown(renderer=HTMLRenderer())
            html = markdown(text)
            # Ensure the rendered HTML contains meaningful content
            return bool(html.strip() and html != text)
        except Exception as e:
            print(f"Markdown parsing error: {e}")
            return False