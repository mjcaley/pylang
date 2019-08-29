#!/usr/bin/env python3

import pytest

from pylang.lexer.token import TokenType
from pylang.parse_tree import Float
from pylang.recursive_descent import Parser, UnexpectedTokenError


def test_float(tokens_from_types):
    tokens = tokens_from_types(TokenType.Float)
    p = Parser(lexer=tokens)
    result = p.float()

    assert isinstance(result, Float)
    assert result.value is tokens[0]
