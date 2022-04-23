import pytest

from core.lexer import Token, TokenType, ListLexer


class TestLexer:
    @staticmethod
    def _lexer_test_cases() -> list[tuple]:
        return [
            # complex case
            ('[ab, c,\td=e\r\n,f]', [
                Token(TokenType.LBRACK, '['),
                Token(TokenType.VAR, 'ab'),
                Token(TokenType.COMMA, ','),
                Token(TokenType.VAR, 'c'),
                Token(TokenType.COMMA, ','),
                Token(TokenType.VAR, 'd'),
                Token(TokenType.EQUAL, '='),
                Token(TokenType.VAR, 'e'),
                Token(TokenType.COMMA, ','),
                Token(TokenType.VAR, 'f'),
                Token(TokenType.RBRACK, ']'),
            ]),
            # starts and ends with var
            ('a, b, def', [
                Token(TokenType.VAR, 'a'),
                Token(TokenType.COMMA, ','),
                Token(TokenType.VAR, 'b'),
                Token(TokenType.COMMA, ','),
                Token(TokenType.VAR, 'def'),
            ]),
            # starts and ends with whitespace
            (' a, b, def ', [
                Token(TokenType.VAR, 'a'),
                Token(TokenType.COMMA, ','),
                Token(TokenType.VAR, 'b'),
                Token(TokenType.COMMA, ','),
                Token(TokenType.VAR, 'def'),
            ]),
        ]

    @pytest.mark.parametrize('input_text,expected', _lexer_test_cases())
    def test_next_token(self, input_text, expected):
        lexer = ListLexer(input_text)
        results = []
        while (token := lexer.next_token()).type != TokenType.EOF:
            results.append(token)

        assert results == expected
