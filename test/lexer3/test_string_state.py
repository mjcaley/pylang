#!/usr/bin/env python3

import pytest

from pylang.lexer3.states import String
from pylang.lexer3.token import TokenType


def test_eof_emits_error_and_transitions_to_indent(context_at_current, mocker):
    s = String(context_at_current('"'))
    mocked_indent = mocker.patch('pylang.lexer3.states.Indent')
    instance = mocked_indent()
    result = s()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Error
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1


def test_emit_single_quoted_string(context_at_current, mocker):
    value = 'The quick brown fox jumped over the lazy dog.'
    s = String(context_at_current(f'"{value}"'))
    mocked_indent = mocker.patch('pylang.lexer3.states.Indent')
    instance = mocked_indent()
    result = s()

    assert result[0] == instance
    assert result[1].token_type == TokenType.String
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
    assert result[1].value == value


def test_eof_in_middle_of_single_quoted_string(context_at_current, mocker):
    value = 'The quick brown fox jumped over the lazy dog.'
    s = String(context_at_current(f'"{value}\n"'))
    mocked_indent = mocker.patch('pylang.lexer3.states.Indent')
    instance = mocked_indent()
    result = s()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Error


@pytest.mark.parametrize('test_input,expected', [
    (r'\a', '\a'),
    (r'\b', '\b'),
    (r'\f', '\f'),
    (r'\n', '\n'),
    (r'\r', '\r'),
    (r'\t', '\t'),
    (r'\v', '\v'),
    (r'\\', '\\'),
    (r'\"', '"'),
])
def test_parse_delimiters(test_input, expected, context_at_current, mocker):
    s = String(context_at_current(f'"{test_input}"'))
    mocked_indent = mocker.patch('pylang.lexer3.states.Indent')
    instance = mocked_indent()
    result = s()

    assert result[0] == instance
    assert result[1].token_type == TokenType.String
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
    assert result[1].value == expected
