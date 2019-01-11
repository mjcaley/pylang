#!/usr/bin/env python3

import pytest


@pytest.fixture
def unary_expr_parser():
    from lark import Lark
    from pylang import parser

    return Lark(parser.GRAMMAR, start='unary_expr')


@pytest.mark.parametrize('test_input,rule_name,token_name,expected', [
    ('!true', 'unary_expr', 'NOT_OP', '!'),
    ('-1', 'unary_expr', 'NEGATIVE_OP', '-')
])
def test_unary_expr(test_input, rule_name, token_name, expected, unary_expr_parser):
    unary_expr_rule = unary_expr_parser.parse(test_input)
    assert rule_name == unary_expr_rule.data
    assert 2 == len(unary_expr_rule.children)

    not_token = unary_expr_rule.children[0]
    assert token_name == not_token.type
    assert expected == not_token.value
