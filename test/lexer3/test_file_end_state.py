#!/usr/bin/env python3

from pylang.lexer3.states import FileEnd
from pylang.lexer3.token import TokenType


def test_call_returns_end_state(context, mocker):
    s = FileEnd(context(''))
    mocked_indent = mocker.patch('pylang.lexer3.states.End')
    instance = mocked_indent()
    s.context.push_indent(0)
    mocker.spy(s.context, 'pop_indent')
    result = s()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Dedent
    assert s.context.pop_indent.call_count == 1
