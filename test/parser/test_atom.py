#!/usr/bin/env python3

import pytest

from lark import Lark


@pytest.fixture
def atom_parser():
    from pylang import parser

    return Lark(parser.GRAMMAR, start='atom')


@pytest.mark.parametrize('test_input', [
    '4',
    '42',
    '424242'
])
def test_atom_integer_input(atom_parser, test_input):
    tree = atom_parser.parse(test_input)

    assert tree.data == 'integer'
    assert tree.children[0].type == 'INT'
    assert tree.children[0].value == test_input


@pytest.mark.parametrize('test_input', [
    '4.',
    '42.',
    '4.2',
    '42.2',
    '42.42'
])
def test_atom_float_input(atom_parser, test_input):
    tree = atom_parser.parse(test_input)

    assert tree.data == 'float'
    assert tree.children[0].type == 'DECIMAL'
    assert tree.children[0].value == test_input


def test_atom_boolean_true(atom_parser):
    tree = atom_parser.parse('true')

    assert tree.data == 'true'
    assert tree.children[0].type == 'TRUE'
    assert tree.children[0].value == 'true'


def test_atom_boolean_false(atom_parser):
    tree = atom_parser.parse('false')

    assert tree.data == 'false'
    assert tree.children[0].type == 'FALSE'
    assert tree.children[0].value == 'false'
