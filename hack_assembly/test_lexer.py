import pytest

from .lexer import Lexer
from .lexer import LexerNextTokenException
from .lexer import Token, TokenType


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
            ('MD=D-A+!M', [
                Token(TokenType.REG_MULTI, 'MD'),
                Token(TokenType.EQUAL, '='),
                Token(TokenType.REG_ONE, 'D'),
                Token(TokenType.MINUS, '-'),
                Token(TokenType.REG_ONE, 'A'),
                Token(TokenType.PLUS, '+'),
                Token(TokenType.NOT, '!'),
                Token(TokenType.REG_ONE, 'M'),
            ]),
            ('AMD=D&123 | A;', [
                Token(TokenType.REG_MULTI, 'AMD'),
                Token(TokenType.EQUAL, '='),
                Token(TokenType.REG_ONE, 'D'),
                Token(TokenType.AND, '&'),
                Token(TokenType.INT, '123'),
                Token(TokenType.OR, '|'),
                Token(TokenType.REG_ONE, 'A'),
                Token(TokenType.SEMICOLON, ';'),
            ]),
            ('0;JMP D;JGT', [
                Token(TokenType.INT, '0'),
                Token(TokenType.SEMICOLON, ';'),
                Token(TokenType.JUMP, 'JMP'),
                Token(TokenType.REG_ONE, 'D'),
                Token(TokenType.SEMICOLON, ';'),
                Token(TokenType.JUMP, 'JGT'),
            ]),
            ('D=R0+SP', [
                Token(TokenType.REG_ONE, 'D'),
                Token(TokenType.EQUAL, '='),
                Token(TokenType.PREDEFINED, 'R0'),
                Token(TokenType.PLUS, '+'),
                Token(TokenType.PREDEFINED, 'SP'),
            ]),
            ('(LOOP)', [
                Token(TokenType.LPAREN, '('),
                Token(TokenType.VAR, 'LOOP'),
                Token(TokenType.RPAREN, ')'),
            ]),
            ('''
            (LOOP)
             
            D=R0+1
            ''', [
                Token(TokenType.LPAREN, '('),
                Token(TokenType.VAR, 'LOOP'),
                Token(TokenType.RPAREN, ')'),
                Token(TokenType.NEWLINE, ''),
                Token(TokenType.REG_ONE, 'D'),
                Token(TokenType.EQUAL, '='),
                Token(TokenType.PREDEFINED, 'R0'),
                Token(TokenType.PLUS, '+'),
                Token(TokenType.INT, '1'),
                Token(TokenType.NEWLINE, ''),
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


