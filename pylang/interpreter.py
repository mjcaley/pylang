#!/usr/bin/env python3

from enum import Enum

from lark import Token, Transformer, v_args

from .parser import Operator


class OperatorToEnum(Transformer):
    def sum_expr(self, tree):
        if len(tree) >= 2:
            if tree[1].type == 'ADD_OP':
                tree[1] = Operator.Add
            elif tree[1].type == 'SUB_OP':
                tree[1] = Operator.Subtract
        return tree

    def mul_expr(self, tree):
        if len(tree) >= 2:
            if tree[1].type == 'MUL_OP':
                tree[1] = Operator.Multiply
            elif tree[1].type == 'DIV_OP':
                tree[1] = Operator.Divide
        return tree


@v_args(inline=True)
class ToLiteral(Transformer):
    def integer(self, token):
        return Token.new_borrow_pos(token.type, int(token), token)

    def float(self, token):
        return Token.new_borrow_pos(token.type, float(token), token)


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
