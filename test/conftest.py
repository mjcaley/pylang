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
def lexer():
    from pylang.lexer3 import Lexer

    def inner(state_name, data, advance_by=1):
        lexer = Lexer(data)
        for _ in range(advance_by):
            lexer.advance()
        lexer.transition(getattr(lexer, state_name))

        return lexer

    return inner
