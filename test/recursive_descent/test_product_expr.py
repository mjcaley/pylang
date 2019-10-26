#!/usr/bin/env python3

import pytest

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser
from pylang.parse_tree import ProductExpression


@pytest.mark.parametrize('operator', [
    TokenType.Multiply, TokenType.Divide, TokenType.Modulo
])
def test_expression(tokens_from_types, operator, mocker):
    tokens = tokens_from_types(TokenType.Integer, operator, TokenType.Integer)
    p = Parser(lexer=tokens)
    expression_spy = mocker.spy(p, 'expression')
    unary_expr_spy = mocker.spy(p, 'unary_expr')
    result = p.product_expr()

    assert isinstance(result, ProductExpression)
    assert result.left.value is tokens[0]
    assert result.operator is tokens[1]
    assert result.right.value is tokens[2]
    assert expression_spy.called
    assert unary_expr_spy.called


def test_returns_atom(tokens_from_types, mocker):
    tokens = tokens_from_types(TokenType.True_)
    p = Parser(lexer=tokens)
    atom_spy = mocker.spy(p, 'atom')
    result = p.unary_expr()

    assert atom_spy.called
    assert result.value is tokens[0]
