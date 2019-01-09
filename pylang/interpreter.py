#!/usr/bin/env python3

from lark import Token, Transformer, Tree, v_args

from .parser import Operator


class OperatorToEnum(Transformer):
    def binary_expr(self, tree):
        if len(tree) > 1:
            tree[1] = Token.new_borrow_pos(tree[1].type, Operator(tree[1]), tree[1])


class ToLiteral(Transformer):
    def integer(self, tokens):
        return Tree('integer', int(tokens[0]))

    def float(self, tokens):
        return Tree('float', float(tokens[0]))

    def true(self, _):
        return Tree('true', True)

    def false(self, _):
        return Tree('false', False)


class TreeWalker(Transformer):
    def __init__(self):
        self.results = []

    # start
    # statement
    # ?expr: sum_expr
    # ?sum_expr
    # ?mul_expr
    def mul_expr(self, tree):
        if tree.data == 'NUMBER':
            return tree.children[0]
        elif tree.children[1].data == 'MUL_OP':
            pass


    def atom(self, tree):
        if tree.data == 'NUMBER':
            return tree.children[0]
        else:
            return tree
