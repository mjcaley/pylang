#!/usr/bin/env python3

from typing import List


class Start:
    def __init__(self, *functions):
        self.functions: List[Function] = functions


class Block:
    def __init__(self, *statements):
        self.statements: List[Statement] = statements


class Statement:
    def __init__(self, expression):
        self.expression: Expression = expression


class Expression:
    pass


class BinaryExpression(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class SumExpression(BinaryExpression):
    def __init__(self, left, operator, right):
        super().__init__(left, operator, right)


class ProductExpression(BinaryExpression):
    def __init__(self, left, operator, right):
        super().__init__(left, operator, right)


class UnaryExpression(Expression):
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression


class Function:
    def __init__(self, name, parameters, block):
        self.name = name
        self.parameters = parameters
        self.block = block


class Boolean:
    def __init__(self, value):
        self.value = value
