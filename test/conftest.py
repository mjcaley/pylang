#!/usr/bin/env python3

import pytest


@pytest.fixture
def parser():
    from lark import Lark
    from pylang.parser import grammar

    def inner(start_rule=None):
        if start_rule:
            return Lark(grammar(), parser='lalr', start=start_rule)
        else:
            return Lark(grammar(), parser='lalr')

    return inner


@pytest.fixture
def context():
    from pylang.lexer3.context import Context
    from pylang.lexer3.stream import Stream

    def inner(data):
        return Context(Stream(data))

    return inner


@pytest.fixture
def context_at_next(context):
    def inner(data):
        ctx = context(data)
        ctx.advance()

        return ctx

    return inner


@pytest.fixture
def context_at_current(context):
    def inner(data):
        ctx = context(data)
        ctx.advance()
        ctx.advance()

        return ctx

    return inner
