
from .lexer import TokenType, Token, Lexer


class MismatchException(Exception):
    pass


class Parser:
    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._lookahead_token: Token = Token(TokenType.EOF, '')
        self._consume()

    def _consume(self):
        self._lookahead_token = self._lexer.next_token()

    def _match(self, token_type: TokenType):
        if self._lookahead_token_type() != token_type:
            raise MismatchException(f'expected: {token_type} but {self._lookahead_token.type}')
        self._consume()

    def _lookahead_token_type(self) -> TokenType:
        return self._lookahead_token.type

    def _a_instruction(self):
        """
        a_instruction: '@' VAR | PREDEFINED | INT
        :return:
        """
        self._match(TokenType.AT)
        if self._lookahead_token_type() == TokenType.VAR:
            self._match(TokenType.VAR)
        elif self._lookahead_token_type() == TokenType.PREDEFINED:
            self._match(TokenType.PREDEFINED)
        else:
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
        if self._lookahead_token_type() == TokenType.REG_ONE:
            self._match(TokenType.REG_ONE)
        else:
            self._match(TokenType.REG_MULTI)

    def _comp(self):
        """
        comp: INT{0, 1}
              | '-' (INT{1} | REG_ONE)
        :return:
        """
        if self._is_zero_or_one_int_token():
            self._match(TokenType.INT)
        elif self._lookahead_token_type() == TokenType.MINUS:
            self._match(TokenType.MINUS)
            if self._is_one_int_token():
                self._match(TokenType.INT)
            else:
                self._match(TokenType.REG_ONE)
        else:
            raise MismatchException(f'comp parsing failed at {self._lookahead_token}')

    def _is_zero_or_one_int_token(self):
        return self._lookahead_token_type() == TokenType.INT and self._lookahead_token.text in {'0', '1'}

    def _is_one_int_token(self):
        return self._lookahead_token_type() == TokenType.INT and self._lookahead_token.text == '1'


