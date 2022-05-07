
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
        self._match(TokenType.AT)
        self._match(TokenType.VAR)

    def _match(self, token_type: TokenType):
        if self._lookahead_token.type != token_type:
            raise MismatchException(f'expected: {token_type} but {self._lookahead_token.type}')
        self._consume()
