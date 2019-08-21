#!/usr/bin/env python3

import pytest

from pylang.lexer.lexer import Lexer
from pylang.recursive_descent import Parser
from pylang.parse_tree import Integer, ProductExpression


@pytest.mark.parametrize('test_input,expected', [
    ['42*42', ProductExpression],
    ['42/42', ProductExpression],
    ['42', Integer]
])
def test_product_expr(test_input, expected):
    l = Lexer.from_stream(test_input)
    next(l)
    p = Parser(lexer=l)

    result = p.product_expr()

    assert isinstance(result, expected)
