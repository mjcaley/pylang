#!/usr/bin/env python3

import pytest


@pytest.mark.parametrize('test_input,rule_name,token_name,expected', [
    ('true', 'bool', 'TRUE', 'true'),
    ('false', 'bool', 'FALSE', 'false'),

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
    ('(true)', 'bool', 'TRUE', 'true'),
    ('(false)', 'bool', 'FALSE', 'false'),
])
def test_atom(test_input, rule_name, token_name, expected, parser):
    atom_rule = parser('atom').parse(test_input)
    assert rule_name == atom_rule.data
    assert 1 == len(atom_rule.children)

    atom_token = atom_rule.children[0]
    assert token_name == atom_token.type
    assert expected == atom_token.value



# @pytest.mark.parametrize('test_input,rule_name,token_name,expected', [
#     ('(4)', 'integer', 'INT', '4'),
#     ('(4.2)', 'float', 'DECIMAL', '4.2'),
#     ('(true)', 'bool', 'TRUE', 'true'),
#     ('(false)', 'bool', 'FALSE', 'false'),
# ])
# def test_atom(test_input, rule_name, token_name, expected, parser):
#     atom_rule = parser('atom').parse(test_input)
#     assert 'atom' == atom_rule.data
#     assert 1 == len(atom_rule.children)
#
#     expr_rule = atom_rule.children[0]
#     assert rule_name == expr_rule.data
#     assert 1 == len(expr_rule.children)
#
#     atom_token = expr_rule.children[0]
#     assert token_name == atom_token.type
#     assert expected == atom_token.value

