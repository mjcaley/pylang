#!/usr/bin/env python3

import pytest


@pytest.fixture
def parser():
    from lark import Lark
    from pylang.parser import GRAMMAR

    return Lark(GRAMMAR, start='statement')


@pytest.mark.parametrize('test_input,rule_name', [
    ('4+2;', 'binary_expr'),
    ('4*2;', 'binary_expr'),
    ('-4;', 'unary_expr'),
    ('4;', 'integer'),
])
def test_statement(test_input, rule_name, parser):
    statement_rule = parser.parse(test_input)
    assert 1 == len(statement_rule.children)
    assert rule_name == statement_rule.children[0].data


def test_statement_missing_semicolon(parser):
    from lark.exceptions import ParseError

    with pytest.raises(ParseError):
        parser.parse('4+2')
