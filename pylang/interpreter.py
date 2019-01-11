#!/usr/bin/env python3

from lark import Transformer

from .interpreter_ast import (Literal, BinaryExpression, UnaryExpression,

                              Integer, Float, Boolean,

                              AddExpression, SubtractExpression,
                              MultiplyExpression, DivideExpression,

                              NotExpression, NegativeExpression,

                              Statement)


class Interpreter:
    def __init__(self):
        self.results = []

    def run(self, tree):
        for statement in tree:
            self.results.append(self.statement(statement))

    def statement(self, statement):
        return self.expression(statement.expression)

    def expression(self, expression):
        if isinstance(expression, Literal):
            return expression.value
        elif isinstance(expression, BinaryExpression):
            expression.left = self.expression(expression.left)
            expression.right = self.expression(expression.right)
            return expression()
        elif isinstance(expression, UnaryExpression):
            expression.value = self.expression(expression.value)
            return expression()
