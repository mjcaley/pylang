#!/usr/bin/env python3

from pylang.lexer3 import TokenType


def test_emit_indent_token(lexer):
    l = lexer('start', '', 0)
    result = next(l)

    assert result.token_type == TokenType.Indent


def test_transition_to_operators(lexer):
    l = lexer('start', '', 0)
    old_state = l.state
    next(l)

    assert l.state != old_state
