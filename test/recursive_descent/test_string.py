#!/usr/bin/env python3

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser


def test_string(tokens_from_types):
    tokens = tokens_from_types(TokenType.String)
    p = Parser(lexer=tokens)
    result = p.string()

    assert result.value is tokens[0]
