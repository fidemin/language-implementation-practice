import pytest

from lexer import ListLexer
from parser import ListParser, ListParserException


class TestListParser:
    @staticmethod
    def _parse_success_test_cases() -> list[tuple[str]]:
        return [
            ('[]',),
            ('[a]',),
            ('[a, b, c]',),
            ('[a, [b, c, d], [e]]',),
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
        ]

    @pytest.mark.parametrize('input_list', _parse_success_test_cases())
    def test_parse_success(self, input_list):
        for input_text in input_list:
            lexer = ListLexer(input_text)
            parser = ListParser(lexer)
            parser.parse()

    @pytest.mark.parametrize('input_list', _parse_fail_test_cases())
    def test_parse_fail(self, input_list):
        for input_text in input_list:
            lexer = ListLexer(input_text)
            parser = ListParser(lexer)
            with pytest.raises(ListParserException):
                parser.parse()
