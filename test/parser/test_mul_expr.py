#!/usr/bin/env python3

import pytest


@pytest.fixture
def parser():
    from lark import Lark
    from pylang.parser import GRAMMAR

    return Lark(GRAMMAR, start='_mul_expr')


@pytest.mark.parametrize('test_input,token_name,expected', [
    ('4*2', 'MUL_OP', '*'),
    ('4/2', 'DIV_OP', '/'),
])
def test_mul_expr_binary(test_input, token_name, expected, parser):
    mul_expr_rule = parser.parse(test_input)
    assert '_mul_expr' == mul_expr_rule.data
    assert 3 == len(mul_expr_rule.children)

    mul_token = mul_expr_rule.children[1]
    assert token_name == mul_token.type
    assert expected == mul_token.value


def test_mul_expr_atom(parser):
    mul_expr_rule = parser.parse('true')
    assert '_mul_expr' == mul_expr_rule.data
    assert 1 == len(mul_expr_rule.children)

    atom_token = mul_expr_rule.children[0]
    assert 'true' == atom_token.data
