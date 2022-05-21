import pytest

from .lexer import Lexer
from .parser import Parser, MismatchException


class TestParser:
    @staticmethod
    def _a_instruction_success_test_cases() -> list[str]:
        return [
            '@i',  # VAR
            '@15',  # INT
            '@R15',  # PREDEFINED
        ]

    @staticmethod
    def _a_instruction_fail_test_cases() -> list[str]:
        return [
            '@JGT',
            '@'
        ]

    @staticmethod
    def _c_instruction_success_test_cases() -> list[str]:
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
    def _c_instruction_fail_test_cases() -> list[str]:
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

    @staticmethod
    def _l_instruction_success_test_cases() -> list[str]:
        return [
            # (VAR)
            '(i)',
            '(abc)',
            '(abc123)',
        ]

    @staticmethod
    def _l_instruction_fail_test_cases() -> list[str]:
        return [
            '(SCREEN)',
            '(123)',
        ]

    @staticmethod
    def _parse_success_test_cases() -> list[str]:
        return [
            '''
// Adds 1 + ... + 100
    @i
    M=1  // i=1
    @sum
    M=0  // sum=0
(LOOP)
    @i
    D=M  // D=i
    @100
    D=D-A  // D=i-100
    @END
    D;JGT  // if (i-100)>0 goto END
    @i
    D=M  // D=i
    @sum
    M=D+M  // sum=sum+1
    @i
    M=M+1 // i=i+1
    @LOOP
    0;JMP  // goto LOOP
(END)
    @END
    0;JMP
            '''
        ]

    @pytest.mark.parametrize('input_text', _a_instruction_success_test_cases())
    def test_a_instruction_success(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        parser._a_instruction()

    @pytest.mark.parametrize('input_text', _a_instruction_fail_test_cases())
    def test_a_instruction_fail(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        with pytest.raises(MismatchException):
            parser._a_instruction()

    @pytest.mark.parametrize('input_text', _c_instruction_success_test_cases())
    def test_c_instruction_success(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        parser._c_instruction()

    @pytest.mark.parametrize('input_text', _c_instruction_fail_test_cases())
    def test_c_instruction_fail(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        with pytest.raises(MismatchException):
            parser._c_instruction()

    @pytest.mark.parametrize('input_text', _l_instruction_success_test_cases())
    def test_l_instruction_success(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        parser._l_instruction()

    @pytest.mark.parametrize('input_text', _l_instruction_fail_test_cases())
    def test_l_instruction_fail(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        with pytest.raises(MismatchException):
            parser._l_instruction()

    @pytest.mark.parametrize('input_text', _parse_success_test_cases())
    def test_parse(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        parser.parse()
