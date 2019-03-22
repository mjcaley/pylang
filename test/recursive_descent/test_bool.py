#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.mark.parametrize('test_input,expected', [
    ['true', True],
    ['false', False]
])
def test_bool(test_input, expected):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.bool()

    assert expected is result.value.value


def test_bool_exception():
    l = Lexer('42')
    l.emit()
    p = Parser(lexer=l)

    with pytest.raises(UnexpectedTokenError):
        p.bool()
