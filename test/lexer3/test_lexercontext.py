#!/usr/bin/env python3

import pytest

from pylang.lexer3 import LexerContext, MismatchedBracketException,  MismatchedIndentException


def test_init():
    l = LexerContext()

    assert 'l' in locals()


def test_push_indent():
    l = LexerContext()
    l.push_indent(length=0)

    assert True


def test_push_indent_mismatch():
    l = LexerContext()
    l.push_indent(length=0)

    with pytest.raises(MismatchedIndentException):
        l.push_indent(length=-1)


def test_pop_indent_one_level():
    l = LexerContext()
    l.push_indent(length=0)
    result = l.pop_indent(until=0)

    assert result == []


def test_pop_indent_multiple_levels():
    l = LexerContext()
    l.push_indent(length=0)
    l.push_indent(length=4)
    l.push_indent(length=8)
    result = l.pop_indent(until=0)

    assert result == [8, 4]


def test_pop_indent_mismatched():
    l = LexerContext()
    l.push_indent(length=0)

    with pytest.raises(MismatchedIndentException):
        l.pop_indent(until=-1)


def test_pop_indent_empty():
    l = LexerContext()

    with pytest.raises(MismatchedIndentException):
        l.pop_indent(until=0)


def test_push_bracket():
    l = LexerContext()
    l.push_bracket('(')

    assert True


def test_pop_bracket_matching():
    l = LexerContext()
    l.push_bracket(bracket='(')
    result = l.pop_bracket(expected='(')

    assert result == '('


def test_pop_bracket_mismatch():
    l = LexerContext()
    l.push_bracket('(')

    with pytest.raises(MismatchedBracketException):
        l.pop_bracket('[')
