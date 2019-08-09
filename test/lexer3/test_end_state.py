#!/usr/bin/env python3

import pytest

from pylang.lexer3 import TokenType


def test_emit_dedent_token(lexer):
    l = lexer('end', '', 0)
    result = next(l)

    assert result.token_type == TokenType.Dedent


def test_raise_stop_iteration(lexer):
    l = lexer('end', '', 0)
    next(l)

    with pytest.raises(StopIteration):
        next(l)
