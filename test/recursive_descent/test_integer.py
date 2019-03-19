#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.mark.parametrize('test_input,expected', [
    ['4', 4],
    ['42', 42]
])
def test_integer(test_input, expected):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.integer()

    assert expected is result.value.value


def test_bool_exception():
    l = Lexer('a')
    l.emit()
    p = Parser(lexer=l)

    with pytest.raises(UnexpectedTokenError):
        p.integer()
