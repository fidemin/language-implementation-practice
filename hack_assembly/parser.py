
from .lexer import TokenType, Token, Lexer


class MismatchException(Exception):
    pass


class Parser:
    """
    TODO:
      - 'M=A D' fail case -> deal with multiline
      - if symbol for l instruction is defined twice, where to deal with it
    """
    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._buffer_size = 2
        self._p = 0
        self._lookahead_buffer = [Token(TokenType.EOF, '')] * self._buffer_size

        for _ in range(self._buffer_size):
            self._consume()

    def _consume(self):
        self._lookahead_buffer[self._p] = self._lexer.next_token()
        self._p = (self._p + 1) % self._buffer_size

    def _match(self, token_type: TokenType):
        if self._lookahead_token_type(0) != token_type:
            raise MismatchException(f'expected: {token_type} but {self._lookahead_token(0).type}')
        self._consume()

    def _lookahead_token(self, i: int) -> Token:
        return self._lookahead_buffer[(self._p + i) % 2]

    def _lookahead_token_type(self, i: int) -> TokenType:
        return self._lookahead_token(i).type

    def _a_instruction(self):
        """
        a_instruction: '@' VAR | PREDEFINED | INT
        :return:
        """
        self._match(TokenType.AT)
        if self._lookahead_token_type(0) == TokenType.VAR:
            self._match(TokenType.VAR)
        elif self._lookahead_token_type(0) == TokenType.PREDEFINED:
            self._match(TokenType.PREDEFINED)
        else:
            self._match(TokenType.INT)

    def _c_instruction(self):
        """
        c_instruction: dest '=' comp
                     | comp ';' jump
        :return:
        """
        if self._lookahead_token_type(1) == TokenType.EQUAL:
            self._dest()
            self._match(TokenType.EQUAL)
            self._comp()
        else:
            self._comp()
            self._match(TokenType.SEMICOLON)
            self._jump()

    def _l_instruction(self):
        """
        l_instruction: '(' VAR ')'

        :return:
        """

        self._match(TokenType.LPAREN)
        self._match(TokenType.VAR)
        self._match(TokenType.RPAREN)

    def _dest(self):
        """
        dest: REG_ONE | REG_MULTI
        :return:
        """
        if self._lookahead_token_type(0) == TokenType.REG_ONE:
            self._match(TokenType.REG_ONE)
        else:
            self._match(TokenType.REG_MULTI)

    def _comp(self):
        """
        comp: INT{0, 1}
              | '-' (INT{1} | REG_ONE)
              | REG_ONE
              | REG_ONE '+' (REG_ONE | INT{1})
              | REG_ONE '-' (REG_ONE | INT{1})
              | REG_ONE '&' REG_ONE
              | REG_ONE '|' REG_ONE
        :return:
        """
        if self._is_zero_or_one_int_token():
            self._match(TokenType.INT)
        elif self._lookahead_token_type(0) == TokenType.MINUS:
            self._match(TokenType.MINUS)
            if self._is_one_int_token():
                self._match(TokenType.INT)
            else:
                self._match(TokenType.REG_ONE)
        elif self._lookahead_token_type(0) == TokenType.NOT:
            self._match(TokenType.NOT)
            self._match(TokenType.REG_ONE)
        elif self._lookahead_token_type(0) == TokenType.REG_ONE:
            self._match(TokenType.REG_ONE)
            if self._lookahead_token_type(0) == TokenType.PLUS:
                self._match(TokenType.PLUS)
                if self._is_one_int_token():
                    self._match(TokenType.INT)
                else:
                    self._match(TokenType.REG_ONE)
            elif self._lookahead_token_type(0) == TokenType.MINUS:
                self._match(TokenType.MINUS)
                if self._is_one_int_token():
                    self._match(TokenType.INT)
                else:
                    self._match(TokenType.REG_ONE)
            elif self._lookahead_token_type(0) == TokenType.AND:
                self._match(TokenType.AND)
                self._match(TokenType.REG_ONE)
            elif self._lookahead_token_type(0) == TokenType.OR:
                self._match(TokenType.OR)
                self._match(TokenType.REG_ONE)
        else:
            raise MismatchException(f'comp parsing failed at {self._lookahead_token}')

    def _jump(self):
        self._match(TokenType.JUMP)

    def _is_zero_or_one_int_token(self):
        return self._lookahead_token_type(0) == TokenType.INT and self._lookahead_token(0).text in {'0', '1'}

    def _is_one_int_token(self):
        return self._lookahead_token_type(0) == TokenType.INT and self._lookahead_token(0).text == '1'
