#!/usr/bin/env python3

import pytest

from pylang.lexer.token import TokenType
from pylang.parse_tree import Boolean
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.mark.parametrize('token_type', [
    TokenType.True_, TokenType.False_
])
def test_bool(token_type, tokens_from_types):
    p = Parser(lexer=tokens_from_types(token_type))
    result = p.bool()

    assert isinstance(result, Boolean)
    assert token_type == result.value.token_type


def test_bool_exception(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Indent))

    with pytest.raises(UnexpectedTokenError):
        p.bool()
