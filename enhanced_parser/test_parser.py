import pytest

from core.lexer import ListLexer
from .parser import Parser, SpeculationException


class TestListParser:
    @staticmethod
    def _parse_success_test_cases() -> list[str]:
        return [
            '[]',
            '[a]',
            '[a, b, c]',
            '[a, b, c=d]',
            '[a, [b, c, d=e], [f=g]]',
            '[a, [], []]',
            '[a, b]=[c, d]',
            '[a, b]=[[c], [de=f]]',
        ]

    @staticmethod
    def _parse_fail_test_cases() -> list[str]:
        return [
            '[',
            ']',
            '[a, b, c,]',
            '[a, [, c]',
            '[a, b, c][',
            '[a, b=, c]',
            '[a, b]=[c, d',
            '[a, b]=[[c], de=f]]',
        ]

    @pytest.mark.parametrize('input_text', _parse_success_test_cases())
    def test_parse_success(self, input_text):
        lexer = ListLexer(input_text)
        parser = Parser(lexer)
        parser.parse()

    @pytest.mark.parametrize('input_text', _parse_fail_test_cases())
    def test_parse_fail(self, input_text):
        lexer = ListLexer(input_text)
        parser = Parser(lexer)
        with pytest.raises(SpeculationException):
            parser.parse()
