#!/usr/bin/env python3

import pytest

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser, UnexpectedTokenError


def test_statement(tokens_from_types):
    tokens = tokens_from_types(TokenType.Integer, TokenType.Plus, TokenType.Integer, TokenType.Newline)
    p = Parser(lexer=tokens)
    result = p.statement()

    assert result is not None


def test_statement_without_newline(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Integer))

    with pytest.raises(UnexpectedTokenError):
        p.statement()
