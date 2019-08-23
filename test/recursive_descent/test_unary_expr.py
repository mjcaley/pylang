#!/usr/bin/env python3


from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser
from pylang.parse_tree import UnaryExpression


def test_negative_expression(tokens_from_types, mocker):
    p = Parser(lexer=tokens_from_types(TokenType.Minus, TokenType.True_))
    mocked_expression = mocker.patch('pylang.recursive_descent.Parser.expression')
    result = p.unary_expr()

    assert isinstance(result, UnaryExpression)
    assert mocked_expression.assert_called
    assert result.operator.token_type == TokenType.Minus
    assert result.expression == mocked_expression.return_value


def test_returns_atom(tokens_from_types, mocker):
    p = Parser(lexer=tokens_from_types(TokenType.True_))
    mocked_atom = mocker.patch('pylang.recursive_descent.Parser.atom')
    result = p.unary_expr()

    assert mocked_atom.assert_called
    assert result == mocked_atom.return_value
