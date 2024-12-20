import language_tool_python

from app.utils.language_code import LanguageCode
from app.schemas.grammar_schema import GrammarCheckResponse


def get_surrounding_context(text: str, line: int, lines_before: int = 2, lines_after: int = 2) -> str:
    """Get surrounding lines for context."""
    lines = text.split("\n")
    start = max(0, line - lines_before - 1)
    end = min(len(lines), line + lines_after)
    return "\n".join(lines[start:end])


class NoteGrammarService:
    @staticmethod
    def check_grammar(md_file: str, lang: LanguageCode = LanguageCode.AUTO) -> GrammarCheckResponse:
        """
        Perform grammar checking on content
        
        Args:
            content (str): Text to check
            lang (LanguageCode): Language for grammar check
        
        Returns:
            GrammarCheckResponse: Grammar check results
        """
        try:
            with language_tool_python.LanguageTool(lang, config={"cacheSize": 1000, "pipelineCaching": True}) as tool:
                matches = tool.check(md_file)
                errors = []
                for match in matches:
                    line_number = md_file[:match.offset].count("\n") + 1
                    column_number = match.offset - md_file.rfind("\n", 0, match.offset)
                    # context_snippet = get_surrounding_context(md_file, line_number)
                    errors.append({
                        "line": line_number,
                        "column": column_number,
                        "message": match.message,
                        "suggestion": match.replacements[0] if match.replacements else None,
                        "context": match.context,
                    })
        except Exception as e:
            raise RuntimeError(f"LanguageTool initialization failed: {str(e)}")
        
        return GrammarCheckResponse(
            has_errors=bool(errors),
            total_issues=len(errors),
            errors=errors,
            message="Grammar check completed" if not errors else None
        )