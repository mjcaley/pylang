#!/usr/bin/env python3

from functools import singledispatchmethod

from .parse_tree import Block, Identifier, Boolean, Integer, Float, String, BinaryExpression, AssignmentExpression, \
    SumExpression, ProductExpression, UnaryExpression, FunctionDecl, Function, Branch
from .lexer.token import Token


class Visitor:
    def __init__(self, tree):
        self.tree = tree

    @singledispatchmethod
    def visit(self, value):
        raise NotImplementedError('Unknown type')

    @visit.register
    def _(self, value: Token):
        pass

    @visit.register
    def _(self, value: Block):
        for statement in value.statements:
            self.visit(statement)

    @visit.register
    def _(self, value: Identifier):
        self.visit(value.value)

    @visit.register
    def _(self, value: Boolean):
        self.visit(value.value)

    @visit.register
    def _(self, value: Integer):
        self.visit(value.value)

    @visit.register
    def _(self, value: Float):
        self.visit(value.value)

    @visit.register
    def _(self, value: String):
        self.visit(value.value)

    @visit.register
    def _(self, value: BinaryExpression):
        self.visit(value.left)
        self.visit(value.operator)
        self.visit(value.right)

    @visit.register
    def _(self, value: AssignmentExpression):
        self.visit(value.left)
        self.visit(value.operator)
        self.visit(value.right)

    @visit.register
    def _(self, value: SumExpression):
        self.visit(value.left)
        self.visit(value.operator)
        self.visit(value.right)

    @visit.register
    def _(self, value: ProductExpression):
        self.visit(value.left)
        self.visit(value.operator)
        self.visit(value.right)

    @visit.register
    def _(self, value: UnaryExpression):
        self.visit(value.operator)
        self.visit(value.expression)

    @visit.register
    def _(self, value: FunctionDecl):
        self.visit(value.name)
        self.visit(value.parameters)
        self.visit(value.return_type)

    @visit.register
    def _(self, value: Function):
        self.visit(value.definition)
        self.visit(value.block)

    @visit.register
    def _(self, value: Branch):
        self.visit(value.condition)
        self.visit(value.then_branch)
        self.visit(value.else_branch)
