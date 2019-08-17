#!/usr/bin/env python3

from pylang.lexer3.states import Start, Operators
from pylang.lexer3.token import TokenType


def test_call_to_file_start(context):
    s = Start(context=context(''))
    result = s()

    assert isinstance(result[0], Operators)
    assert result[1].token_type == TokenType.Indent
