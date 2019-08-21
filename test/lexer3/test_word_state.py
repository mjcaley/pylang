#!/usr/bin/env python3

import pytest

from pylang.lexer3.states import Word
from pylang.lexer3.token import TokenType


def test_returns_identifier(context_at_current, mocker):
    w = Word(context_at_current('a'))
    mocked_indent = mocker.patch('pylang.lexer3.states.Indent')
    instance = mocked_indent()
    result = w()

    assert result[0] == instance
    assert result[1].token_type == TokenType.Identifier
    assert result[1].position.index == 0
    assert result[1].position.line == 1
    assert result[1].position.column == 1
