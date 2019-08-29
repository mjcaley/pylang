#!/usr/bin/env python3

import pytest

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.mark.parametrize('token', [
    TokenType.Integer,
    TokenType.Float,
    TokenType.Identifier,
    TokenType.True_,
    TokenType.False_
])
def test_atom_types(token, tokens_from_types):
    tokens = tokens_from_types(token)
    p = Parser(lexer=tokens)
    result = p.atom()

    assert result.value is tokens[0]


def test_expression(mocker, tokens_from_types):
    tokens = tokens_from_types(TokenType.LParen, TokenType.Identifier, TokenType.RParen)
    p = Parser(lexer=tokens)
    expression_spy = mocker.spy(p, 'expression')
    result = p.atom()

    assert result.value is tokens[1]
    assert expression_spy.assert_called


def test_expression_raises_on_open_bracket(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.LParen, TokenType.Identifier, TokenType.Indent))

    with pytest.raises(UnexpectedTokenError):
        p.atom()


def test_raises_on_unexpected_token(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Indent))

    with pytest.raises(UnexpectedTokenError):
        p.atom()
