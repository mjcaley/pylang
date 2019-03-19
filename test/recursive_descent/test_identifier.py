#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedTokenError
from pylang.parse_tree import Identifier


@pytest.mark.parametrize('test_input', [
    'abc',
    'abc123',
    '_abc',
    '_abc_123_',
    '\N{SIGN OF THE HORNS}'
])
def test_identifier(test_input):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.identifier()

    assert isinstance(result, Identifier)
    assert test_input == result.value


@pytest.mark.parametrize('test_input', [
    '123abc',
    '123',
    'true',
    'false',
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
def test_not_identifier(test_input):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    with pytest.raises(UnexpectedTokenError):
        p.identifier()
