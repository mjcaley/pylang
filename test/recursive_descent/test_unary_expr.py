#!/usr/bin/env python3

import pytest

from pylang.lexer.lexer import Lexer
from pylang.recursive_descent import Parser
from pylang.parse_tree import Integer, UnaryExpression


@pytest.mark.parametrize('test_input,expected', [
    ['-42', UnaryExpression],
    ['42', Integer]
])
def test_identifier(test_input, expected):
    l = Lexer.from_stream(test_input)
    next(l)
    p = Parser(lexer=l)

    result = p.unary_expr()

    assert isinstance(result, expected)
