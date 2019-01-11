#!/usr/bin/env python3

import pytest


@pytest.fixture
def parser():
    from lark import Lark
    from pylang.parser import GRAMMAR

    return Lark(GRAMMAR, start='unary_expr')


@pytest.mark.parametrize('test_input,token_name,expected', [
    ('!true', 'NOT_OP', '!'),
    ('-1', 'NEGATIVE_OP', '-')
])
def test_unary_expr(test_input, token_name, expected, parser):
    unary_expr_rule = parser.parse(test_input)
    assert 'unary_expr' == unary_expr_rule.data
    assert 2 == len(unary_expr_rule.children)

    not_token = unary_expr_rule.children[0]
    assert token_name == not_token.type
    assert expected == not_token.value
