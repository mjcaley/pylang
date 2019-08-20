#!/usr/bin/env python3

from pylang.lexer3.states import Dedent
from pylang.lexer3.token import TokenType


def test_call_transition_to_indent_when_done(mocker, context_at_current):
    d = Dedent(context_at_current('x'), target_indent=0)
    d.context.push_indent(0)
    mocked_indent = mocker.patch('pylang.lexer3.states.Indent')
    d()

    assert mocked_indent.called


def test_call_transition_to_file_end_when_eof(mocker, context_at_current):
    d = Dedent(context_at_current(''), target_indent=0)
    d.context.push_indent(0)
    mocked_fileend = mocker.patch('pylang.lexer3.states.FileEnd')
    d()

    assert mocked_fileend.called


def test_call_emits_dedent_token(mocker, context_at_current):
    d = Dedent(context_at_current(''), target_indent=0)
    d.context.push_indent(0)
    d.context.push_indent(4)
    mocker.spy(d.context, 'pop_indent')
    result = d()

    assert isinstance(result[0], Dedent)
    assert result[1].token_type == TokenType.Dedent
    assert d.context.pop_indent.called


def test_call_dumps_multiple_dedents(mocker, context_at_current):
    d = Dedent(context_at_current(''), target_indent=0)
    d.context.push_indent(0)
    d.context.push_indent(4)
    d.context.push_indent(8)
    d.context.push_indent(12)
    mocked_fileend = mocker.patch('pylang.lexer3.states.FileEnd')
    mocker.spy(d.context, 'pop_indent')
    result1 = d()
    result2 = d()
    result3 = d()
    d()

    assert isinstance(result1[0], Dedent)
    assert result1[1].token_type == TokenType.Dedent

    assert isinstance(result2[0], Dedent)
    assert result2[1].token_type == TokenType.Dedent

    assert isinstance(result3[0], Dedent)
    assert result3[1].token_type == TokenType.Dedent

    assert mocked_fileend.called
