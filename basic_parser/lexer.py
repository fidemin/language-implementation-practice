import re
from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    EOF = -1
    VAR = 1
    COMMA = 2
    LBRACK = 3
    RBRACK = 4
    EQUAL = 5


@dataclass
class Token:
    type: TokenType
    text: str


class ListLexerNextTokenException(Exception):
    pass


class ListLexer:
    EOF = -1

    def __init__(self, input_: str):
        self._input = input_
        self._current_char = None
        self._cursor = -1

    def next_token(self) -> Token:
        while self._current_char != self.EOF:
            if self._current_char is None:
                # for first next_token call
                self._consume()
            elif self._is_whitespace():
                self._whitespace()
            elif self._current_char == ',':
                self._consume()
                return Token(TokenType.COMMA, ',')
            elif self._current_char == '[':
                self._consume()
                return Token(TokenType.LBRACK, '[')
            elif self._current_char == ']':
                self._consume()
                return Token(TokenType.RBRACK, ']')
            elif self._current_char == '=':
                self._consume()
                return Token(TokenType.EQUAL, '=')
            elif self._is_letter():
                return self._var_token()
            else:
                raise ListLexerNextTokenException(f'invalid character: {self._current_char}')
        return Token(TokenType.EOF, '')

    def _consume(self):
        self._cursor += 1
        if self._cursor >= len(self._input):
            self._current_char = self.EOF
        else:
            self._current_char = self._input[self._cursor]

    def _is_letter(self) -> bool:
        # if current character is letter a-z, A-Z -> True
        return re.match(r'^[a-zA-Z]$', self._current_char) is not None

    def _is_whitespace(self) -> bool:
        # if current character is white space -> True
        return re.match(r'^\s$', self._current_char) is not None

    def _var_token(self) -> Token:
        variable_letters = []
        while self._is_letter():
            variable_letters.append(self._current_char)
            self._consume()
        return Token(TokenType.VAR, ''.join(variable_letters))

    def _whitespace(self):
        while self._is_whitespace():
            self._consume()
