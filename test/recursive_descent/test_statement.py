#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedToken
from pylang.parse_tree import BinaryExpression, Float, Integer


@pytest.mark.parametrize('test_input,expected', [
    ['4.2+42\n', BinaryExpression],
    ['4.2\r', Float],
    ['42\r\n', Integer]
])
def test_statement(test_input, expected):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.statement()

    assert isinstance(result, expected)


def test_statement_without_newline():
    l = Lexer('42')
    l.emit()
    p = Parser(l)

    with pytest.raises(UnexpectedToken):
        p.statement()
