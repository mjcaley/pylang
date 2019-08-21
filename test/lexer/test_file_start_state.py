#!/usr/bin/env python3

from pylang.lexer.states import FileStart
from pylang.lexer.token import TokenType


def test_call_returns_indent_state(context, mocker):
    s = FileStart(context(''))
    mocked_indent = mocker.patch('pylang.lexer.states.Indent')
    instance = mocked_indent()
    mocker.spy(s.context, 'advance')
    mocker.spy(s.context, 'push_indent')
    result = s()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Indent
    assert s.context.advance.call_count == 2
    s.context.push_indent.assert_called_once_with(0)
