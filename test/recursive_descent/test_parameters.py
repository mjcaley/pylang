#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedToken
from pylang.parse_tree import Identifier


@pytest.mark.parametrize('test_input,length', [
    ['abc', 1],
    ['abc, def, ghi', 3]
])
def test_parameters(test_input, length):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.parameters()

    assert length == len(result)
    for node in result:
        assert isinstance(node, Identifier)


def test_parameters_raises():
    l = Lexer('abc,')
    l.emit()
    p = Parser(l)

    with pytest.raises(UnexpectedToken):
        p.parameters()
