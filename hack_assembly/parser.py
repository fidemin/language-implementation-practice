
from .lexer import TokenType, Lexer


class MismatchException(Exception):
    pass


class Parser:
    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._lookahead_token = None
        self._consume()

    def _consume(self):
        self._lookahead_token = self._lexer.next_token()

    def _a_instruction(self):
        """
        a_instruction: '@' VAR | PREDEFINED | INT
        :return:
        """
        self._match(TokenType.AT)
        if self._lookahead_token == TokenType.VAR:
            self._match(TokenType.VAR)
        elif self._lookahead_token == TokenType.PREDEFINED:
            self._match(TokenType.VAR)
        elif self._lookahead_token == TokenType.INT:
            self._match(TokenType.INT)

    def _match(self, token_type: TokenType):
        if self._lookahead_token.type != token_type:
            raise MismatchException(f'expected: {token_type} but {self._lookahead_token.type}')
        self._consume()
