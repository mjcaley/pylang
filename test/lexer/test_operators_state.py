#!/usr/bin/env python3

import pytest

from pylang.lexer.states import Operators
from pylang.lexer.token import TokenType


def test_eof_transitions_to_indent(context, mocker):
    o = Operators(context(''))
    mocked_indent = mocker.patch('pylang.lexer.states.Indent')
    called_instance = mocked_indent()()
    result = o()

    assert result == called_instance


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
def test_call_token(context_at_current, test_input, token_type, mocker):
    o = Operators(context_at_current(test_input))
    mocked_indent = mocker.patch('pylang.lexer.states.Indent')
    instance = mocked_indent()
    mocker.spy(o.context, 'advance')
    result = o()

    assert result[0] == instance
    assert result[1].token_type == token_type
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
    assert o.context.advance.call_count == len(test_input)


def test_call_newline(context_at_current, mocker):
    o = Operators(context_at_current('\n'))
    mocked_indent = mocker.patch('pylang.lexer.states.Indent')
    instance = mocked_indent()
    mocker.spy(o.context, 'advance')
    result = o()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Newline
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 0
    assert o.context.advance.call_count == 1


def test_error_with_invalid_input(context_at_current, mocker):
    o = Operators(context_at_current('!'))
    mocked_indent = mocker.patch('pylang.lexer.states.Indent')
    instance = mocked_indent()
    result = o()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Error
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1


@pytest.mark.parametrize('test_input,token_type', [
    ('(', TokenType.LParen),
    ('[', TokenType.LSquare),
    ('{', TokenType.LBrace),
])
def test_call_left_bracket(mocker, context_at_current, test_input, token_type):
    o = Operators(context_at_current(test_input))
    mocked_indent = mocker.patch('pylang.lexer.states.Indent')
    instance = mocked_indent()
    mocker.spy(o.context, 'push_bracket')
    result = o()

    assert result[0] == instance
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
def test_call_right_bracket(mocker, context_at_current, test_input, left_bracket, token_type):
    o = Operators(context_at_current(test_input))
    o.context.push_bracket(left_bracket)
    mocked_indent = mocker.patch('pylang.lexer.states.Indent')
    instance = mocked_indent()
    mocker.spy(o.context, 'pop_bracket')
    result = o()

    assert result[0] == instance
    assert result[1].token_type == token_type
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
    assert o.context.pop_bracket.called


@pytest.mark.parametrize('test_input', [
    ')', ']', '}'
])
def test_right_bracket_mismatched(mocker, context_at_current, test_input):
    o = Operators(context_at_current(test_input))
    o.context.push_bracket('\0')
    mocked_indent = mocker.patch('pylang.lexer.states.Indent')
    instance = mocked_indent()
    mocker.spy(o.context, 'pop_bracket')
    result = o()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Error
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
    assert o.context.pop_bracket.called


@pytest.mark.parametrize('test_input', [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
])
def test_digit_transitions_to_number_state(context_at_current, mocker, test_input):
    o = Operators(context_at_current(test_input))
    mocked_number = mocker.patch('pylang.lexer.states.Number')
    called_instance = mocked_number()()
    result = o()

    assert result == called_instance


def test_double_quote_transitions_to_string_state(context_at_current, mocker):
    o = Operators(context_at_current('"'))
    mocked_string = mocker.patch('pylang.lexer.states.String')
    called_instance = mocked_string()()
    result = o()

    assert result == called_instance


@pytest.mark.parametrize('test_input', [
    'a', 'b', 'c', '_'
])
def test_non_reserved_character_or_digit_transitions_to_word_state(context_at_current, mocker, test_input):
    o = Operators(context_at_current('a'))
    mocked_word = mocker.patch('pylang.lexer.states.Word')
    called_instance = mocked_word()()
    result = o()
    
    assert result == called_instance
