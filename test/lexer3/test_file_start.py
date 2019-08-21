#!/usr/bin/env python3

from pylang.lexer3.states import FileStart
from pylang.lexer3.token import TokenType


def test_call_returns_indent_state(context, mocker):
    s = FileStart(context(''))
    mocked_indent = mocker.patch('pylang.lexer3.states.Indent')
    instance = mocked_indent()
    mocker.spy(s.context, 'advance')
    result = s()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Indent
    assert s.context.advance.call_count == 2
