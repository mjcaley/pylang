#!/usr/bin/env python3

from pylang.lexer3.token import TokenType


def test_emit_integer_token(lexer):
    l = lexer('number', '42', 2)
    result = next(l)

    assert result.token_type == TokenType.Integer
    assert result.value == '42'


def test_emit_float_token(lexer):
    l = lexer('number', '4.2', 2)
    result = next(l)

    assert result.token_type == TokenType.Float
    assert result.value == '4.2'
