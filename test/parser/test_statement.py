#!/usr/bin/env python3

import pytest


@pytest.mark.parametrize('test_input,rule_name', [
    ('4+2;', 'binary_expr'),
    ('4*2;', 'binary_expr'),
    ('-4;', 'unary_expr'),
    ('4;', 'integer'),
])
def test_statement(test_input, rule_name, parser):
    statement_rule = parser('statement').parse(test_input)
    assert 1 == len(statement_rule.children)
    assert rule_name == statement_rule.children[0].data


def test_statement_missing_semicolon(parser):
    from lark.exceptions import ParseError

    with pytest.raises(ParseError):
        parser('statement').parse('4+2')
