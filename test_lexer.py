from lexer import Token, TokenType, ListLexer


class TestLexer:
    def test_next_token(self):
        lexer = ListLexer('[ab, c, d]')
        expected_tokens = [
            Token(TokenType.LBRACK, '['),
            Token(TokenType.VAR, 'ab'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.VAR, 'c'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.VAR, 'd'),
            Token(TokenType.RBRACK, ']')
        ]
        i = 0
        while (token := lexer.next_token()) is not None:
            assert token == expected_tokens[i]
            i += 1
