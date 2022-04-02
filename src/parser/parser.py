"""Contains the Parser class"""
from typing import Optional, Callable

from . import BinaryFile


class Parser:
    """Parses a grammar file"""

    def __init__(
            self,
            grammar_file: BinaryFile
    ):
        self._grammar_file = grammar_file

    def is_terminal(self):
        pass

    def read_conditional(
            self,
            predicate: Callable[bool]
    ) -> Optional[str]:
        pass

    @staticmethod
    def _is_character(ch: chr):
        return (
            Parser._is_digit(ch)
            or Parser._is_letter(ch)
            or Parser._is_symbol(ch)
            or Parser._is_underscore(ch)
        )

    @staticmethod
    def _is_digit(ch: chr):
        Parser._ensure_chr(ch)
        return ch.isdigit()

    @staticmethod
    def _is_letter(ch: chr):
        Parser._ensure_chr(ch)
        return ch.isalpha()

    @staticmethod
    def _is_symbol(ch: chr):
        Parser._ensure_chr(ch)
        return ch in "'\"(){}[],;|"

    @staticmethod
    def _is_underscore(ch: chr):
        Parser._ensure_chr(ch)
        return ch == '_'

    @staticmethod
    def _is_terminal_quote(ch: chr):
        Parser._ensure_chr(ch)
        return ch in ['"', "'"]

    @staticmethod
    def _ensure_chr(ch: chr):
        if not isinstance(ch, chr):
            raise(TypeError(
                f"Expected chr intance, got {ch} (type={type(ch)})"
            ))
