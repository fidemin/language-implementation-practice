from dataclasses import dataclass
import re
from enum import Enum


class TokenType(Enum):
    EOF = -1
    AT = 1  # @ token
    INT = 2  # integer
    VAR = 3  # variable
    REG1 = 4  # one register
    REG2 = 5  # two registers

    EQUAL = 5
    MINUS = 6
    PLUS = 7

@dataclass
class Token:
    type: TokenType
    text: str


class LexerNextTokenException(Exception):
    pass


class Lexer:
    EOF = -1

    def __init__(self, input_text: str):
        self._input_text = input_text
        self._current_char = None
        self._p = -1
        self._consume()

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
            elif self._is_whitespace():
                self._whitespace()
            elif self._is_int():
                return self._int_token()
            elif self._is_letter():
                return self._var_token()
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
        if self._current_char == self.EOF:
            return False

        return re.match(r'^\s$', self._current_char) is not None

    def _whitespace(self):
        while self._is_whitespace():
            self._consume()

    def _is_int(self) -> bool:
        if self._current_char == self.EOF:
            return False

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
        if self._current_char == self.EOF:
            return False

        return re.match(r'^[a-zA-Z]$', self._current_char) is not None

    def _var_token(self):
        # first character should be letter
        chars = [self._current_char]
        self._consume()

        while self._is_letter() or self._is_int():
            chars.append(self._current_char)
            self._consume()

        var_text = ''.join(chars)

        if var_text in ['M', 'D', 'A']:
            return Token(TokenType.REG1, var_text)
        elif var_text in ['MD', 'AM', 'AD', 'AMD']:
            return Token(TokenType.REG2, var_text)

        return Token(TokenType.VAR, ''.join(chars))
