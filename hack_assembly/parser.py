
from .lexer import TokenType, Token, Lexer
from typing import Optional


class MismatchException(Exception):
    pass


class Parser:
    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._lookahead_token: Optional[Token] = None
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

    def _c_instruction(self):
        """
        c_instruction: dest '=' comp
        :return:
        """
        self._dest()
        self._match(TokenType.EQUAL)
        self._comp()

    def _dest(self):
        """
        dest: REG_ONE | REG_MULTI
        :return:
        """
        if self._lookahead_token == TokenType.REG_ONE:
            self._match(TokenType.REG_ONE)
        elif self._lookahead_token == TokenType.REG_MULTI:
            self._match(TokenType.REG_MULTI)

    def _comp(self):
        """
        comp: INT

        where INT in {0, 1}
        :return:
        """
        if self._is_zero_or_one_int_token():
            self._match(TokenType.INT)

    def _is_zero_or_one_int_token(self):
        return self._lookahead_token.type == TokenType.INT and self._lookahead_token.text in {'0', '1'}

    def _match(self, token_type: TokenType):
        if self._lookahead_token.type != token_type:
            raise MismatchException(f'expected: {token_type} but {self._lookahead_token.type}')
        self._consume()
