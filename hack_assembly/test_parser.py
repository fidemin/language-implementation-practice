import pytest

from .lexer import Lexer
from .parser import Parser, MismatchException


class TestParser:
    @staticmethod
    def _parser_a_instruction_success_test_cases() -> list[str]:
        return [
            '@i',  # VAR
            '@15',  # INT
            '@R15',  # PREDEFINED
        ]

    @staticmethod
    def _parser_a_instruction_fail_test_cases() -> list[str]:
        return [
            '@JGT',
            '@'
        ]

    @staticmethod
    def _parser_c_instruction_success_test_cases() -> list[str]:
        return [
            # dest=comp
            'M=0',
            'M=1',
            'MD=1',
            'MD=-1',
            'MD=!M',
            'M=!A',
            'M=D',
            'M=A+D',
            'M=D+1',
            'M=A-D',
            'M=D-1',
            'M=A&D',
            'M=D|A',

            # comp;jump
            '0;JMP',
            'D;JGT',
            'D&A;JGT',
        ]

    @staticmethod
    def _parser_c_instruction_fail_test_cases() -> list[str]:
        return [
            # dest=comp fail cases
            'M=-0',
            'MD=2',
            'MD=i',
            'MD=-2',
            'MD=AMD',
            'MD=!1',
            'M=D+0',
            'M=D-0',
            'M=A&0',
            'M=D|1',
            'M=JMP'

            # comp;jump fail cases
            'AMD;JMP',
        ]

    @pytest.mark.parametrize('input_text', _parser_a_instruction_success_test_cases())
    def test_parser_a_instruction_success(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        parser._a_instruction()

    @pytest.mark.parametrize('input_text', _parser_a_instruction_fail_test_cases())
    def test_parser_a_instruction_fail(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        with pytest.raises(MismatchException):
            parser._a_instruction()

    @pytest.mark.parametrize('input_text', _parser_c_instruction_success_test_cases())
    def test_parser_c_instruction_success(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        parser._c_instruction()

    @pytest.mark.parametrize('input_text', _parser_c_instruction_fail_test_cases())
    def test_parser_c_instruction_fail(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        with pytest.raises(MismatchException):
            parser._c_instruction()
