#!/usr/bin/env python3

from lark import Lark, Transformer, Visitor

from .pylang_ast import *


PYLANG_GRAMMAR = '''
    start: statement+
    
    statement: sum_expr EOL
    
    sum_expr: NUMBER ADD_OP NUMBER
    
    EOL: ";"
    
    ADD_OP: "+"
    SUB_OP: "-"
    MUL_OP: "*"
    DIV_OP: "/"
    PAREN_L: "("
    PAREN_R: ")"
    
    %import common.WORD
    %import common.NUMBER
    %ignore " "
'''

parser = Lark(PYLANG_GRAMMAR)
# program = "42 + 24;"
# tree = parser.parse(program)
# print(tree.pretty())


class MyVisitor(Visitor):
    def __init__(self):
        self.ast = None
    
    def start(self, tree):
        print("start rule")
        self.ast = Start(tree.children)

    def statement(self, tree):
        print("statement rule")
        self.ast = Statement(tree.children)

    def sum_expr(self, tree):
        print("sum_expr rule")
        self.ast = SumExpression(tree.children[0], tree.children[2])


class ToAST(Transformer):
    def start(self, tree):
        print("start rule")
        return Start(*tree)

    def statement(self, tree):
        print("statement rule")
        return Statement(tree[0])

    def sum_expr(self, tree):
        print("sum_expr rule")
        return SumExpression(tree[0], tree[2])
