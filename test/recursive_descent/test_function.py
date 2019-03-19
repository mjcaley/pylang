#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedTokenError
from pylang.parse_tree import Function, FunctionDecl


@pytest.mark.parametrize('test_input', [
    'func functionName() = \n\ttrue\n',
])
def test_function(test_input):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.function()

    assert isinstance(result, Function)
    assert isinstance(result.definition, FunctionDecl)
    assert isinstance(result.block, list)


@pytest.mark.parametrize('test_input', [
    'func functionName()',
    'func functionName() = '
])
def test_function_raises(test_input):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    with pytest.raises(UnexpectedTokenError):
        p.function()
