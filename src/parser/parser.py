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
        self.grammar = None

    def parse(self):
        """
        Main function to parse a grammar file. Should evolve when more
        parsing features will be available.

        For now the Parser can only read one terminal symbol definition
        to test the very first reading function implemented.
        """
        self.grammar = self.read_terminal(required=True)

    def read_terminal(
        self,
        required: bool = False
    ) -> Optional[str]:
        """
        Tries to read a terminal symbol definition ('X' or "X") and
        returns the symbol.
        """
        terminal = self.read_conditional(
            Parser._read_terminal(self._grammar_file)
        )
        if terminal is None and required:
            raise(ValueError(
                "Expected a terminal symbol definition at "
                f"file position {self._grammar_file.pos}."
            ))
        return terminal

    def read_conditional(
            self,
            read_function: Callable[BinaryFile, Optional[str]]
    ) -> Optional[str]:
        """
        Using a reader function, tries to read a grammar element. If the
        element is successfully read, it is returned. Otherwise the function
        returns None and reset the file cursor position to its value before
        the function call.
        """

        pos = self._grammar_file.pos
        token = read_function(self._grammar_file)
        if not token:
            # Read unsuccessful -> reset cursor position to old value
            self._grammar_file.pos = pos

        return token

    # Methods to infer character type

    @staticmethod
    def _is_character(ch: chr) -> bool:
        return (
            Parser._is_digit(ch)
            or Parser._is_letter(ch)
            or Parser._is_symbol(ch)
            or Parser._is_underscore(ch)
        )

    @staticmethod
    def _is_digit(ch: chr) -> bool:
        return ch.isdigit()

    @staticmethod
    def _is_letter(ch: chr) -> bool:
        return ch.isalpha()

    @staticmethod
    def _is_symbol(ch: chr) -> bool:
        return ch in "'\"(){}[],;|"

    @staticmethod
    def _is_underscore(ch: chr) -> bool:
        return ch == '_'

    @staticmethod
    def _is_terminal_quote(ch: chr) -> bool:
        return ch in ['"', "'"]

    # Methods to read characters

    @staticmethod
    def _read_terminal_quote(file: BinaryFile) -> Optional[str]:
        quote = file.read(1)
        return quote if Parser._is_terminal_quote(quote) else None

    @staticmethod
    def _read_character(file: BinaryFile) -> Optional[str]:
        character = file.read(1)
        return character if Parser._is_character(character) else None

    @staticmethod
    def _read_terminal(file: BinaryFile) -> Optional[str]:
        if Parser._read_terminal_quote() is None:
            return None
        ch = Parser._read_character()
        if ch is None:
            return None
        return ch if Parser._read_terminal_quote() else None
