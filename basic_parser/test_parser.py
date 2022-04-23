import pytest

from core.lexer import ListLexer
from .parser import ListParser, ListParserException


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

    def test_constructor_fail(self):
        lexer = ListLexer('[]')
        with pytest.raises(ListParserException):
            ListParser(lexer, 1)

    @pytest.mark.parametrize('input_list', _parse_success_test_cases())
    def test_parse_success(self, input_list):
        # from k = 2 to k = 4
        for input_text in input_list:
            for i in range(2, 4):
                lexer = ListLexer(input_text)
                parser = ListParser(lexer, i)
                parser.parse()

    @pytest.mark.parametrize('input_list', _parse_fail_test_cases())
    def test_parse_fail_ll(self, input_list):
        # from k = 2 to k = 4
        for input_text in input_list:
            for i in range(2, 4):
                lexer = ListLexer(input_text)
                parser = ListParser(lexer, 2)
                with pytest.raises(ListParserException):
                    parser.parse()
