#!/usr/bin/env python3

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser
from pylang.parse_tree import Function, FunctionDecl


def test_function(tokens_from_types, mocker):
    tokens = tokens_from_types(
        TokenType.Function,
        TokenType.Identifier,
        TokenType.LParen,
        TokenType.RParen,
        TokenType.Assignment,
        TokenType.Newline,
        TokenType.Indent,
        TokenType.Dedent
    )
    p = Parser(lexer=tokens)
    block_spy = mocker.spy(p, 'block')

    result = p.function()

    assert isinstance(result, Function)
    assert isinstance(result.definition, FunctionDecl)
    assert isinstance(result.block, list)
    assert block_spy.called
