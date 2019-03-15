#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedToken
from pylang.parse_tree import Identifier


@pytest.mark.parametrize('test_input', [
    '()',
    '(abc)'
    '(abc, def, ghi)'
])
def test_parameters(test_input):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.parameters()

    for node in result:
        assert isinstance(node, Identifier)


@pytest.mark.parametrize('test_input', [
    'abc',
    '(42',
    '(abc def)'
])
def test_parameters_raises(test_input):
    l = Lexer(test_input)
    l.emit()
    p = Parser(l)

    with pytest.raises(UnexpectedToken):
        p.parameters()
