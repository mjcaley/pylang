#!/usr/bin/env python3

import pytest

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser


def test_integer(tokens_from_types):
    tokens = tokens_from_types(TokenType.Integer)
    p = Parser(lexer=tokens)
    result = p.integer()

    assert result.value is tokens[0]
