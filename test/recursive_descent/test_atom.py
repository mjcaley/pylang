#!/usr/bin/env python3

from functools import partial

import pytest

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser, UnexpectedTokenError
from pylang.parse_tree import Atom, Boolean, Float, Identifier, Integer


@pytest.mark.parametrize('token,parse_tree_cls', [
    [TokenType.Integer, Integer],
    [TokenType.Float, Float],
    [TokenType.Identifier, Identifier],
    [TokenType.True_, Boolean],
    [TokenType.False_, Boolean]
])
def test_atom_types(token, parse_tree_cls, tokens_from_types):
    p = Parser(lexer=tokens_from_types(token))
    result = p.atom()

    assert isinstance(result, parse_tree_cls)
    assert result.value.token_type == token


def test_expression(mocker, tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.LParen, TokenType.Identifier, TokenType.RParen))
    expression_return = mocker.stub()

    def side_effect():
        p.advance()
        return expression_return

    mocked_expression = mocker.patch(
        'pylang.recursive_descent.Parser.expression',
        side_effect=side_effect
    )
    result = p.atom()

    assert result == expression_return
    assert mocked_expression.call_count == 1


def test_expression_raises_on_open_bracket(mocker, tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.LParen, TokenType.Identifier, TokenType.Indent))

    def side_effect():
        p.advance()
        return mocker.stub()

    mocker.patch(
        'pylang.recursive_descent.Parser.expression',
        side_effect=side_effect
    )

    with pytest.raises(UnexpectedTokenError):
        p.atom()


def test_raises_on_unexpected_token(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Indent))

    with pytest.raises(UnexpectedTokenError):
        p.atom()
