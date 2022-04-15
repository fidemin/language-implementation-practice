import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TokenType(Enum):
    VAR = 2
    COMMA = 3
    LBRACK = 4
    RBRACK = 5


@dataclass
class Token:
    token_type: TokenType
    text: str


class ListLexerNextTokenException(Exception):
    pass


class ListLexer:
    EOF = -1

    def __init__(self, input_: str):
        self._input = input_
        self._current = None
        self._cursor = -1

    def next_token(self) -> Optional[Token]:
        while self._current != self.EOF:
            if self._current is None:
                # first next_token
                self._consume()
            elif self._current in [' ']:
                # white space
                # TODO: deal with all whitespace case
                self._consume()
            elif self._current == ',':
                self._consume()
                return Token(TokenType.COMMA, ',')
            elif self._current == '[':
                self._consume()
                return Token(TokenType.LBRACK, '[')
            elif self._current == ']':
                self._consume()
                return Token(TokenType.RBRACK, ']')
            elif self._is_letter():
                return self._var_token()
            else:
                raise ListLexerNextTokenException(f'invalid character: {self._current}')
        return None

    def _consume(self):
        self._cursor += 1
        if self._cursor >= len(self._input):
            self._current = self.EOF
        else:
            self._current = self._input[self._cursor]

    def _is_letter(self) -> bool:
        # only alphabet is acceptable
        return re.match('^[a-zA-Z]$', self._current) is not None

    def _var_token(self) -> Token:
        variable_letters = []
        while self._is_letter():
            variable_letters.append(self._current)
            self._consume()
        return Token(TokenType.VAR, ''.join(variable_letters))
