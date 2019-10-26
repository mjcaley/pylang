#!/usr/bin/env python3

from functools import singledispatch

from .parse_tree import *


# https://en.wikipedia.org/wiki/Box-drawing_character
# \u2500 \u256c

# Tree drawing design
# objects need to mark where a trunk should be written
# e.g. BinaryExpression needs a trunk to display connections between left, operator and right
# might need to tell how many children it has?
# sequence types might be a problem marking the final element, might need to use the length
#
# Block
#  ├──BinaryExpression
#  │   ├──Left
#  │   │   └──Integer: 4
#  │   ├──Operator: Add
#  │   └──Right
#  │       └──Integer: 5
#  └──Last expression
#


class IndentLevel:
    def __init__(self, width=4):
        self.width = width
        self.current = 0

    def __str__(self):
        return ' ' * self.current

    def push(self):
        self.current += self.width

    def pop(self):
        self.current = min(self.current - self.width, 0)


def printer(func):
    def inner(self, *args, **kwargs):
        self.print_rule(func.__name__)
        self.level.push()
        result = func(self, *args, **kwargs)
        self.level.pop()

        return result
    return inner


class ParseTreePrinter:
    def __init__(self, tree):
        self.tree = tree
        self.level = IndentLevel()

    def print_line(self, class_name, value):
        print(self.level, class_name, value)

    def print_token(self, rule_name, token):
        print(self.level, rule_name, ' ', token.token_type, ' ', token.value, sep='')

    def print_rule(self, name):
        print(self.level, name, sep='')

    def print_tree(self):
        self.block(self.tree)

    @printer
    def block(self, value):
        for statement in value:
            self.statement(statement)

    @printer
    def statement(self, value):
        self.expression(value)

    @printer
    def expression(self, value):
        if isinstance(value, BinaryExpression):
            self.binary_expression(value)
        elif type(value) is UnaryExpression:
            self.unary_expression(value)
        elif type(value) is Function:
            self.function(value)
        else:
            self.atom(value)

    @printer
    def binary_expression(self, value):
        self.expression(value.left)
        self.print_token('Operator', value.operator)
        self.expression(value.right)

    @printer
    def unary_expression(self, value):
        self.print_token('Operator', value.operator)

    @printer
    def function(self, value):
        self.print_token('FunctionDecl', value.definition.name)

    @printer
    def atom(self, value):
        if type(value) is Float:
            self.print_token('Float', value.value)
        elif type(value) is Integer:
            self.print_token('Integer', value.value)
        elif type(value) is Boolean:
            self.print_token('Boolean', value.value)
        elif type(value) is Identifier:
            self.print_token('Identifier', value.value)
        elif type(value) is String:
            self.print_token('String', value.value)
        else:
            self.expression(value)
