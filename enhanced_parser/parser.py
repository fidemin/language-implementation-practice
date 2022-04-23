from core.lexer import TokenType, Token, ListLexer

from collections import defaultdict


class ParserException(Exception):
    pass


class MisMatchException(ParserException):
    pass


class SpeculationException(ParserException):
    pass


def save_and_restore_p(method):
    def inner(self, *args, **kwargs):
        self._save_p()
        returned = method(self, *args, **kwargs)
        self._restore_p()
        return returned
    return inner


class Parser:
    def __init__(self, lexer: ListLexer):
        self._lexer = lexer
        self._lookahead_buffer = []

        self._lock_buffer_reset = False
        self._retrieved_buffer_size = 0

        self._p = -1
        self._saved_p = -1

        # caches for already parsed rule
        self._parsed_caches = defaultdict(dict)

        self._consume()

    def parse(self):
        self._stat()
        self._match(TokenType.EOF)

    def _stat(self):
        """
        stat: list EOF | assign EOF;
        :return:
        """
        if self._speculate_list():
            self._list()
            self._match(TokenType.EOF)
        elif self._speculate_assign():
            self._assign()
            self._match(TokenType.EOF)
        else:
            raise SpeculationException(f'expecting stat but found {self._lookahead_token(0)}')

    @save_and_restore_p
    def _speculate_list(self) -> bool:
        success = True
        try:
            self._list()
            self._match(TokenType.EOF)
        except MisMatchException:
            success = False
        return success

    @save_and_restore_p
    def _speculate_assign(self) -> bool:
        success = True
        try:
            self._assign()
            self._match(TokenType.EOF)
        except MisMatchException:
            success = False
        return success

    def _save_p(self):
        self._lock_buffer_reset = True
        self._saved_p = self._p

    def _restore_p(self):
        self._p = self._saved_p
        self._saved_p = -1
        self._lock_buffer_reset = False

    def _assign(self):
        """
        assign: List '=' List;
        :return:
        """
        self._list()
        self._match(TokenType.EQUAL)
        self._list()

    def _list(self):
        """
        list: '[' elements ']'
        :return:
        """
        cache_key = '_list'

        start_accumulative_p = self._accumulative_p()
        if (start_end_p_tuple := self._parsed_caches[cache_key].get(start_accumulative_p)) is not None:
            self._p = start_end_p_tuple[1]
            return

        start_p = self._p
        self._match(TokenType.LBRACK)
        if self._lookahead_token(0).type != TokenType.RBRACK:
            self._elements()
        self._match(TokenType.RBRACK)
        end_p = self._p

        self._parsed_caches[cache_key][start_accumulative_p] = (start_p, end_p)

    def _elements(self):
        """
        elements: element (',' element)*
        :return:
        """
        self._element()
        while self._lookahead_token(0).type == TokenType.COMMA:
            self._match(TokenType.COMMA)
            self._element()

    def _element(self):
        """
        element: VAR '=' VAR | VAR | list
        :return:
        """
        if self._lookahead_token(0).type == TokenType.VAR and self._lookahead_token(1).type == TokenType.EQUAL:
            # VAR=VAR case e.g. a=b
            self._match(TokenType.VAR)
            self._match(TokenType.EQUAL)
            self._match(TokenType.VAR)
        elif self._lookahead_token(0).type == TokenType.VAR:
            self._match(TokenType.VAR)
        else:
            self._list()

    def _match(self, token_type: TokenType):
        if self._lookahead_token(0).type == token_type:
            self._consume()
        else:
            raise MisMatchException(f'expecting {token_type}; found {self._lookahead_token(0).type}')

    def _lookahead_token(self, i: int) -> Token:
        self._sync(i+1)
        return self._lookahead_buffer[self._p+i]

    def _consume(self):
        self._p += 1
        if self._p == len(self._lookahead_buffer) and not self._lock_buffer_reset:
            self._reset_buffer()
            self._remove_old_caches()
        self._sync(1)

    def _reset_buffer(self):
        self._retrieved_buffer_size += self._retrieved_buffer_size + len(self._lookahead_buffer)
        self._p = 0
        self._lookahead_buffer = []

    def _remove_old_caches(self):
        for cache_method_key in self._parsed_caches.keys():
            cache_for_method = self._parsed_caches[cache_method_key]
            delete_keys = []
            for cached_acc_p in cache_for_method.keys():
                if cached_acc_p < self._retrieved_buffer_size:
                    delete_keys.append(cached_acc_p)
            for key in delete_keys:
                cache_for_method.pop(key)

    def _accumulative_p(self):
        return self._retrieved_buffer_size + self._p

    def _sync(self, i: int):
        if self._p + i - 1 > len(self._lookahead_buffer) - 1:
            n = (self._p + i - 1) - (len(self._lookahead_buffer) - 1)
            self._fill(n)

    def _fill(self, n: int):
        for _ in range(n):
            self._lookahead_buffer.append(self._lexer.next_token())
