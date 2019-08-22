#!/usr/bin/env python3

import pytest

from pylang.lexer.token import TokenType
from pylang.parse_tree import Float
from pylang.recursive_descent import Parser, UnexpectedTokenError


def test_float(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Float))
    result = p.float()

    assert isinstance(result, Float)
    assert result.value.token_type == TokenType.Float


def test_float_exception(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Indent))

    with pytest.raises(UnexpectedTokenError):
        p.float()
