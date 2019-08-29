#!/usr/bin/env python3

import pytest


@pytest.fixture
def context():
    from pylang.lexer.context import Context
    from pylang.lexer.stream import Stream

    def inner(data):
        return Context(Stream(data))

    return inner


@pytest.fixture
def context_at_position(context):
    def inner(data, position):
        ctx = context(data)
        for _ in range(position):
            ctx.advance()

        return ctx

    return inner


@pytest.fixture
def context_at_next(context_at_position):
    def inner(data):
        ctx = context_at_position(data, 1)

        return ctx

    return inner


@pytest.fixture
def context_at_current(context_at_position):
    def inner(data):
        ctx = context_at_position(data, 2)

        return ctx

    return inner