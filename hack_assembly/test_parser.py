import pytest

from .lexer import Lexer
from .parser import Parser


class TestParser:
    @staticmethod
    def _parser_a_instruction_success_test_cases() -> list[str]:
        return [
            '@i',
            '@15',
            '@R0',
            '@SCREEN',
        ]

    @staticmethod
    def _parser_c_instruction_success_test_cases() -> list[str]:
        return [
            'M=1',
            'MD=1',
        ]

    @pytest.mark.parametrize('input_text', _parser_a_instruction_success_test_cases())
    def test_parser_a_instruction_success(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        parser._a_instruction()
