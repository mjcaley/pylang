#!/usr/bin/env python3

import pytest


@pytest.mark.parametrize('test_input,token_name,expected', [
    ('!true', 'NOT_OP', '!'),
    ('-1', 'NEGATIVE_OP', '-')
])
def test_unary_expr(test_input, token_name, expected, parser):
    unary_expr_rule = parser('unary_expr').parse(test_input)
    assert 'unary_expr' == unary_expr_rule.data
    assert 2 == len(unary_expr_rule.children)

    not_token = unary_expr_rule.children[0]
    assert token_name == not_token.type
    assert expected == not_token.value


@pytest.mark.parametrize('test_input,rule_name', [
    ('true', 'bool'),
    ('false', 'bool'),
    ('42', 'integer'),
    ('4.2', 'float'),
    ('(4+2)', 'binary_expr'),
])
def test_unary_expr_atom(test_input, rule_name, parser):
    unary_expr_rule = parser('unary_expr').parse(test_input)
    assert rule_name == unary_expr_rule.data
