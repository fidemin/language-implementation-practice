from lexer import TokenType, ListLexer


class ListParserException(Exception):
    pass


class ListParser:
    def __init__(self, lexer: ListLexer):
        self._lexer = lexer
        self._lookahead = self._lexer.next_token()

    def parse(self):
        self._list()
        if self._lookahead.type != TokenType.EOF:
            raise ListParserException(f'expecting {TokenType.EOF}; found {self._lookahead.type}')

    def _list(self):
        self._match(TokenType.LBRACK)
        if self._lookahead.type != TokenType.RBRACK:
            self._elements()
        self._match(TokenType.RBRACK)

    def _elements(self):
        self._match(TokenType.VAR)
        while self._lookahead.type == TokenType.COMMA:
            self._match(TokenType.COMMA)
            self._match(TokenType.VAR)

    def _element(self):
        self._match(TokenType.VAR)

    def _match(self, token_type: TokenType):
        if self._lookahead.type == token_type:
            self._consume()
        else:
            raise ListParserException(f'expecting {token_type}; found {self._lookahead.type}')

    def _consume(self):
        self._lookahead = self._lexer.next_token()
