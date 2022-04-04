import os
import pytest
from .grammar_compiler.parser import BinaryFile, Parser


def test_parser():
    """
    Test grammars (including grammars containing errors) in
    the test_grammars/ directory.

    For now contains only tests for very simple grammars (only one
    terminal symbol definition).
    """
    directory = "test_grammars"
    file_data = [
        ("single_terminal_1.grm", '['),
        ("single_terminal_2.grm", 'p'),
        ("bad_terminal_1.grm", None),
        ("bad_terminal_2.grm", None),
    ]
    for file_name, expected_grammar in file_data:
        with BinaryFile(os.path.join(directory, file_name), "r") as file:
            parser = Parser(file)
            if expected_grammar is not None:
                parser.parse()
                assert(expected_grammar == parser.grammar)
            else:
                with pytest.raises(ValueError):
                    parser.parse()


if __name__ == '__main__':
    test_parser()
