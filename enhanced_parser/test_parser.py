import pytest

from core.lexer import ListLexer
from .parser import Parser, ParserException


class TestListParser:
    @staticmethod
    def _parse_success_test_cases() -> list[tuple[str]]:
        return [
            ('[]',),
            ('[a]',),
            ('[a, b, c]',),
            ('[a, b, c=d]',),
            ('[a, [b, c, d=e], [f=g]]',),
            ('[a, [], []]',),
        ]

    @staticmethod
    def _parse_fail_test_cases() -> list[tuple[str]]:
        return [
            ('[',),
            (']',),
            ('[a, b, c,]',),
            ('[a, [, c]',),
            ('[a, b, c][',),
            ('[a, b=, c]',),
        ]

    @pytest.mark.parametrize('input_list', _parse_success_test_cases())
    def test_parse_success(self, input_list):
        for input_text in input_list:
            lexer = ListLexer(input_text)
            parser = Parser(lexer)
            parser.parse()

    @pytest.mark.parametrize('input_list', _parse_fail_test_cases())
    def test_parse_fail(self, input_list):
        for input_text in input_list:
            lexer = ListLexer(input_text)
            parser = Parser(lexer)
            with pytest.raises(ParserException):
                parser.parse()
