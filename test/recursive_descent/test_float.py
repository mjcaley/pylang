#!/usr/bin/env python3

import pytest

from pylang.lexer.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.mark.parametrize('test_input,expected', [
    ['4.2', 4.2],
    ['42.42', 42.42]
])
def test_float(test_input, expected):
    l = Lexer.from_stream(test_input)
    next(l)
    p = Parser(lexer=l)

    result = p.float()

    assert pytest.approx(expected, result.value)


def test_float_exception():
    l = Lexer.from_stream('42')
    next(l)
    p = Parser(lexer=l)

    with pytest.raises(UnexpectedTokenError):
        p.float()
