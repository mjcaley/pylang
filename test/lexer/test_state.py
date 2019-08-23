#!/usr/bin/env python3

from string import digits

import pytest

from pylang.lexer.characters import WHITESPACE
from pylang.lexer.states import State


@pytest.mark.parametrize('test_input', [
    '123', '123_'
])
def test_append_while(context_at_current, test_input):
    s = State(context_at_current(test_input))
    result = s.append_while(digits)

    assert result == '123'


def test_append_while_not(context_at_current):
    s = State(context_at_current('123'))
    result = s.append_while_not(WHITESPACE)

    assert result == '123'


def test_skip_whitespace(context_at_current):
    s = State(context_at_current('  123'))
    s.skip_whitespace()

    assert s.context.current == '1'
    assert s.context.current_position.index == 2
    assert s.context.current_position.line == 1
    assert s.context.current_position.column == 3


def test_skip_until(context_at_current):
    s = State(context_at_current('  123'))
    s.skip_until(digits)

    assert s.context.current == '1'
    assert s.context.current_position.index == 2
    assert s.context.current_position.line == 1
    assert s.context.current_position.column == 3


def test_skip_while(context_at_current):
    s = State(context_at_current('  123'))
    s.skip_while(WHITESPACE)

    assert s.context.current == '1'
    assert s.context.current_position.index == 2
    assert s.context.current_position.line == 1
    assert s.context.current_position.column == 3


def test_match(context_at_current):
    s = State(context_at_current('123'))

    assert s.match('1')


def test_match_next(context_at_next):
    s = State(context_at_next('123'))

    assert s.match_next('1')


def test_current_in(context_at_current):
    s = State(context_at_current('123'))

    assert s.current_in(digits)


def test_next_in(context_at_current):
    s = State(context_at_current('123'))

    assert s.next_in(digits)


def test_call(mocker):
    s = State(mocker.stub())

    with pytest.raises(NotImplementedError):
        assert s()


def test_eof_true(context_at_current):
    s = State(context_at_current(''))

    assert s.eof is True


def test_eof_false(context_at_current):
    s = State(context_at_current('123'))

    assert s.eof is False
