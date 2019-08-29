#!/usr/bin/env python3

import pytest


@pytest.fixture
def tokens_from_types():
    from pylang.lexer.stream import Position
    from pylang.lexer.token import Token

    def inner(*token_types):
        return [Token(token_type, Position(0, 1, 1)) for token_type in token_types]

    return inner
