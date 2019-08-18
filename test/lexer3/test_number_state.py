#!/usr/bin/env python3

import pytest

from string import digits

from pylang.lexer3.exceptions import InvalidNumberInputException
from pylang.lexer3.states import Number, Operators
from pylang.lexer3.token import TokenType


@pytest.mark.parametrize('test_input', [
    '123',
    '1_2_3',
    '_123'
])
def test_consume_number(context_at_current, test_input):
    n = Number(context_at_current(test_input))
    result = n.consume_number(digits)

    assert result == '123'


@pytest.mark.parametrize('test_input', [
    '123_',
    '1__2__3'
])
def test_consume_number_raises(context_at_current, test_input):
    n = Number(context_at_current(test_input))

    with pytest.raises(InvalidNumberInputException):
        n.consume_number(digits)


@pytest.mark.parametrize('test_input', [
    '42',
    '4_2',
    '0x2a',
    '0x2_a',
    '0x_2a',
    '0b101010',
    '0b10_10_10',
    '0b_101010',
    '0o52',
    '0o5_2',
    '0o_52'
])
def test_read_numbers(context_at_current, test_input):
    n = Number(context_at_current(test_input))
    result = n.read_number()

    assert result == 42


@pytest.mark.parametrize('test_input,token_type', [
    ('42', TokenType.Integer),
    ('0x2a', TokenType.Integer),
    ('0b101010', TokenType.Integer),
    ('0o52', TokenType.Integer),
])
def test_call_token(context_at_current, test_input, token_type):
    n = Number(context_at_current(test_input))
    result = n()

    assert isinstance(result[0], Operators)
    assert result[1].token_type == token_type
    assert result[1].value == 42
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
