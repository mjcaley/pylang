#!/usr/bin/env python3

from lark import Visitor


class Interpreter(Visitor):
    def __init__(self):
        pass

    def start(self, tree):
        pass

    def statement(self, tree):
        pass

    def binary_expr(self, tree):
        pass

    def unary_expr(self, tree):
        pass

    def atom(self, tree):
        pass

    def integer(self, tree):
        pass

    def float(self, tree):
        pass

    def bool(self, tree):
        pass

    def identifier(self, tree):
        pass
