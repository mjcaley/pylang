#!/usr/bin/env python3

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser


def test_block(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Indent, TokenType.True_, TokenType.Newline, TokenType.Dedent))
    result = p.block()

    assert isinstance(result, list)
