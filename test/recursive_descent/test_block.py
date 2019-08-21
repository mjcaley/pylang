#!/usr/bin/env python3

import pytest

from pylang.lexer.lexer import Lexer
from pylang.recursive_descent import Parser


@pytest.mark.parametrize('test_input', [
    '\t42\n\t4.2\n\ttrue\n',
    '    42\r\n    4.2\r\n    true\r\n'
])
def test_block(test_input):
    l = Lexer.from_stream(test_input)
    next(l)
    p = Parser(lexer=l)

    result = p.block()

    assert isinstance(result, list)
