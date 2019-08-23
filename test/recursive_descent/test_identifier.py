#!/usr/bin/env python3

import pytest

from pylang.lexer.token import TokenType
from pylang.parse_tree import Identifier
from pylang.recursive_descent import Parser, UnexpectedTokenError


def test_identifier(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Identifier))

    result = p.identifier()

    assert isinstance(result, Identifier)
    assert result.value.token_type == TokenType.Identifier


def test_not_identifier(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Indent))

    with pytest.raises(UnexpectedTokenError):
        p.identifier()
