from lexer import Token, TokenType, ListLexer


class TestLexer:
    def test_next_token(self):
        lexer = ListLexer('[ab, c,\td=e\r\n,f ]')
        expected = [
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
            Token(TokenType.RBRACK, ']')
        ]
        results = []
        while (token := lexer.next_token()).type != TokenType.EOF:
            results.append(token)

        assert results == expected
