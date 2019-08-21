#!/usr/bin/env python3

import pytest

from pylang.lexer3.states import Word
from pylang.lexer3.token import TokenType


def test_returns_identifier(context_at_current, mocker):
    w = Word(context_at_current('a'))
    mocked_indent = mocker.patch('pylang.lexer3.states.Indent')
    instance = mocked_indent()
    mocker.spy(w.context, 'advance')
    result = w()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Identifier
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
    assert w.context.advance.call_count == 1


@pytest.mark.parametrize('test_input,expected', [
    ('func', TokenType.Function),
    ('struct', TokenType.Struct),
    ('if', TokenType.If),
    ('elif', TokenType.ElseIf),
    ('else', TokenType.Else),
    ('while', TokenType.While),
    ('for', TokenType.ForEach),
    ('and', TokenType.And),
    ('not', TokenType.Not),
    ('or', TokenType.Or),
    ('true', TokenType.True_),
    ('false', TokenType.False_),
    ('return', TokenType.Return),
])
def test_returns_keyword(context_at_current, test_input, expected, mocker):
    w = Word(context_at_current(test_input))
    mocked_indent = mocker.patch('pylang.lexer3.states.Indent')
    instance = mocked_indent()
    mocker.spy(w.context, 'advance')
    result = w()

    assert result[0] == instance
    assert result[1].token_type == expected
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
    assert w.context.advance.call_count == len(test_input)
