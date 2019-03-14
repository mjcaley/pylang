#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedToken
from pylang.parse_tree import Boolean, Float, Identifier, Integer


@pytest.mark.parametrize('test_input,expected', [
    ['42', Integer],
    ['4.2', Float],
    ['abc', Identifier],
    ['true', Boolean]
])
def test_identifier(test_input, expected):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.atom()

    assert isinstance(result, expected)


@pytest.mark.parametrize('test_input', [
    'func',
    'struct',
    'if',
    'elif',
    'else',
    'while',
    'for',
    'and',
    'or',
    'not'
])
def test_keywords(test_input):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    with pytest.raises(UnexpectedToken):
        p.atom()
