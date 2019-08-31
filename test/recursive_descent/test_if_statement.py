#!/usr/bin/env python3

from pylang.lexer.token import TokenType
from pylang.parse_tree import Branch
from pylang.recursive_descent import Parser


def test_if_statement(tokens_from_types):
    tokens = tokens_from_types(
        TokenType.If, TokenType.True_, TokenType.Colon,
        TokenType.Indent, TokenType.Dedent)
    p = Parser(lexer=tokens)
    result = p.statement()

    assert isinstance(result, Branch)
    assert result.condition.value is tokens[1]
    assert result.then_branch is not None
    assert result.else_branch == []


def test_if_else_statement(tokens_from_types):
    tokens = tokens_from_types(
        TokenType.If, TokenType.True_, TokenType.Colon,
        TokenType.Indent, TokenType.Dedent,
        TokenType.Else, TokenType.Colon, TokenType.Newline,
        TokenType.Indent, TokenType.Dedent)
    p = Parser(lexer=tokens)
    result = p.if_statement()

    assert isinstance(result, Branch)
    assert result.condition.value is tokens[1]
    assert result.then_branch is not None
    assert result.else_branch is not None


def test_if_elseif_statement(tokens_from_types):
    tokens = tokens_from_types(
        TokenType.If, TokenType.True_, TokenType.Colon,
        TokenType.Indent, TokenType.Dedent,
        TokenType.ElseIf, TokenType.False_, TokenType.Colon, TokenType.Newline,
        TokenType.Indent, TokenType.Dedent)
    p = Parser(lexer=tokens)
    result = p.if_statement()

    assert isinstance(result, Branch)
    assert result.condition.value is tokens[1]
    assert result.then_branch is not None
    assert isinstance(result.else_branch, Branch)
