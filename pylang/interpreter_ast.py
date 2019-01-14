#!/usr/bin/env python3

from lark import Transformer


class Literal:
    def __init__(self, value):
        self.value = value


class Integer(Literal):
    def __init__(self, value):
        super().__init__(int(value))


class Float(Literal):
    def __init__(self, value):
        super().__init__(float(value))


class Boolean(Literal):
    def __init__(self, value):
        super().__init__(True if value == 'true' else False)


# TODO: Identfier isn't a literal
class Identifier(Literal):
    def __init__(self, value):
        super().__init__(value)


class Expression:
    def __call__(self):
        raise NotImplementedError


class BinaryExpression(Expression):
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation

    def __call__(self):
        return self.operation(self.left, self.right)


class AddExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, lambda l, r: l + r)


class SubtractExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, lambda l, r: l - r)


class MultiplyExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, lambda l, r: l * r)


class DivideExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, lambda l, r: l / r)


class AssignmentExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, None)


class UnaryExpression(Expression):
    def __init__(self, value, operation):
        self.value = value
        self.operation = operation

    def __call__(self):
        return self.operation(self.value)


class NotExpression(UnaryExpression):
    def __init__(self, literal):
        super().__init__(literal, lambda v: not v)


class NegativeExpression(UnaryExpression):
    def __init__(self, literal):
        super().__init__(literal, lambda v: -v)


class Statement:
    def __init__(self, expressions):
        self.expression = expressions


class ToAST(Transformer):
    def integer(self, children):
        return Integer(children[0].value)

    def float(self, children):
        return Float(children[0].value)

    def true(self, children):
        return Boolean(children[0].value)

    def false(self, children):
        return Boolean(children[0].value)

    def identifier(self, children):
        return Identifier(children[0].value)

    def binary_expr(self, children):
        if len(children) > 1:
            if children[1].type == 'MUL_OP':
                return MultiplyExpression(children[0], children[2])
            elif children[1].type == 'DIV_OP':
                return DivideExpression(children[0], children[2])
            elif children[1].type == 'ADD_OP':
                return AddExpression(children[0], children[2])
            elif children[1].type == 'SUB_OP':
                return SubtractExpression(children[0], children[2])
            elif children[1].type == 'ASSIGN_OP':
                return AssignmentExpression(children[0], children[2])
        else:
            return children

    def unary_expr(self, children):
        if len(children) > 1:
            if children[0].type == 'NOT_OP':
                return NotExpression(children[1])
            elif children[0].type == 'NEGATIVE_OP':
                return NegativeExpression(children[1])
        else:
            return children

    def statement(self, children):
        return Statement(children[0])

    def start(self, children):
        return children

