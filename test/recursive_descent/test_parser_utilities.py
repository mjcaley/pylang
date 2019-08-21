#!/usr/bin/env python3

import pytest

from pylang.lexer.token import Token, TokenType
from pylang.lexer.stream import Position
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.fixture
def lexer_digits():
    return [
        Token(TokenType.Indent, Position(0, 1, 1)),
        Token(TokenType.Integer, Position(1, 1, 2), 1),
        Token(TokenType.Float, Position(1, 1, 2), 1),
        Token(TokenType.Dedent, Position(2, 1, 3)),
    ]


def test_current(lexer_digits):
    p = Parser(lexer_digits)

    assert p.current.token_type == TokenType.Indent


def test_next(lexer_digits):
    p = Parser(lexer_digits)

    assert p.next.token_type == TokenType.Integer
    assert p.next.value == 1


def test_match_current(lexer_digits):
    p = Parser(lexer_digits)

    assert p.match_current(TokenType.Indent) is True


def test_match_next(lexer_digits):
    p = Parser(lexer_digits)

    assert p.match_next(TokenType.Integer) is True


def test_match(lexer_digits):
    p = Parser(lexer_digits)

    assert p.match(current_type=TokenType.Indent)
    assert p.match(current_type=TokenType.Indent, next_type=TokenType.Integer)


def test_advance(lexer_digits):
    p = Parser(lexer_digits)
    token = p.advance()

    assert token.token_type == TokenType.Integer
    assert token.value == 1
    assert p.current == token


def test_consume(lexer_digits):
    p = Parser(lexer_digits)

    first_token = p.current
    next_token = p.consume()

    assert first_token == next_token
    assert p.current != next_token


def test_consume_if_success(lexer_digits):
    p = Parser(lexer_digits)
    current_token = p.current
    token = p.consume_if(TokenType.Indent)

    assert current_token == token


def test_consume_if_fail(lexer_digits):
    p = Parser(lexer_digits)
    current_token = p.current
    token = p.consume_if(TokenType.Dedent)

    assert current_token != token


def test_consume_if2_success_one(lexer_digits):
    match = lexer_digits[0].token_type
    p = Parser(lexer_digits)
    result = p.consume_if2(match)

    assert result[0].token_type == match


def test_consume_if2_success_multiple(lexer_digits):
    match = [token.token_type for token in lexer_digits[:3]]
    p = Parser(lexer_digits)
    result = p.consume_if2(*match)

    assert result[0] == lexer_digits[0]
    assert result[1] == lexer_digits[1]
    assert result[2] == lexer_digits[2]
    assert len(result) == 3


def test_consume_if2_fail_first(lexer_digits):
    p = Parser(lexer_digits)
    result = p.consume_if2(TokenType.Error)

    assert len(result) == 0


def test_consume_if2_fail_partial(lexer_digits):
    p = Parser(lexer_digits)
    result = p.consume_if2(TokenType.Indent, TokenType.Integer, TokenType.Integer)

    assert result[0] == lexer_digits[0]
    assert result[1] == lexer_digits[1]
    assert len(result) == 2


def test_consume_try2_success_one(lexer_digits):
    p = Parser(lexer_digits)
    result = p.consume_try2(TokenType.Indent)

    assert result[0] == lexer_digits[0]
    assert len(result) == 1


def test_consume_try2_success_multiple(lexer_digits):
    p = Parser(lexer_digits)
    result = p.consume_try2(TokenType.Indent, TokenType.Integer, TokenType.Dedent)

    assert result[0] == lexer_digits[0]
    assert result[1] == lexer_digits[1]
    assert result[2] == lexer_digits[2]
    assert len(result) == 3


@pytest.mark.parametrize('test_input', [
    [TokenType.Error],
    [TokenType.Indent, TokenType.Error],
    [TokenType.Indent, TokenType.Integer, TokenType.Dedent, TokenType.Indent],
])
def test_consume_try2_fails(test_input, lexer_digits):
    p = Parser(lexer_digits)

    with pytest.raises(UnexpectedTokenError):
        p.consume_try2(*test_input)


def test_consume_try_success(lexer_digits):
    p = Parser(lexer_digits)
    current_token = p.current
    token = p.consume_try(TokenType.Indent)

    assert current_token == token


def test_consume_try_fail(lexer_digits):
    p = Parser(lexer_digits)

    with pytest.raises(UnexpectedTokenError):
        p.consume_try(TokenType.Dedent)


def test_eof(lexer_digits):
    p = Parser(lexer_digits)

    p.advance()
    assert p.eof() is False     # Current is Digits
    p.advance()
    assert p.eof() is False     # Current is Dedent

    p.advance()
    assert p.eof() is True
