#!/usr/bin/env python3

from lark import Visitor, v_args


class MapFunctions(Visitor):
    def __init__(self):
        self.function_map = dict()

    @v_args(tree=True)
    def function(self, tree):
        self.function_map[self._function_name(tree.children[0])] = tree

    def _function_name(self, function_tree):
        return str(function_tree.children[0])


class Interpreter(Visitor):
    def __init__(self, function_map, entry='main'):
        self.entry = entry
        self.function_map = function_map
        self.stack = list()
        self.map = dict()

    def reset(self):
        self.stack.clear()
        self.map.clear()

    def run(self):
        self.visit(self.function_map[self.entry])

    @v_args(tree=True)
    def start(self, tree):
        print('start', tree)

    @v_args(tree=True)
    def statement(self, tree):
        print('statement', tree)
        self.stack.pop()

    @v_args(tree=True)
    def binary_expr(self, tree):
        print('binary_expr', tree)
        right = self.stack.pop()
        left = self.stack.pop()
        if tree.children[1].type == 'ADD_OP':
            self.stack.append(left + right)
        elif tree.children[1].type == 'SUB_OP':
            self.stack.append(left - right)
        elif tree.children[1].type == 'MUL_OP':
            self.stack.append(left * right)
        elif tree.children[1].type == 'DIV_OP':
            self.stack.append(left / right)
        elif tree.children[1].type == 'ASSIGN_OP':
            self.map[left] = right
            self.stack.append(self.map[left])
        else:
            raise SyntaxError(f'{str(tree.children[1])} is not a supported binary operator')

    @v_args(tree=True)
    def unary_expr(self, tree):
        print('unary_expr', tree)
        if tree.children[0].type == 'NEGATIVE_OP':
            val = self.stack.pop()
            val *= -1
            self.stack.append(val)
        elif tree.children[0].type == 'NOT_OP':
            val = self.stack.pop()
            val = not val
            self.stack.append(val)
        else:
            raise SyntaxError(f'{str(tree.children[0])} is not a supported unary operator')

    def call(self, tree):
        self.visit(self.function_map[tree.children[0].children[0]])

    @v_args(tree=True)
    def integer(self, tree):
        print('integer', tree)
        value = int(tree.children[0])
        self.stack.append(value)

    @v_args(tree=True)
    def float(self, tree):
        print('float', tree)
        value = float(tree.children[0])
        self.stack.append(value)

    @v_args(tree=True)
    def bool(self, tree):
        print('bool', tree)
        if tree.children[0] == 'true':
            self.stack.append(True)
        elif tree.children[0] == 'false':
            self.stack.append(False)
        else:
            raise TypeError(f'Cannot convert {tree.children[0]} to boolean')

    @v_args(tree=True)
    def identifier(self, tree):
        print('identifier', tree)
        self.stack.append(str(tree.children[0]))
