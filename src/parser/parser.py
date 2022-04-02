"""Contains the Parser class"""

from typing import Optional, Callable, Any

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
        terminal = self.read_conditional(Parser._read_terminal)
        if terminal is None and required:
            raise(ValueError(
                "Expected a terminal symbol definition at "
                f"file position {self._grammar_file.pos}."
            ))
        return terminal

    # Generic methods dealing with conditionals

    @staticmethod
    def _conditional(
        value: Any,
        predicate: Callable[Any, bool]
    ) -> Optional[Any]:
        """
        Syntax sugar to avoid repeating...
        >>> if not condition(value):
        >>>     return None
        >>> return value

        ...in every read function. Replaced by
        >>> return Parser._conditional(value, condition)
        """

        if predicate(value):
            return value
        return None

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

    # Methods to read characters or sequences

    @staticmethod
    def _read_terminal_quote(file: BinaryFile) -> Optional[str]:
        return Parser._conditional(file.read(1), Parser._is_terminal_quote)

    @staticmethod
    def _read_character(file: BinaryFile) -> Optional[str]:
        return Parser._conditional(file.read(1), Parser._is_character)

    @staticmethod
    def _read_terminal(file: BinaryFile) -> Optional[str]:

        # Read left quote
        left_quote = Parser._read_terminal_quote(file)
        if left_quote is None:
            return None

        # Read the terminal character
        ch = Parser._read_character(file)
        if ch is None:
            return None

        # Read the right quote
        right_quote = Parser._read_terminal_quote(file)
        if left_quote == right_quote:  # 'X" is invalid
            return ch
        return None
