#!/usr/bin/env python3

import pytest

from pylang.lexer.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedTokenError
from pylang.parse_tree import Identifier


@pytest.mark.parametrize('test_input,length', [
    ['abc', 1],
    ['abc, def, ghi', 3]
])
def test_parameters(test_input, length):
    l = Lexer.from_stream(test_input)
    next(l)
    p = Parser(lexer=l)

    result = p.parameters()

    assert length == len(result)
    for node in result:
        assert isinstance(node, Identifier)


def test_parameters_raises():
    l = Lexer.from_stream('abc,')
    next(l)
    p = Parser(l)

    with pytest.raises(UnexpectedTokenError):
        p.parameters()
