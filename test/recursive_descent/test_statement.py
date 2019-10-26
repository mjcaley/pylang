#!/usr/bin/env python3

import pytest

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.mark.parametrize('token,mock_func', [
    [TokenType.Function, 'function'],
    [TokenType.If, 'if_statement'],
])
def test_statement(tokens_from_types, token, mock_func, mocker):
    p = Parser(lexer=tokens_from_types(token))
    mocked_func = mocker.patch(f'pylang.recursive_descent.Parser.{mock_func}')
    result = p.statement()

    assert mocked_func.called
    assert result == mocked_func.return_value


def test_statement_expression(tokens_from_types, mocker):
    p = Parser(lexer=tokens_from_types(TokenType.True_, TokenType.Newline))
    mocker.spy(p, 'expression')
    result = p.statement()

    assert p.expression.called


def test_statement_without_newline(tokens_from_types):
    p = Parser(lexer=tokens_from_types(TokenType.Integer))

    with pytest.raises(UnexpectedTokenError):
        p.statement()
