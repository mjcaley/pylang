#!/usr/bin/env python3

from pylang.lexer3.states import Indent
from pylang.lexer3.token import TokenType


def test_transition_when_not_at_beginning(context_at_position, mocker):
    i = Indent(context_at_position('+++', 3))
    i.context.push_indent(0)
    mocked_operators = mocker.patch('pylang.lexer3.states.Operators')
    called_instance = mocked_operators()()
    result = i()

    assert result == called_instance


def test_transition_on_non_whitespace(context_at_current, mocker):
    i = Indent(context_at_current('+'))
    i.context.push_indent(0)
    mocked_operators = mocker.patch('pylang.lexer3.states.Operators')
    called_instance = mocked_operators()()
    result = i()

    assert result == called_instance


def test_skip_empty_line(context_at_current, mocker):
    i = Indent(context_at_current('    \n+'))
    i.context.push_indent(0)
    mocked_operators = mocker.patch('pylang.lexer3.states.Operators')
    called_instance = mocked_operators()()
    result = i()

    assert result == called_instance


def test_indent(context_at_position, mocker):
    i = Indent(context_at_position('\n    +', 3))
    i.context.push_indent(0)
    mocker.spy(i.context, 'push_indent')
    mocked_operators = mocker.patch('pylang.lexer3.states.Operators')
    instance = mocked_operators()
    result = i()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Indent


def test_same_indent(context_at_position, mocker):
    i = Indent(context_at_position('\n    +', 3))
    i.context.push_indent(0)
    i.context.push_indent(4)
    mocker.spy(i.context, 'push_indent')
    mocked_operators = mocker.patch('pylang.lexer3.states.Operators')
    called_instance = mocked_operators()()
    result = i()

    assert result == called_instance


def test_dedent(context_at_position, mocker):
    i = Indent(context_at_position('\n    +', 3))
    i.context.push_indent(0)
    i.context.push_indent(8)
    mocked_dedent = mocker.patch('pylang.lexer3.states.Dedent')
    called_instance = mocked_dedent()()
    result = i()

    assert result == called_instance


def test_eof_transitions_to_dedent(context_at_current, mocker):
    i = Indent(context_at_current(''))
    i.context.push_indent(0)
    mocked_dedent = mocker.patch('pylang.lexer3.states.Dedent')
    called_instance = mocked_dedent()()
    result = i()

    assert result == called_instance


def test_eof_with_whitespace_transitions_to_dedent(context_at_current, mocker):
    i = Indent(context_at_current('    '))
    i.context.push_indent(0)
    mocked_dedent = mocker.patch('pylang.lexer3.states.Dedent')
    called_instance = mocked_dedent()()
    result = i()

    assert result == called_instance
