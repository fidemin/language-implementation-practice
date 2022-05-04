from dataclasses import dataclass
import re
from enum import Enum


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
            elif self._is_whitespace():
                self._whitespace()
            elif self._is_newline():
                return self._newline_token()
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
        if self._current_char == self.EOF:
            return False

        return re.match(r'^[^\S\r\n]$', self._current_char) is not None

    def _whitespace(self):
        while self._is_whitespace():
            self._consume()

    def _is_newline(self) -> bool:
        if self._current_char == self.EOF:
            return False

        return re.match(r'^[\r\n]$', self._current_char) is not None

    def _newline_token(self) -> Token:
        while self._is_newline():
            self._consume()

        return Token(TokenType.NEWLINE, '')

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

    def _letters_token(self):
        # first character should be letter
        chars = [self._current_char]
        self._consume()

        while self._is_letter() or self._is_int():
            chars.append(self._current_char)
            self._consume()

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
