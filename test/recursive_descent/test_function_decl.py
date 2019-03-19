#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer
from pylang.recursive_descent import Parser, UnexpectedTokenError
from pylang.parse_tree import FunctionDecl


@pytest.mark.parametrize('test_input,name,num_params,return_type', [
    ['func functionName()', 'functionName', 0, None],
    ['func functionName(abc)', 'functionName', 1, None],
    ['func functionName(abc, def, ghi)', 'functionName', 3, None],
    ['func functionName() : int', 'functionName', 0, 'int'],
    ['func functionName(abc) : int', 'functionName', 1, 'int'],
    ['func functionName(abc, def, ghi) : int', 'functionName', 3, 'int'],
])
def test_parameters(test_input, name, num_params, return_type):
    l = Lexer(test_input)
    l.emit()
    p = Parser(lexer=l)

    result = p.function_decl()

    assert isinstance(result, FunctionDecl)
    assert name == result.name.value
    assert num_params == len(result.parameters)
    if return_type:
        assert return_type == result.return_type.value
