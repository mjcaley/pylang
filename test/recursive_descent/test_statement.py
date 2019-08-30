#!/usr/bin/env python3

import pytest

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.mark.parametrize('token_stream,func_spy', [
    [[TokenType.True_, TokenType.Newline], 'atom'],
    [
        [TokenType.Function, TokenType.Identifier, TokenType.LParen, TokenType.RParen,
         TokenType.Assignment, TokenType.Newline, TokenType.Indent, TokenType.Dedent], 'function'
    ],
    [[TokenType.If, TokenType.True_, TokenType.Colon, TokenType.Indent, TokenType.Dedent], 'if_statement'],
    [
        [TokenType.If, TokenType.True_, TokenType.Colon, TokenType.Indent, TokenType.Dedent,
         TokenType.Else, TokenType.Colon, TokenType.Newline, TokenType.Indent, TokenType.Dedent], 'if_statement'
    ],
    [
        [TokenType.If, TokenType.True_, TokenType.Colon, TokenType.Indent, TokenType.Dedent,
         TokenType.ElseIf, TokenType.False_, TokenType.Colon,
         TokenType.Newline, TokenType.Indent, TokenType.Dedent], 'if_statement'
    ],
])
def test_statement(tokens_from_types, token_stream, func_spy, mocker):
    tokens = tokens_from_types(*token_stream)
    p = Parser(lexer=tokens)
    spy = mocker.spy(p, func_spy)
    result = p.statement()

    assert result is not None
    assert spy.called


def test_statement_without_newline(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Integer))

    with pytest.raises(UnexpectedTokenError):
        p.statement()
