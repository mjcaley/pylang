#!/usr/bin/env python3


class Start:
    def __init__(self, *statements):
        self.statements = statements


class Statement:
    def __init__(self, expression):
        self.expression = expression


class SumExpression:
    def __init__(self, left, right):
        self.left, self.right = left, right


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
        self.print_node(tree, tree.left, tree.right)
