#!/usr/bin/env python3

import pytest

from pylang.lexer.lexer import Lexer
from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.mark.parametrize('test_input', [
    '4', '42'
])
def test_integer(test_input):
    l = Lexer.from_stream(test_input)
    next(l)
    p = Parser(lexer=l)

    result = p.integer()

    assert result.value.token_type == TokenType.Integer
    assert test_input == result.value.value


def test_bool_exception():
    l = Lexer.from_stream('a')
    next(l)
    p = Parser(lexer=l)

    with pytest.raises(UnexpectedTokenError):
        p.integer()
