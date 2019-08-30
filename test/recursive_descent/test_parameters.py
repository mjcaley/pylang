#!/usr/bin/env python3

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser, UnexpectedTokenError


def test_one_parameter(tokens_from_types):
    tokens = tokens_from_types(TokenType.Identifier)
    p = Parser(lexer=tokens)
    result = p.parameters()

    assert len(result) == 1
    assert result[0].value is tokens[0]


def test_multiple_parameter(tokens_from_types):
    tokens = tokens_from_types(
        TokenType.Identifier,
        TokenType.Comma,
        TokenType.Identifier,
        TokenType.Comma,
        TokenType.Identifier
    )
    p = Parser(lexer=tokens)
    result = p.parameters()

    assert len(result) == 3
    assert result[0].value is tokens[0]
    assert result[1].value is tokens[2]
    assert result[2].value is tokens[4]
