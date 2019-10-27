#!/usr/bin/env python3

from functools import singledispatchmethod
from typing import Collection, List

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
    def __init__(
            self,
            template=' {}{}',
            trunk='\u2502',
            child='\u2514',
            children='\u251c',
            horizontal_line='\u2500',
            width=3
    ):
        self.template = template
        self.trunk = trunk
        self.child = child
        self.children = children
        self.horizontal_line = horizontal_line
        self.width = width
        self.stack = []

    def __str__(self):
        output = []
        output += [self.trunk_template(num) for num in self.stack[:-1]]
        output += [self.edge_template(num) for num in self.stack[-1:]]

        return ''.join(output)

    def edge_template(self, num_children):
        width = self.width - 1

        if num_children == 0:
            return self.template.format(' ', ' ' * width)
        elif num_children == 1:
            return self.template.format(self.child, self.horizontal_line * width)
        else:
            return self.template.format(self.children, self.horizontal_line * width)

    def trunk_template(self, num_children):
        width = self.width - 1

        if num_children == 0:
            return self.template.format(' ', ' ' * width)
        else:
            return self.template.format(self.trunk, ' ' * width)

    def push(self, num_children):
        self.stack.append(num_children)

    def pop(self):
        self.stack.pop()

    def decrement(self):
        if self.stack[-1] > 0:
            self.stack[-1] -= 1


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

    def print_tree(self):
        self.level = IndentLevel()
        string_tree = self.visit(self.tree)
        self.level.push(0)
        self.print_node(string_tree)

    def print_node(self, node):
        if isinstance(node[1], list):
            print(str(self.level), node[0], sep='')
            self.level.decrement()
            self.level.push(len(node[1]))
            for child in node[1]:
                self.print_node(child)
            self.level.pop()
        else:
            print(str(self.level), node[0], ': ', node[1], sep='')
            self.level.decrement()

    @singledispatchmethod
    def visit(self, value):
        raise NotImplementedError('Unknown type')

    @visit.register
    def _(self, token: Token):
        return token.token_type.name, token.value

    @visit.register
    def _(self, value: Block):
        statements = [self.visit(statement) for statement in value.statements]
        return 'Block', statements

    @visit.register
    def _(self, value: Identifier):
        return 'Identifier', [self.visit(value.value)]

    @visit.register
    def _(self, value: Boolean):
        return 'Boolean', [self.visit(value.value)]

    @visit.register
    def _(self, value: Integer):
        return 'Integer', [self.visit(value.value)]

    @visit.register
    def _(self, value: Float):
        return 'Float', [self.visit(value.value)]

    @visit.register
    def _(self, value: String):
        return 'String', [self.visit(value.value)]

    @visit.register
    def _(self, value: BinaryExpression):
        return 'BinaryExpression', [self.visit(value.left), self.visit(value.operator), self.visit(value.right)]

    @visit.register
    def _(self, value: AssignmentExpression):
        return 'AssignmentExpression', [self.visit(value.left), self.visit(value.operator), self.visit(value.right)]

    @visit.register
    def _(self, value: SumExpression):
        return 'SumExpression', [self.visit(value.left), self.visit(value.operator), self.visit(value.right)]

    @visit.register
    def _(self, value: ProductExpression):
        return 'ProductExpression', [self.visit(value.left), self.visit(value.operator), self.visit(value.right)]

    @visit.register
    def _(self, value: UnaryExpression):
        return 'UnaryExpression', [self.visit(value.operator), self.visit(value.expression)]

    @visit.register
    def _(self, value: FunctionDecl):
        return 'FunctionDecl', [self.visit(value.name), self.visit(value.parameters), self.visit(value.return_type)]

    @visit.register
    def _(self, value: Function):
        return 'Function', [self.visit(value.definition), self.visit(value.block)]

    @visit.register
    def _(self, value: Branch):
        return 'Branch', [self.visit(value.condition), self.visit(value.then_branch), self.visit(value.else_branch)]
