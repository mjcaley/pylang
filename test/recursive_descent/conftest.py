#!/usr/bin/env python3

import pytest


@pytest.fixture
def tokens_from_types(mocker):
    from pylang.lexer.token import Token

    def inner(*token_types):
        return [Token(token_type, mocker.stub()) for token_type in token_types]

    return inner
