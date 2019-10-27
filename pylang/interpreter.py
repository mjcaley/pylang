#!/usr/bin/env python3

import dataclasses
from functools import singledispatchmethod
from typing import List

from .parse_tree import Block, Identifier, Boolean, Integer, Float, String, BinaryExpression, AssignmentExpression, \
    SumExpression, ProductExpression, UnaryExpression, FunctionDecl, Function, Branch
from .lexer.token import Token


class FunctionMap:
    def __init__(self, tree):
        self.functions = {}
        self.tree = tree

    @singledispatchmethod
    def visit(self, value):
        for field in dataclasses.fields(value):
            self.visit(getattr(value, field))

    @visit.register
    def _(self, value: List):
        for item in value:
            self.visit(item)

    @visit.register
    def _(self, value: Token):
        return

    @visit.register
    def _(self, value: Function):
        name = value.definition.name
        self.functions[name] = value
        self.visit(value.definition)
        self.visit(value.block)


class Interpreter:
    def __init__(self, tree):
        self.tree = tree

    @singledispatchmethod
    def visit(self, value):
        raise NotImplementedError('Unknown type')

    @visit.register
    def _(self, value: Token):
        return value.value

    @visit.register
    def _(self, value: Block):
        statements = [self.visit(statement) for statement in value.statements]
        return 'Block', statements

    @visit.register
    def _(self, value: Identifier):
        return 'Identifier', [self.visit(value.value)]

    @visit.register
    def _(self, value: Boolean):
        token_value = self.visit(value.value)
        return True if token_value == 'true' else False

    @visit.register
    def _(self, value: Integer):
        return int(self.visit(value.value))

    @visit.register
    def _(self, value: Float):
        return float(self.visit(value.value))

    @visit.register
    def _(self, value: String):
        return self.visit(value.value)

    @visit.register
    def _(self, value: BinaryExpression):
        return 'BinaryExpression', [self.visit(value.left), self.visit(value.operator), self.visit(value.right)]

    @visit.register
    def _(self, value: AssignmentExpression):
        return 'AssignmentExpression', [self.visit(value.left), self.visit(value.operator), self.visit(value.right)]

    @visit.register
    def _(self, value: SumExpression):
        return 'SumExpression', [self.visit(value.left), self.visit(value.operator), self.visit(value.right)]

    @visit.register
    def _(self, value: ProductExpression):
        return 'ProductExpression', [self.visit(value.left), self.visit(value.operator), self.visit(value.right)]

    @visit.register
    def _(self, value: UnaryExpression):
        return 'UnaryExpression', [self.visit(value.operator), self.visit(value.expression)]

    @visit.register
    def _(self, value: FunctionDecl):
        return 'FunctionDecl', [self.visit(value.name), self.visit(value.parameters), self.visit(value.return_type)]

    @visit.register
    def _(self, value: Function):
        return 'Function', [self.visit(value.definition), self.visit(value.block)]

    @visit.register
    def _(self, value: Branch):
        return 'Branch', [self.visit(value.condition), self.visit(value.then_branch), self.visit(value.else_branch)]


# from lark import Visitor, v_args
#
#
# class MapFunctions(Visitor):
#     def __init__(self):
#         self.function_map = dict()
#
#     @v_args(tree=True)
#     def function(self, tree):
#         self.function_map[self._function_name(tree.children[0])] = tree
#
#     def _function_name(self, function_tree):
#         return str(function_tree.children[0])
#
#
# class Interpreter(Visitor):
#     def __init__(self, function_map, entry='main'):
#         self.entry = entry
#         self.function_map = function_map
#         self.stack = list()
#         self.map = dict()
#
#     def reset(self):
#         self.stack.clear()
#         self.map.clear()
#
#     def run(self):
#         self.visit(self.function_map[self.entry])
#
#     @v_args(tree=True)
#     def start(self, tree):
#         print('start', tree)
#
#     @v_args(tree=True)
#     def statement(self, tree):
#         print('statement', tree)
#         self.stack.pop()
#
#     @v_args(tree=True)
#     def binary_expr(self, tree):
#         print('binary_expr', tree)
#         right = self.stack.pop()
#         left = self.stack.pop()
#         if tree.children[1].type == 'ADD_OP':
#             self.stack.append(left + right)
#         elif tree.children[1].type == 'SUB_OP':
#             self.stack.append(left - right)
#         elif tree.children[1].type == 'MUL_OP':
#             self.stack.append(left * right)
#         elif tree.children[1].type == 'DIV_OP':
#             self.stack.append(left / right)
#         elif tree.children[1].type == 'ASSIGN_OP':
#             self.map[left] = right
#             self.stack.append(self.map[left])
#         else:
#             raise SyntaxError(f'{str(tree.children[1])} is not a supported binary operator')
#
#     @v_args(tree=True)
#     def unary_expr(self, tree):
#         print('unary_expr', tree)
#         if tree.children[0].type == 'NEGATIVE_OP':
#             val = self.stack.pop()
#             val *= -1
#             self.stack.append(val)
#         elif tree.children[0].type == 'NOT_OP':
#             val = self.stack.pop()
#             val = not val
#             self.stack.append(val)
#         else:
#             raise SyntaxError(f'{str(tree.children[0])} is not a supported unary operator')
#
#     def call(self, tree):
#         self.visit(self.function_map[tree.children[0].children[0]])
#
#     @v_args(tree=True)
#     def integer(self, tree):
#         print('integer', tree)
#         value = int(tree.children[0])
#         self.stack.append(value)
#
#     @v_args(tree=True)
#     def float(self, tree):
#         print('float', tree)
#         value = float(tree.children[0])
#         self.stack.append(value)
#
#     @v_args(tree=True)
#     def bool(self, tree):
#         print('bool', tree)
#         if tree.children[0] == 'true':
#             self.stack.append(True)
#         elif tree.children[0] == 'false':
#             self.stack.append(False)
#         else:
#             raise TypeError(f'Cannot convert {tree.children[0]} to boolean')
#
#     @v_args(tree=True)
#     def identifier(self, tree):
#         print('identifier', tree)
#         self.stack.append(str(tree.children[0]))
