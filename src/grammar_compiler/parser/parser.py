"""Contains the Parser class"""

from typing import Optional, List

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
        self.grammar = self.read_grammar(required=True)

    def read_grammar(self, required=True):
        rules = []
        while True:
            rule = self.read_rule(required=False)
            if rule is None:
                break
            rules.append(rule)
        return rules

    def read_rule(self, required=True):
        identifier = self.read_identifier(required=required)
        if identifier is None:
            return None
        self.read_assignement(required=True)
        terminal = self.read_terminal(required=True)

        return {
            'identifier': identifier,
            'terminal': terminal
        }

    def read_identifier(
        self,
        required: bool = True
    ) -> Optional[str]:
        identifier_parser = Parser.get_identifier_reader()
        parsed_identifier = identifier_parser(self._grammar_file)
        if parsed_identifier is None:
            if required:
                raise(ValueError(
                    f"Expected identifier at pos {self._grammar_file.pos}"))
            return None

        return parsed_identifier[0] + ''.join(parsed_identifier[1])

    def read_assignement(
        self,
        required: bool = True
    ) -> None:
        reader = AllReader([
            SequenceReader(CharacterReader(lambda ch: ch == ' ')),
            CharacterReader(lambda ch: ch == '='),
            SequenceReader(CharacterReader(lambda ch: ch == ' ')),
        ])
        res = reader(self._grammar_file)
        if res is None and required:
            raise(ValueError(
                f"Expected assignement at pos {self._grammar_file.pos}"
            ))

    def read_terminal(
        self,
        required: bool = True
    ) -> Optional[str]:
        terminal_reader = Parser.get_terminal_reader()
        parsed_terminal = terminal_reader(self._grammar_file)
        if parsed_terminal is None and required:
            raise(ValueError(
                f"Expected terminal at pos {self._grammar_file.pos}"
            ))
        if not Parser._is_terminal(parsed_terminal):
            raise(ValueError(
                f"Bad terminal definition {parsed_terminal}"))
        return parsed_terminal[1]

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
