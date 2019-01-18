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
