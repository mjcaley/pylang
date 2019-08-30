#!/usr/bin/env python3


from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser
from pylang.parse_tree import UnaryExpression


def test_negative_expression(tokens_from_types, mocker):
    tokens = tokens_from_types(TokenType.Minus, TokenType.True_)
    p = Parser(lexer=tokens)
    expression_spy = mocker.spy(p, 'expression')
    result = p.unary_expr()

    assert isinstance(result, UnaryExpression)
    assert result.operator is tokens[0]
    assert result.expression.value is tokens[1]
    assert expression_spy.called


def test_returns_atom(tokens_from_types, mocker):
    tokens = tokens_from_types(TokenType.True_)
    p = Parser(lexer=tokens)
    atom_spy = mocker.spy(p, 'atom')
    result = p.unary_expr()

    assert result.value is tokens[0]
    assert atom_spy.called
