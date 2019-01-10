#!/usr/bin/env python3

from enum import Enum
from lark import Transformer, Token


class Operator(Enum):
    Add = '+'
    Subtract = '-'
    Multiply = '*'
    Divide = '/'

    Assign = '='


class Start:
    def __init__(self, *statements):
        self.statements = statements


class Statement:
    def __init__(self, expression):
        self.expression = expression


class Expression:
    def __init__(self, expression=None, literal=None):
        if expression:
            self.expression = expression
        elif literal:
            self.literal = literal


class BinaryExpression:
    def __init__(self, left, right, operator):
        self.left, self.right, self.operator = left, right, operator


class Literal:
    def __init__(self, value):
        self.value = value


class ToAST(Transformer):
    def start(self, tree):
        print("start rule")
        return Start(*tree)

    def statement(self, tree):
        print("statement rule")
        return Statement(tree[0])

    def expr(self, tree):
        return Expression(tree)

    def sum_expr(self, tree):
        print("sum_expr rule")
        return BinaryExpression(tree[0], Operator(tree[1]), [2])

    def mul_expr(self, tree):
        print("mul_expr rule")
        return BinaryExpression(tree[0], Operator(tree[1]), [2])

    def atom(self, tree):
        if type(tree[0]) == Token and tree[0].type == 'NUMBER':
            return Literal(tree[0])
        else:
            return tree


def methoddispatch(func):
    registry = {}

    def dispatch(cls):
        try:
            return registry[cls]
        except KeyError:
            return registry[object]

    def register(cls):
        from typing import get_type_hints
        name, type_info = next(iter(get_type_hints(cls).items()))
        registry[type_info] = cls

    def wrapper(self, *args, **kwargs):
        if not args:
            raise TypeError('Requires at least one parameter')
        return dispatch(args[0].__class__,)(self, *args, **kwargs)

    registry[object] = func
    wrapper.registry = registry
    wrapper.register = register
    wrapper.dispatch = dispatch

    return wrapper


# Decorate method to setup registry dict and have default method invocation
# adds 'register' function to the method

class ASTPrinter2:
    def __init__(self):
        self.indent = 0

    def increment_indent(self):
        self.indent += 4

    def decrement_indent(self):
        self.indent -= 4

    def print_node(self, tree, *value):
        print(' ' * self.indent, f'[{tree.__class__.__name__}]', ':', *value)

    def start(self, tree):
        self.indent = 0
        self.start(tree)
        self.indent = 0

    @methoddispatch
    def visit(self, arg):
        pass

    @visit.register
    def _(self, arg: BinaryExpression):
        left = self.visit(arg.left)
        right = self.visit(arg.right)
        if arg.operator == Operator.Assign:
            pass
        elif arg.operator == Operator.Add:
            pass
        elif arg.operator == Operator.Subtract:
            pass
        elif arg.operator == Operator.Multiply:
            pass
        elif arg.operator == Operator.Divide:
            pass

class ASTPrinter:
    def __init__(self):
        self.indent = 0

    def increment_indent(self):
        self.indent += 4

    def decrement_indent(self):
        self.indent -= 4

    def print_node(self, tree, *value):
        print(' ' * self.indent, f'[{tree.__class__.__name__}]', ':', *value)

    def visit(self, tree):
        self.indent = 0
        self.start(tree)
        self.indent = 0

    def start(self, tree):
        self.print_node(tree)
        self.increment_indent()
        for statement in tree.statements:
            self.statement(statement)
        self.decrement_indent()

    def statement(self, tree):
        self.print_node(tree)
        self.increment_indent()
        self.expression(tree.expression)

    def expression(self, tree):
        if hasattr(tree, 'expression'):
            if isinstance(tree.expression, BinaryExpression):
                self.binary_expression(tree.expression)
        elif hasattr(tree, 'literal'):
            self.literal(tree.literal)

    def binary_expression(self, tree):
        self.print_node(tree, tree.left, tree.right)
