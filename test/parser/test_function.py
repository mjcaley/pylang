#!/usr/bin/env python3

import pytest


@pytest.mark.parametrize('test_input,parameter_tokens', [
    ('', []),
    ('one', ['one']),
    ('one, two, three, four', ['one', 'two', 'three', 'four'])
])
def test_parameter_list(test_input, parameter_tokens, parser):
    p = parser('parameter_list')
    tree = p.parse(test_input)

    assert len(parameter_tokens) == len(tree.children)
    for token_name, token in zip(parameter_tokens, tree.children):
        assert token_name == token.children[0]


@pytest.mark.parametrize('test_input,function_name', [
    ('func main()', 'main'),
    ('func length(container)', 'length'),
    ('func add(first, second)', 'add'),
])
def test_function_decl(test_input, function_name, parser):
    p = parser('_function_decl')
    tree = p.parse(test_input)

    assert function_name == tree.children[0].children[0]
    assert tree.children[1].data == 'parameter_list'


@pytest.mark.parametrize('test_input', [
    'func main() = {}',
    'func length(container) = {}',
    'func sum(first, second) = { first + second; }'
])
def test_function(test_input, parser):
    p = parser('function')
    tree = p.parse(test_input)

    assert 'identifier' == tree.children[0].data
    assert 'parameter_list' == tree.children[1].data
    assert 'ASSIGN_OP' == tree.children[2].type
    for rule in tree.children[3:]:
        assert 'statement' == rule.data
