#!/usr/bin/env python3

import pytest

from pylang.lexer.lexer import Lexer
from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.mark.parametrize('test_input,expected', [
    ['true', TokenType.True_],
    ['false', TokenType.False_]
])
def test_bool(test_input, expected):
    l = Lexer.from_stream(test_input)
    next(l)
    p = Parser(lexer=l)

    result = p.bool()

    assert expected is result.value.token_type


def test_bool_exception():
    l = Lexer.from_stream('42')
    next(l)
    p = Parser(lexer=l)

    with pytest.raises(UnexpectedTokenError):
        p.bool()
