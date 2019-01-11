#!/usr/bin/env python3

import pytest


@pytest.fixture
def parser():
    from lark import Lark
    from pylang.parser import GRAMMAR

    return Lark(GRAMMAR, start='_atom')


@pytest.mark.parametrize('test_input,rule_name,token_name,expected', [
    ('true', 'true', 'TRUE', 'true'),
    ('false', 'false', 'FALSE', 'false'),

    ('4', 'integer', 'INT', '4'),
    ('42', 'integer', 'INT', '42'),
    ('424242', 'integer', 'INT', '424242'),

    ('4.', 'float', 'DECIMAL', '4.'),
    ('42.', 'float', 'DECIMAL', '42.'),
    ('4.2', 'float', 'DECIMAL', '4.2'),
    ('42.2', 'float', 'DECIMAL', '42.2'),
    ('42.42', 'float', 'DECIMAL', '42.42'),

    ('(4)', 'integer', 'INT', '4'),
    ('(4.2)', 'float', 'DECIMAL', '4.2'),
    ('(true)', 'true', 'TRUE', 'true'),
    ('(false)', 'false', 'FALSE', 'false'),
])
def test_atom(test_input, rule_name, token_name, expected, parser):
    atom_rule = parser.parse(test_input)
    assert '_atom' == atom_rule.data
    assert 1 == len(atom_rule.children)

    false_rule = atom_rule.children[0]
    assert rule_name == false_rule.data
    assert 1 == len(false_rule.children)

    false_token = false_rule.children[0]
    assert token_name == false_token.type
    assert expected == false_token.value
