from .lexer import TokenType, Token, ListLexer


class ListParserException(Exception):
    pass


class ListParser:
    def __init__(self, lexer: ListLexer, k: int):
        if k <= 1:
            raise ListParserException("k value should be larger than 1")
        self._lexer = lexer
        self._k = k
        self._lookahead_buffer = [Token(TokenType.EOF, '')] * self._k
        self._p = 0

        # fill lookahead buffer
        for i in range(k):
            self._consume()

    def parse(self):
        self._list()
        if self._lookahead_token(0).type != TokenType.EOF:
            raise ListParserException(f'expecting {TokenType.EOF}; found {self._lookahead_token(0).type}')

    def _list(self):
        self._match(TokenType.LBRACK)
        if self._lookahead_token(0).type != TokenType.RBRACK:
            self._elements()
        self._match(TokenType.RBRACK)

    def _elements(self):
        self._element()
        while self._lookahead_token(0).type == TokenType.COMMA:
            self._match(TokenType.COMMA)
            self._element()

    def _element(self):
        if self._lookahead_token(0).type == TokenType.VAR and self._lookahead_token(1).type == TokenType.EQUAL:
            # VAR=VAR case e.g. a=b
            self._match(TokenType.VAR)
            self._match(TokenType.EQUAL)
            self._match(TokenType.VAR)
        elif self._lookahead_token(0).type == TokenType.VAR:
            self._match(TokenType.VAR)
        else:
            self._list()

    def _match(self, token_type: TokenType):
        if self._lookahead_token(0).type == token_type:
            self._consume()
        else:
            raise ListParserException(f'expecting {token_type}; found {self._lookahead_token(0).type}')

    def _consume(self):
        self._lookahead_buffer[self._p] = self._lexer.next_token()
        self._p = (self._p + 1) % self._k

    def _lookahead_token(self, i: int) -> Token:
        return self._lookahead_buffer[(self._p + i) % self._k]
