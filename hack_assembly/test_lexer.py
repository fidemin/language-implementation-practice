from .lexer import Token, TokenType
from .lexer import Lexer
from .lexer import LexerNextTokenException

import pytest


class TestLexer:
    @staticmethod
    def _lexer_success_test_cases() -> list[tuple]:
        return [
            ('@aBc', [
                Token(TokenType.AT, '@'),
                Token(TokenType.VAR, 'aBc')
            ]),
            ('@132', [
                Token(TokenType.AT, '@'),
                Token(TokenType.INT, '132')
            ]),
            ('ab123cde', [
                Token(TokenType.VAR, 'ab123cde'),
            ]),
            ('ab123 @ 123', [
                Token(TokenType.VAR, 'ab123'),
                Token(TokenType.AT, '@'),
                Token(TokenType.INT, '123'),
            ]),
            ('MD=-A', [
                Token(TokenType.REG2, 'MD'),
                Token(TokenType.EQUAL, '='),
                Token(TokenType.MINUS, '-'),
                Token(TokenType.REG1, 'A'),
            ]),
        ]

    @staticmethod
    def _lexer_fail_test_cases() -> list[tuple]:
        return [
            ('@123abc', LexerNextTokenException),
        ]

    @pytest.mark.parametrize('input_text,expected', _lexer_success_test_cases())
    def test_next_token_success(self, input_text, expected):
        lexer = Lexer(input_text)
        results = []
        while (token := lexer.next_token()).type != TokenType.EOF:
            results.append(token)

        assert results == expected

    @pytest.mark.parametrize('input_text,expected_exception', _lexer_fail_test_cases())
    def test_next_token_fail(self, input_text, expected_exception):
        lexer = Lexer(input_text)

        with pytest.raises(expected_exception):
            while lexer.next_token().type != TokenType.EOF:
                lexer.next_token()


