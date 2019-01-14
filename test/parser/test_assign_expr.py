#!/usr/bin/env python3

import pytest


@pytest.mark.parametrize('test_input,token_name', [
    ('a=42', 'ASSIGN_OP'),
    ('abc=42', 'ASSIGN_OP'),
    ('abc123=42', 'ASSIGN_OP'),
    ('_abc=42', 'ASSIGN_OP'),
    ('_123=42', 'ASSIGN_OP'),
])
def test_assign_expr_binary(test_input, token_name, parser):
    assign_rule = parser('_assign_expr').parse(test_input)
    assert 3 == len(assign_rule.children)
    assert token_name == assign_rule.children[1].type
