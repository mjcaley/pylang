#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser
from pylang.parse_tree import Integer, SumExpression


@pytest.mark.parametrize('test_input,expected', [
    ['42+42', SumExpression],
    ['42-42', SumExpression],
    ['42', Integer]
])
def test_sum_expr(test_input, expected):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.sum_expr()

    assert isinstance(result, expected)
