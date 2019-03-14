#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser
from pylang.parse_tree import Integer, AssignmentExpression


@pytest.mark.parametrize('test_input,expected', [
    ['id=42', AssignmentExpression],
    ['42', Integer]
])
def test_product_expr(test_input, expected):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.assignment_expr()

    assert isinstance(result, expected)