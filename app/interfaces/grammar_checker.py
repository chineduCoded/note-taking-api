from typing import Protocol
from app.utils.language_code import LanguageCode
from app.schemas.grammar_schema import GrammarCheckResponse

class GrammarChecker(Protocol):
    @staticmethod
    def check_grammar(md_file: str, lang: LanguageCode = LanguageCode.AUTO) -> GrammarCheckResponse:
        ...