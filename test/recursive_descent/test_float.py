#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedToken


@pytest.mark.parametrize('test_input,expected', [
    ['4.2', 4.2],
    ['.2', 0.2],
    ['42.42', 42.42]
])
def test_float(test_input, expected):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.float()

    assert pytest.approx(expected, result.value)


def test_float_exception():
    l = Lexer('42')
    l.emit()
    p = Parser(lexer=l)

    with pytest.raises(UnexpectedToken):
        p.float()
