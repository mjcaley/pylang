#!/usr/bin/env python3

from .interpreter_ast import Literal, BinaryExpression, UnaryExpression


class Interpreter:
    def run(self, statements):
        return [self.statement(statement) for statement in statements]

    def statement(self, statement):
        return self.expression(statement.expression)

    def expression(self, expression):
        if isinstance(expression, Literal):
            return expression.value
        elif isinstance(expression, BinaryExpression):
            return expression.operation(
                self.expression(expression.left),
                self.expression(expression.right)
            )
        elif isinstance(expression, UnaryExpression):
            return expression.operation(
                self.expression(expression.value)
            )
