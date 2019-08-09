#!/usr/bin/env python3

import pytest

from pylang.lexer3 import Lexer, Position, WHITESPACE, digits, TokenType


def test_iter():
    l = Lexer('')
    iterator = iter(l)

    assert 'iterator' in locals()


def test_next():
    l = Lexer('')
    result = next(l)

    assert result is not None


def test_current():
    l = Lexer('')
    result = l.current

    assert result == ''


def test_current_position():
    l = Lexer('123')
    l.advance()
    l.advance()
    result = l.current_position

    assert isinstance(result, Position)


def test_advance():
    l = Lexer('123')

    position, character = l.advance()
    assert character == ''
    assert position is None

    position, character = l.advance()
    assert character == '1'
    assert position.index == 0
    assert position.line == 1
    assert position.column == 1


def test_advance_next():
    l = Lexer('123')
    l.advance()

    assert l.next == '1'
    assert l.next_position.index == 0
    assert l.next_position.line == 1
    assert l.next_position.column == 1


def test_advance_current():
    l = Lexer('123')
    l.advance()
    l.advance()

    assert l.current == '1'
    assert l.current_position.index == 0
    assert l.current_position.line == 1
    assert l.current_position.column == 1


def test_append_while():
    l = Lexer('123')
    l.advance()
    result = l.append_while(digits)

    assert result == '123'


def test_append_while_not():
    l = Lexer('123')
    l.advance()
    result = l.append_while_not(WHITESPACE)

    assert result == '123'


def test_skip_whitespace():
    l = Lexer('  123')
    l.advance()
    l.skip_whitespace()

    assert l.current == '1'
    assert l.current_position.index == 2
    assert l.current_position.line == 1
    assert l.current_position.column == 3


def test_skip_until():
    l = Lexer('  123')
    l.advance()
    l.skip_until(digits)

    assert l.current == '1'
    assert l.current_position.index == 2
    assert l.current_position.line == 1
    assert l.current_position.column == 3


def test_skip_while():
    l = Lexer('  123')
    l.advance()
    l.skip_while(WHITESPACE)

    assert l.current == '1'
    assert l.current_position.index == 2
    assert l.current_position.line == 1
    assert l.current_position.column == 3


@pytest.mark.xfail
def test_skip_empty_lines():
    # not sure if keeping the method
    assert False


def test_match():
    l = Lexer('123')
    l.advance()
    l.advance()

    assert l.match('1')


def test_match_next():
    l = Lexer('123')
    l.advance()

    assert l.match_next('1')


def test_current_in():
    l = Lexer('123')
    l.advance()
    l.advance()

    assert l.current_in(digits)


def test_next_in():
    l = Lexer('123')
    l.advance()

    assert l.next_in(digits)
