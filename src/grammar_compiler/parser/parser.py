"""Contains the Parser class"""

from typing import Optional, Any, List

from .binaryfile import BinaryFile
from .base_reader import BaseReader
from .character_reader import CharacterReader
from .all_reader import AllReader
from .any_reader import AnyReader
from .sequence_reader import SequenceReader


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
        reader = Parser.get_terminal_reader()
        terminal = reader(self._grammar_file)
        if Parser._is_terminal(terminal):
            return terminal[1]  # Returns only the character
        if required:
            raise(ValueError(
                f"Expected terminal symbol at line {self._grammar_file.pos}"
            ))

        return None

    def read_identifier(
        self,
        required: bool = False
    ) -> Optional[str]:
        # Identifier = letter, {letter | digit | "_"}

        reader = Parser.get_identifier_reader()
        identifier = reader(self._grammar_file)
        return ''.join(identifier)

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

    @staticmethod
    def _is_terminal(terminal: List[str]) -> bool:
        if not terminal or len(terminal) < 3:
            return False
        if not Parser._is_terminal_quote(terminal[0]):
            return False
        return terminal[0] == terminal[2]  # Must be same quote

    # Specific methods to generate readers for characters or sequences

    @staticmethod
    def get_terminal_quote_reader() -> BaseReader:
        return CharacterReader(lambda ch: Parser._is_terminal_quote(ch))

    @staticmethod
    def get_character_reader() -> BaseReader:
        return CharacterReader(Parser._is_character)

    @staticmethod
    def get_terminal_reader() -> BaseReader:
        return AllReader([
            Parser.get_terminal_quote_reader(),
            Parser.get_character_reader(),
            Parser.get_terminal_quote_reader()
        ])

    @staticmethod
    def get_identifier_reader() -> BaseReader:
        # Identifier = letter, {letter | digit | "_"}
        return AllReader([
            CharacterReader(Parser._is_letter),
            SequenceReader(AnyReader([
                CharacterReader(Parser._is_letter),
                CharacterReader(Parser._is_digit),
                CharacterReader(Parser._is_underscore)
            ]))
        ])
