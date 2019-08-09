#!/usr/bin/env python3

from pylang.lexer3 import TokenType


def test_emit_integer_token(lexer):
    l = lexer('number', '123', 2)
    result = next(l)

    assert result.token_type == TokenType.Digits
