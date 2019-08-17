#!/usr/bin/env python3

from pylang.lexer3.states import FileStart, Operators
from pylang.lexer3.token import TokenType


def test_call_returns_operators_state(context):
    s = FileStart(context(''))
    result = s()

    assert isinstance(result[0], Operators)


def test_call_returns_indent(context):
    s = FileStart(context(''))
    result = s()

    assert result[1].token_type == TokenType.Indent
