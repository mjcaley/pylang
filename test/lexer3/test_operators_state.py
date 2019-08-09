#!/usr/bin/env python3

import pytest

from pylang.lexer3 import TokenType


def test_emit_plus_token(lexer):
    l = lexer('operators', '+')
    result = next(l)

    assert result.token_type == TokenType.Plus
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_plus_assign_token(lexer):
    l = lexer('operators', '+=')
    result = next(l)

    assert result.token_type == TokenType.PlusAssign
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_minus_token(lexer):
    l = lexer('operators', '-')
    result = next(l)

    assert result.token_type == TokenType.Minus
    assert l.next_position is None


def test_emit_minus_assign_token(lexer):
    l = lexer('operators', '-=')
    result = next(l)

    assert result.token_type == TokenType.MinusAssign
    assert l.next_position is None


def test_emit_multiply_token(lexer):
    l = lexer('operators', '*')
    result = next(l)

    assert result.token_type == TokenType.Multiply
    assert l.next_position is None


def test_emit_multiply_assign_token(lexer):
    l = lexer('operators', '*=')
    result = next(l)

    assert result.token_type == TokenType.MultiplyAssign
    assert l.next_position is None


def test_emit_divide_token(lexer):
    l = lexer('operators', '/')
    result = next(l)

    assert result.token_type == TokenType.Divide
    assert l.next_position is None


def test_emit_divide_assign_token(lexer):
    l = lexer('operators', '/=')
    result = next(l)

    assert result.token_type == TokenType.DivideAssign
    assert l.next_position is None


def test_emit_exponent_token(lexer):
    l = lexer('operators', '**')
    result = next(l)

    assert result.token_type == TokenType.Exponent
    assert l.next_position is None


def test_emit_exponent_assign_token(lexer):
    l = lexer('operators', '**=')
    result = next(l)

    assert result.token_type == TokenType.ExponentAssign
    assert l.next_position is None


def test_emit_modulo_token(lexer):
    l = lexer('operators', '%')
    result = next(l)

    assert result.token_type == TokenType.Modulo
    assert l.next_position is None


def test_emit_modulo_assign_token(lexer):
    l = lexer('operators', '%=')
    result = next(l)

    assert result.token_type == TokenType.ModuloAssign
    assert l.next_position is None


def test_emit_assignment_token(lexer):
    l = lexer('operators', '=')
    result = next(l)

    assert result.token_type == TokenType.Assignment
    assert l.next_position is None


def test_emit_equal_token(lexer):
    l = lexer('operators', '==')
    result = next(l)

    assert result.token_type == TokenType.Equal
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_not_equal_token(lexer):
    l = lexer('operators', '!=')
    result = next(l)

    assert result.token_type == TokenType.NotEqual
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_less_than_token(lexer):
    l = lexer('operators', '<')
    result = next(l)

    assert result.token_type == TokenType.LessThan
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_less_than_or_equal_token(lexer):
    l = lexer('operators', '<=')
    result = next(l)

    assert result.token_type == TokenType.LessThanOrEqual
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_greater_than_token(lexer):
    l = lexer('operators', '>')
    result = next(l)

    assert result.token_type == TokenType.GreaterThan
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_greater_or_equal_than_token(lexer):
    l = lexer('operators', '>=')
    result = next(l)

    assert result.token_type == TokenType.GreaterThanOrEqual
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_dot_token(lexer):
    l = lexer('operators', '.')
    result = next(l)

    assert result.token_type == TokenType.Dot
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_colon_token(lexer):
    l = lexer('operators', ':')
    result = next(l)

    assert result.token_type == TokenType.Colon
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_comma_token(lexer):
    l = lexer('operators', ',')
    result = next(l)

    assert result.token_type == TokenType.Comma
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_left_parentheses_token(lexer):
    l = lexer('operators', '(')
    result = next(l)

    assert result.token_type == TokenType.LParen
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_left_square_token(lexer):
    l = lexer('operators', '[')
    result = next(l)

    assert result.token_type == TokenType.LSquare
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_left_brace_token(lexer):
    l = lexer('operators', '{')
    result = next(l)

    assert result.token_type == TokenType.LBrace
    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert l.next_position is None


def test_emit_right_parentheses_token(lexer):
    l = lexer('operators', '()')
    next(l)
    result = next(l)

    assert result.token_type == TokenType.RParen
    assert result.position.index == 1
    assert result.position.line == 1
    assert result.position.column == 2
    assert l.next_position is None


def test_emit_right_parentheses_error_token(lexer):
    l = lexer('operators', '[)')
    next(l)
    result = next(l)

    assert result.token_type == TokenType.Error
    assert result.position.index == 1
    assert result.position.line == 1
    assert result.position.column == 2
    assert l.next_position is None


def test_emit_right_square_token(lexer):
    l = lexer('operators', '[]')
    next(l)
    result = next(l)

    assert result.token_type == TokenType.RSquare
    assert result.position.index == 1
    assert result.position.line == 1
    assert result.position.column == 2
    assert l.next_position is None


def test_emit_right_square_error_token(lexer):
    l = lexer('operators', '(]')
    next(l)
    result = next(l)

    assert result.token_type == TokenType.Error
    assert result.position.index == 1
    assert result.position.line == 1
    assert result.position.column == 2
    assert l.next_position is None


def test_emit_right_brace_token(lexer):
    l = lexer('operators', '{}')
    next(l)
    result = next(l)

    assert result.token_type == TokenType.RBrace
    assert result.position.index == 1
    assert result.position.line == 1
    assert result.position.column == 2
    assert l.next_position is None


def test_emit_right_brace_error_token(lexer):
    l = lexer('operators', '[}')
    next(l)
    result = next(l)

    assert result.token_type == TokenType.Error
    assert result.position.index == 1
    assert result.position.line == 1
    assert result.position.column == 2
    assert l.next_position is None


def test_emit_exclamation_error_token(lexer):
    l = lexer('operators', '!')
    result = next(l)

    assert result.token_type == TokenType.Error


@pytest.mark.xfail
def test_transition_to_number(lexer):
    l = lexer('operators', '123')
    state = l.state
    next(l)

    assert state != l.state


@pytest.mark.xfail
def test_transition_to_word(lexer):
    l = lexer('operators', 'abc')
    state = l.state
    next(l)

    assert state != l.state


@pytest.mark.xfail
def test_transition_to_string(lexer):
    l = lexer('operators', '"abc"')
    state = l.state
    next(l)

    assert state != l.state
