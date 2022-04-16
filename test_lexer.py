from lexer import Token, TokenType, ListLexer


class TestLexer:
    def test_next_token(self):
        lexer = ListLexer('[ab, c,\td\r\n,e ]')
        expected = [
            Token(TokenType.LBRACK, '['),
            Token(TokenType.VAR, 'ab'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.VAR, 'c'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.VAR, 'd'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.VAR, 'e'),
            Token(TokenType.RBRACK, ']')
        ]
        results = []
        while (token := lexer.next_token()) is not None:
            results.append(token)

        assert results == expected
