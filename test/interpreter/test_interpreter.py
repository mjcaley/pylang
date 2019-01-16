#!/usr/bin/env python3

import pytest

from pylang.interpreter import Interpreter

from lark import Tree, Token


@pytest.fixture
def interpreter():
    return Interpreter()


def test_initialized(interpreter):
    assert hasattr(interpreter, 'stack')
    assert hasattr(interpreter, 'map')


def test_reset(interpreter):
    interpreter.stack.append('value')
    interpreter.map['mock'] = 'value'

    interpreter.reset()

    assert [] == interpreter.stack
    assert {} == interpreter.map


@pytest.mark.parametrize('start_rule,test_input,expected', [
    ('identifier', 'id', 'id'),
    ('integer', '42', 42),
    ('bool', 'true', True),
    ('bool', 'false', False),
])
def test_literal_push(start_rule, test_input, expected, parser, interpreter):
    p = parser(start_rule)
    interpreter.visit(p.parse(test_input))

    assert expected == interpreter.stack[0]


def test_float_push(interpreter, parser):
    p = parser('float')
    interpreter.visit(p.parse('4.2'))

    assert pytest.approx(4.2, interpreter.stack[0])


def test_bool_raises(interpreter):
    tree = Tree('tree_rule', [Token('TOKEN', 'error')])

    with pytest.raises(TypeError):
        interpreter.bool(tree)


@pytest.mark.parametrize('test_input,expected', [
    ('!true', False),
    ('-42', -42),
])
def test_unary_expr_pushes(test_input, expected, interpreter, parser):
    p = parser('unary_expr')
    interpreter.visit(p.parse(test_input))

    assert expected == interpreter.stack[0]


def test_unary_expr_raises(interpreter):
    tree = Tree('unary_expr', [Token('TOKEN', 'error')])

    with pytest.raises(SyntaxError):
        interpreter.visit(tree)


@pytest.mark.parametrize('test_input,expected', [
    ('4+2', 6),
    ('4-2', 2),
    ('4*2', 8),
    ('4/2', 2),
    ('a=42', 42),
])
def test_binary_expr_pushes(test_input, expected, interpreter, parser):
    p = parser('binary_expr')
    interpreter.visit(p.parse(test_input))

    assert expected == interpreter.stack[0]


def test_binary_expr_assignment(interpreter):
    left = Tree('integer', [Token('INT', '4')])
    right = Tree('integer', [Token('INT', '2')])
    tree = Tree('binary_expr', [left, Token('TOKEN', 'error'), right])

    with pytest.raises(SyntaxError):
        interpreter.visit(tree)


def test_statement(interpreter, parser):
    p = parser()
    interpreter.visit(p.parse('a=42;'))

    assert 0 == len(interpreter.stack)
    assert 'a' in interpreter.map.keys()
    assert 42 == interpreter.map['a']
