#!/usr/bin/env python3

import pytest

from pylang.lexer import TokenType
from pylang.recursive_descent import Parser, UnexpectedTokenError


@pytest.fixture
def lexer_digits():
    from pylang.lexer import Lexer
    return Lexer('1')


def test_current(lexer_digits):
    p = Parser(lexer_digits)

    assert p.current().token_type == TokenType.Indent


def test_next(lexer_digits):
    p = Parser(lexer_digits)

    assert p.next().token_type == TokenType.Digits
    assert p.next().value == 1


def test_match_current(lexer_digits):
    p = Parser(lexer_digits)

    assert p.match_current(TokenType.Indent) is True


def test_match_next(lexer_digits):
    p = Parser(lexer_digits)

    assert p.match_next(TokenType.Digits) is True


def test_match(lexer_digits):
    p = Parser(lexer_digits)

    assert p.match(current_type=TokenType.Indent)
    assert p.match(current_type=TokenType.Indent, next_type=TokenType.Digits)


def test_advance(lexer_digits):
    p = Parser(lexer_digits)
    token = p.advance()

    assert token.token_type == TokenType.Digits
    assert token.value == 1
    assert p.current() == token


def test_consume(lexer_digits):
    p = Parser(lexer_digits)

    first_token = p.current()
    next_token = p.consume()

    assert first_token == next_token
    assert p.current() != next_token


def test_consume_if_success(lexer_digits):
    p = Parser(lexer_digits)
    current_token = p.current()
    token = p.consume_if(TokenType.Indent)

    assert current_token == token


def test_consume_if_fail(lexer_digits):
    p = Parser(lexer_digits)
    current_token = p.current()
    token = p.consume_if(TokenType.Dedent)

    assert current_token != token


def test_consume_try_success(lexer_digits):
    p = Parser(lexer_digits)
    current_token = p.current()
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
