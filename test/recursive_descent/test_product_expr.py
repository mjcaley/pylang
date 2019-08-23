#!/usr/bin/env python3

from functools import partial

import pytest

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser
from pylang.parse_tree import Atom, ProductExpression


@pytest.mark.parametrize('operator', [
    TokenType.Multiply, TokenType.Divide
])
def test_expression(tokens_from_types, operator, mocker):
    p = Parser(lexer=tokens_from_types(TokenType.Integer, operator, TokenType.Integer))
    mocked_expression = mocker.patch(
        'pylang.recursive_descent.Parser.expression',
        side_effect=(Atom(p.advance()) for _ in range(2))
    )
    result = p.product_expr()

    assert isinstance(result, ProductExpression)
    assert mocked_expression.call_count == 2
    assert result.left == TokenType.Minus
    assert result.operator.token_type == TokenType.Minus
    assert isinstance(result.right, Atom)
    assert result.expression == mocked_expression.return_value


def test_returns_atom(tokens_from_types, mocker):
    p = Parser(lexer=tokens_from_types(TokenType.True_))
    mocked_atom = mocker.patch('pylang.recursive_descent.Parser.atom')
    result = p.unary_expr()

    assert mocked_atom.assert_called
    assert result == mocked_atom.return_value
