#!/usr/bin/env python3

from pylang.lexer.token import TokenType
from pylang.recursive_descent import Parser
from pylang.parse_tree import FunctionDecl


def test_function_no_param_no_return(tokens_from_types):
    tokens = tokens_from_types(
        TokenType.Function,
        TokenType.Identifier,
        TokenType.LParen,
        TokenType.RParen,
        TokenType.Assignment,
        TokenType.Newline
    )
    tokens[1].value = 'name'
    p = Parser(lexer=tokens)
    result = p.function_decl()

    assert isinstance(result, FunctionDecl)
    assert result.name.value.value == 'name'
    assert result.parameters == []
    assert result.return_type is None


def test_function_one_param_no_return(tokens_from_types):
    tokens = tokens_from_types(
        TokenType.Function,
        TokenType.Identifier,
        TokenType.LParen,
        TokenType.Identifier,
        TokenType.RParen,
        TokenType.Assignment,
        TokenType.Newline
    )
    tokens[1].value = 'name'
    tokens[3].value = 'param'
    p = Parser(lexer=tokens)
    result = p.function_decl()

    assert isinstance(result, FunctionDecl)
    assert result.name.value.value == 'name'
    assert result.parameters[0].value.value == 'param'
    assert len(result.parameters) == 1
    assert result.return_type is None


def test_function_multiple_param_no_return(tokens_from_types):
    tokens = tokens_from_types(
        TokenType.Function,
        TokenType.Identifier,
        TokenType.LParen,
        TokenType.Identifier,
        TokenType.Comma,
        TokenType.Identifier,
        TokenType.RParen,
        TokenType.Assignment,
        TokenType.Newline
    )
    tokens[1].value = 'name'
    tokens[3].value = 'param1'
    tokens[5].value = 'param2'
    p = Parser(lexer=tokens)
    result = p.function_decl()

    assert isinstance(result, FunctionDecl)
    assert result.name.value.value == 'name'
    assert result.parameters[0].value.value == 'param1'
    assert result.parameters[1].value.value == 'param2'
    assert len(result.parameters) == 2
    assert result.return_type is None


def test_function_no_param_with_return(tokens_from_types):
    tokens = tokens_from_types(
        TokenType.Function,
        TokenType.Identifier,
        TokenType.LParen,
        TokenType.RParen,
        TokenType.Colon,
        TokenType.Identifier,
        TokenType.Assignment,
        TokenType.Newline
    )
    tokens[1].value = 'name'
    tokens[5].value = 'return'
    p = Parser(lexer=tokens)
    result = p.function_decl()

    assert isinstance(result, FunctionDecl)
    assert result.name.value.value == 'name'
    assert len(result.parameters) == 0
    assert result.return_type.value.value == 'return'
