#!/usr/bin/env python3

import pytest

from pylang.lexer.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedTokenError
from pylang.parse_tree import Boolean, Float, Identifier, Integer


@pytest.mark.parametrize('test_input,expected', [
    ['42', Integer],
    ['4.2', Float],
    ['abc', Identifier],
    ['true', Boolean],
    ['(42)', Integer]
])
def test_atom_types(test_input, expected):
    l = Lexer.from_stream(test_input)
    next(l)
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
    l = Lexer.from_stream(test_input)
    next(l)
    p = Parser(lexer=l)

    with pytest.raises(UnexpectedTokenError):
        p.atom()
