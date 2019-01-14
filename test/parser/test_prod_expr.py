#!/usr/bin/env python3

import pytest


@pytest.mark.parametrize('test_input,token_name,expected', [
    ('4*2', 'MUL_OP', '*'),
    ('4/2', 'DIV_OP', '/'),
])
def test_prod_expr_binary(test_input, token_name, expected, parser):
    prod_expr_rule = parser('_prod_expr').parse(test_input)
    assert '_prod_expr' == prod_expr_rule.data
    assert 3 == len(prod_expr_rule.children)

    mul_token = prod_expr_rule.children[1]
    assert token_name == mul_token.type
    assert expected == mul_token.value


@pytest.mark.parametrize('test_input,rule_name', [
    ('true', 'bool'),
    ('false', 'bool'),
    ('42', 'integer'),
    ('4.2', 'float'),
    ('(4+2)', 'binary_expr'),
    ('!true', 'unary_expr'),
])
def test_prod_expr_atom(test_input, rule_name, parser):
    prod_expr_rule = parser('_prod_expr').parse(test_input)
    assert '_prod_expr' == prod_expr_rule.data
    assert 1 == len(prod_expr_rule.children)

    atom_rule = prod_expr_rule.children[0]
    assert rule_name == atom_rule.data
