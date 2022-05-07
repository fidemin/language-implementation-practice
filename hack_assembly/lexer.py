import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TokenType(Enum):
    # EOF
    EOF = -1

    # main
    AT = 1  # @ token
    INT = 2  # integer
    VAR = 3  # variable
    REG_ONE = 4  # one register
    REG_MULTI = 5  # multiple registers
    JUMP = 6  # jump symbol
    PREDEFINED = 7  # predefined symbol

    # operators
    EQUAL = 20
    MINUS = 21
    PLUS = 22
    NOT = 23
    AND = 24
    OR = 25

    # others
    SEMICOLON = 30
    LPAREN = 31
    RPAREN = 32
    NEWLINE = 33


@dataclass
class Token:
    type: TokenType
    text: str


class LexerNextTokenException(Exception):
    pass


class Lexer:
    EOF = ''

    def __init__(self, input_text: str):
        self._input_text = input_text
        self._current_char = None
        self._p = -1
        self._consume()

        # if newline exists in front, igonre it
        if self._whitespace():
            self._whitespace()

    def next_token(self) -> Token:
        while self._current_char != self.EOF:
            if self._current_char == '@':
                self._consume()
                return Token(TokenType.AT, '@')
            elif self._current_char == '=':
                self._consume()
                return Token(TokenType.EQUAL, '=')
            elif self._current_char == '-':
                self._consume()
                return Token(TokenType.MINUS, '-')
            elif self._current_char == '+':
                self._consume()
                return Token(TokenType.PLUS, '+')
            elif self._current_char == '!':
                self._consume()
                return Token(TokenType.NOT, '!')
            elif self._current_char == '&':
                self._consume()
                return Token(TokenType.AND, '&')
            elif self._current_char == '|':
                self._consume()
                return Token(TokenType.OR, '|')
            elif self._current_char == ';':
                self._consume()
                return Token(TokenType.SEMICOLON, ';')
            elif self._current_char == '(':
                self._consume()
                return Token(TokenType.LPAREN, '(')
            elif self._current_char == ')':
                self._consume()
                return Token(TokenType.RPAREN, ')')
            elif self._current_char == '/':
                self._comment()
            elif self._is_whitespace():
                if (token := self._whitespace()) is not None:
                    return token
            elif self._is_int():
                return self._int_token()
            elif self._is_letter():
                return self._letters_token()
            else:
                raise LexerNextTokenException(f'invalid character at {self._p}: {self._current_char}')
        return Token(TokenType.EOF, '')

    def _consume(self):
        self._p += 1

        if self._p >= len(self._input_text):
            self._current_char = self.EOF
            return

        self._current_char = self._input_text[self._p]

    def _is_whitespace(self) -> bool:
        return re.match(r'^\s$', self._current_char) is not None

    def _is_newline(self) -> bool:
        return re.match(r'^[\r\n]$', self._current_char) is not None

    def _whitespace(self) -> Optional[Token]:
        has_newline = False
        while self._is_whitespace():
            if self._is_newline():
                has_newline = True
            self._consume()

        if has_newline:
            return Token(TokenType.NEWLINE, '')

        return None

    def _comment(self):
        for _ in range(2):
            if self._current_char != '/':
                raise LexerNextTokenException(f'expected / but {self._current_char}')
            self._consume()

        while self._current_char != self.EOF:
            # returning newline token after comment is redundant
            # pass newline token if exists
            if self._is_newline():
                self._whitespace()
                return
            self._consume()

    def _is_int(self) -> bool:
        # if current char is integer -> True
        return re.match(r'^\d$', self._current_char) is not None

    def _int_token(self):
        chars = []
        while self._is_int():
            chars.append(self._current_char)
            self._consume()

            # letter is not proper character for integer token
            if self._is_letter():
                raise LexerNextTokenException(f'{self._current_char} char is not proper for integer')
        return Token(TokenType.INT, ''.join(chars))

    def _is_letter(self) -> bool:
        return re.match(r'^[a-zA-Z]$', self._current_char) is not None

    def _is_banned_trailing_char(self) -> bool:
        return re.match(r'^[@/]$', self._current_char) is not None

    def _letters_token(self):
        # first character should be letter
        chars = [self._current_char]
        self._consume()

        while self._is_letter() or self._is_int():
            chars.append(self._current_char)
            self._consume()

            if self._is_banned_trailing_char():
                raise LexerNextTokenException(f'{self._current_char} is not proper for letters token')

        var_text = ''.join(chars)

        if var_text in ['M', 'D', 'A']:
            return Token(TokenType.REG_ONE, var_text)
        elif var_text in ['MD', 'AM', 'AD', 'AMD']:
            return Token(TokenType.REG_MULTI, var_text)
        elif var_text in ['JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']:
            return Token(TokenType.JUMP, var_text)
        elif (var_text in ['SP', 'LCL', 'ARG', 'THIS', 'THAT', 'SCREEN', 'KBD'] or
                re.match(r'^R([01][0-5]|\d)$', var_text) is not None):
            return Token(TokenType.PREDEFINED, var_text)
        return Token(TokenType.VAR, ''.join(chars))
