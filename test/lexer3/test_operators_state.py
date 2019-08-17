#!/usr/bin/env python3

import pytest

from pylang.lexer3.states import Operators, End
from pylang.lexer3.token import TokenType


def test_eof_transitions_to_file_end(context):
    o = Operators(context(''))
    result = o()

    assert isinstance(result[0], End)
    assert result[1].token_type == TokenType.Dedent
    assert result[1].position is None


@pytest.mark.parametrize('test_input,token_type', [
    ('+', TokenType.Plus),
    ('-', TokenType.Minus),
    ('*', TokenType.Multiply),
    ('/', TokenType.Divide),
    ('%', TokenType.Modulo),
    ('**', TokenType.Exponent),
    ('=', TokenType.Assignment),
    ('<', TokenType.LessThan),
    ('>', TokenType.GreaterThan),
    ('.', TokenType.Dot),
    (':', TokenType.Colon),
    (',', TokenType.Comma),
    ('==', TokenType.Equal),
    ('<=', TokenType.LessThanOrEqual),
    ('>=', TokenType.GreaterThanOrEqual),
    ('!=', TokenType.NotEqual),
    ('+=', TokenType.PlusAssign),
    ('-=', TokenType.MinusAssign),
    ('*=', TokenType.MultiplyAssign),
    ('/=', TokenType.DivideAssign),
    ('%=', TokenType.ModuloAssign),
    ('**=', TokenType.ExponentAssign),
])
def test_call_token(context_at_next, test_input, token_type):
    o = Operators(context_at_next(test_input))
    result = o()

    assert isinstance(result[0], Operators)
    assert result[1].token_type == token_type
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1


def test_error_with_invalid_input(context_at_next):
    o = Operators(context_at_next('!'))
    result = o()

    assert isinstance(result[0], Operators)
    assert result[1].token_type == TokenType.Error
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1


@pytest.mark.parametrize('test_input,token_type', [
    ('(', TokenType.LParen),
    ('[', TokenType.LSquare),
    ('{', TokenType.LBrace),
])
def test_call_left_bracket(mocker, context_at_next, test_input, token_type):
    o = Operators(context_at_next(test_input))
    mocker.spy(o.context, 'push_bracket')
    result = o()

    assert isinstance(result[0], Operators)
    assert result[1].token_type == token_type
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
    assert o.context.push_bracket.called


@pytest.mark.parametrize('test_input,left_bracket,token_type', [
    (')', '(', TokenType.RParen),
    (']', '[', TokenType.RSquare),
    ('}', '{', TokenType.RBrace),
])
def test_call_right_bracket(mocker, context_at_next, test_input, left_bracket, token_type):
    o = Operators(context_at_next(test_input))
    o.context.push_bracket(left_bracket)
    mocker.spy(o.context, 'pop_bracket')
    result = o()

    assert isinstance(result[0], Operators)
    assert result[1].token_type == token_type
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
    assert o.context.pop_bracket.called


@pytest.mark.parametrize('test_input', [
    ')', ']', '}'
])
def test_right_bracket_mismatched(mocker, context_at_next, test_input):
    o = Operators(context_at_next(test_input))
    o.context.push_bracket('\0')
    mocker.spy(o.context, 'pop_bracket')
    result = o()

    assert isinstance(result[0], Operators)
    assert result[1].token_type == TokenType.Error
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
    assert o.context.pop_bracket.called
