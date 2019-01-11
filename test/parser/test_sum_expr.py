#!/usr/bin/env python3

import pytest


@pytest.fixture
def parser():
    from lark import Lark
    from pylang.parser import GRAMMAR

    return Lark(GRAMMAR, start='_sum_expr')


@pytest.mark.parametrize('test_input,token_name,expected', [
    ('4+2', 'ADD_OP', '+'),
    ('4-2', 'SUB_OP', '-'),
])
def test_sum_expr_binary(test_input, token_name, expected, parser):
    sum_expr_rule = parser.parse(test_input)
    assert '_sum_expr' == sum_expr_rule.data
    assert 3 == len(sum_expr_rule.children)

    sum_token = sum_expr_rule.children[1]
    assert token_name == sum_token.type
    assert expected == sum_token.value


@pytest.mark.parametrize('test_input,rule_name', [
    ('true', 'true'),
    ('false', 'false'),
    ('42', 'integer'),
    ('4.2', 'float'),
    ('(4+2)', 'binary_expr'),
    ('!true', 'unary_expr'),
])
def test_sum_expr_atom(test_input, rule_name, parser):
    sum_expr_rule = parser.parse(test_input)
    assert '_sum_expr' == sum_expr_rule.data
    assert 1 == len(sum_expr_rule.children)

    atom_rule = sum_expr_rule.children[0]
    assert rule_name == atom_rule.data


@pytest.mark.parametrize('test_input,token_name', [
    ('4*2', 'MUL_OP'),
    ('4/2', 'DIV_OP'),
])
def test_sum_expr_product(test_input, token_name, parser):
    sum_expr_rule = parser.parse(test_input)
    assert '_sum_expr' == sum_expr_rule.data
    assert 3 == len(sum_expr_rule.children)
    assert token_name == sum_expr_rule.children[1].type
