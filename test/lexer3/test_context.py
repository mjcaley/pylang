#!/usr/bin/env python3

import pytest

from pylang.lexer3.exceptions import MismatchedBracketException,  MismatchedIndentException
from pylang.lexer3.context import Context
from pylang.lexer3.stream import Position, Stream


def test_init(mocker):
    c = Context(mocker.stub())

    assert 'c' in locals()


def test_push_indent(mocker):
    c = Context(mocker.stub())
    c.push_indent(length=0)

    assert True


def test_push_indent_mismatch(mocker):
    c = Context(mocker.stub())
    c.push_indent(length=0)

    with pytest.raises(MismatchedIndentException):
        c.push_indent(length=-1)


def test_pop_indent_one_level(mocker):
    c = Context(mocker.stub())
    c.push_indent(length=0)
    result = c.pop_indent(until=0)

    assert result == []


def test_pop_indent_multiple_levels(mocker):
    c = Context(mocker.stub())
    c.push_indent(length=0)
    c.push_indent(length=4)
    c.push_indent(length=8)
    result = c.pop_indent(until=0)

    assert result == [8, 4]


def test_pop_indent_mismatched(mocker):
    c = Context(mocker.stub())
    c.push_indent(length=0)

    with pytest.raises(MismatchedIndentException):
        c.pop_indent(until=-1)


def test_pop_indent_empty(mocker):
    c = Context(mocker.stub())

    with pytest.raises(MismatchedIndentException):
        c.pop_indent(until=0)


def test_push_bracket(mocker):
    c = Context(mocker.stub())
    c.push_bracket('(')

    assert True


def test_pop_bracket_matching(mocker):
    c = Context(mocker.stub())
    c.push_bracket(bracket='(')
    result = c.pop_bracket(expected='(')

    assert result == '('


def test_pop_bracket_mismatch(mocker):
    c = Context(mocker.stub())
    c.push_bracket('(')

    with pytest.raises(MismatchedBracketException):
        c.pop_bracket('[')


def test_current():
    c = Context(stream='')
    result = c.current

    assert result == ''


def test_current_position():
    c = Context(stream=Stream('123'))
    c.advance()
    c.advance()
    result = c.current_position

    assert isinstance(result, Position)


def test_advance():
    c = Context(stream=Stream('123'))

    position, character = c.advance()
    assert character == ''
    assert position is None

    position, character = c.advance()
    assert character == '1'
    assert position.index == 0
    assert position.line == 1
    assert position.column == 1


def test_advance_next():
    c = Context(stream=Stream('123'))
    c.advance()

    assert c.next == '1'
    assert c.next_position.index == 0
    assert c.next_position.line == 1
    assert c.next_position.column == 1


def test_advance_current():
    c = Context(stream=Stream('123'))
    c.advance()
    c.advance()

    assert c.current == '1'
    assert c.current_position.index == 0
    assert c.current_position.line == 1
    assert c.current_position.column == 1


def test_state(mocker):
    c = Context(stream='')
    state = mocker.stub()
    c.state = state

    assert c.state is state
