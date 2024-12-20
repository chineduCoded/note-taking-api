from app.interfaces.grammar_checker import GrammarChecker
from app.services.grammar_service import NoteGrammarService

def get_grammar_checker() -> GrammarChecker:
    return NoteGrammarService