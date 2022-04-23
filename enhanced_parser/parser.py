from core.lexer import TokenType, Token, ListLexer


class ParserException(Exception):
    pass


class MatchFailException(ParserException):
    pass


class Parser:
    def __init__(self, lexer: ListLexer):
        self._lexer = lexer
        self._lookahead_buffer = []
        self._p = -1
        self._consume()

    def parse(self):
        self._list()
        self._match(TokenType.EOF)

    #def _stat(self):
    #    """
    #    stat: list EOF | assign EOF;
    #    :return:
    #    """
    #    if self._speculate_list():
    #        self._list()
    #        self._match(TokenType.EOF)
    #    elif self._speculate_assign():
    #        self._assign()
    #        self._match(TokenType.EOF)

    #def _speculate_list(self) -> bool:
    #    success = True
    #    self._mark()
    #    try:
    #        self._list()
    #        self._match(TokenType.EOF)
    #    except MatchFailException:
    #        success = False
    #    finally:
    #        self._release()
    #    return success

    #def _speculate_assign(self) -> bool:
    #    success = True
    #    self._mark()
    #    try:
    #        self._assign()
    #        self._match(TokenType.EOF)
    #    except MatchFailException:
    #        success = False
    #    finally:
    #        self._release()
    #    return success

    #def _assign(self):
    #    """
    #    assign: List '=' List;
    #    :return:
    #    """
    #    self._list()
    #    self._match(TokenType.EQUAL)
    #    self._list()

    def _list(self):
        """
        list: '[' elements ']'
        :return:
        """
        self._match(TokenType.LBRACK)
        if self._lookahead_token(0).type == TokenType.RBRACK:
            self._match(TokenType.RBRACK)
            return
        self._elements()
        self._match(TokenType.RBRACK)

    def _elements(self):
        """
        elements: element (',' element)*
        :return:
        """
        self._element()
        while self._lookahead_token(0).type == TokenType.COMMA:
            self._match(TokenType.COMMA)
            self._element()

    def _element(self):
        """
        element: VAR '=' VAR | VAR | list
        :return:
        """
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
            raise MatchFailException(f'expecting {token_type}; found {self._lookahead_token(0).type}')

    def _lookahead_token(self, i: int) -> Token:
        self._sync(i+1)
        return self._lookahead_buffer[self._p+i]

    def _consume(self):
        self._p += 1
        if self._p == len(self._lookahead_buffer) and not self._is_speculating():
            self._p = 0
            self._lookahead_buffer = []
        self._sync(1)
        print("\nLOOKAHEAD: ", self._lookahead_buffer)

    def _is_speculating(self):
        return False

    def _sync(self, i: int):
        if self._p + i - 1 > len(self._lookahead_buffer) - 1:
            n = (self._p + i - 1) - (len(self._lookahead_buffer) - 1)
            self._fill(n)

    def _fill(self, n: int):
        for _ in range(n):
            self._lookahead_buffer.append(self._lexer.next_token())
