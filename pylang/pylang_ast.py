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
