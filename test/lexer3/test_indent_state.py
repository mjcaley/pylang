#!/usr/bin/env python3

from pylang.lexer3.states import Indent, Operators
from pylang.lexer3.token import TokenType


def test_transition_when_not_at_beginning(context_at_position):
    i = Indent(context_at_position('+++', 3))
    i.context.push_indent(0)
    result = i()

    assert isinstance(result[0], Operators)


def test_transition_on_non_whitespace(context_at_current):
    i = Indent(context_at_current('+'))
    i.context.push_indent(0)
    result = i()

    assert isinstance(result[0], Operators)


def test_skip_empty_line(context_at_current):
    i = Indent(context_at_current('    \n+'))
    i.context.push_indent(0)
    result = i()

    assert isinstance(result[0], Operators)


def test_indent(context_at_position, mocker):
    i = Indent(context_at_position('\n    +', 3))
    i.context.push_indent(0)
    mocker.spy(i.context, 'push_indent')
    result = i()

    assert isinstance(result[0], Operators)
    assert result[1].token_type == TokenType.Indent
    assert result[1].position.index == 1
    assert result[1].position.line == 2
    assert result[1].position.column == 1
    assert i.context.push_indent.called


def test_same_indent(context_at_position, mocker):
    i = Indent(context_at_position('\n    +', 3))
    i.context.push_indent(0)
    i.context.push_indent(4)
    mocker.spy(i.context, 'push_indent')
    result = i()

    assert isinstance(result[0], Operators)


def test_dedent(context_at_position, mocker):
    i = Indent(context_at_position('\n    +', 3))
    i.context.push_indent(0)
    i.context.push_indent(8)
    mocker.spy(i.context, 'pop_indent')
    result = i()

    assert isinstance(result[0], Indent)
    assert result[1].token_type == TokenType.Dedent
    assert result[1].position.index == 1
    assert result[1].position.line == 2
    assert result[1].position.column == 1
    assert i.context.pop_indent.called


def test_multiple_dedents(context_at_position, mocker):
    i = Indent(context_at_position('\n+', 3))
    i.context.push_indent(0)
    i.context.push_indent(4)
    i.context.push_indent(8)
    i.context.push_indent(16)
    mocker.spy(i.context, 'pop_indent')
    result1 = i()
    result2 = i()
    result3 = i()
    result4 = i()

    assert isinstance(result1[0], Indent)
    assert result1[1].token_type == TokenType.Dedent

    assert isinstance(result2[0], Indent)
    assert result2[1].token_type == TokenType.Dedent

    assert isinstance(result3[0], Indent)
    assert result3[1].token_type == TokenType.Dedent

    assert i.context.pop_indent.call_count == 3

    assert isinstance(result4[0], Operators)
    assert result4[1].token_type != TokenType.Dedent
