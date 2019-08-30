#!/usr/bin/env python3

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser


def test_start(tokens_from_types, mocker):
    p = Parser(lexer=tokens_from_types(TokenType.Indent, TokenType.Dedent))
    block_spy = mocker.spy(p, 'block')
    result = p.start()

    assert result == []
    assert block_spy.assert_called
