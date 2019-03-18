#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Sequence

from .lexer import Token


class Expression:
    pass


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: Token
    right: Expression


@dataclass
class AssignmentExpression(BinaryExpression):
    pass


@dataclass
class SumExpression(BinaryExpression):
    pass


@dataclass
class ProductExpression(BinaryExpression):
    pass


@dataclass
class UnaryExpression(Expression):
    operator: Token
    expression: Expression


@dataclass
class Statement:
    expression: Expression


@dataclass
class Block:
    statements: Sequence[Statement]


@dataclass
class FunctionDecl:
    name: Token
    parameters: Sequence[Token]
    return_type: Token


@dataclass
class Function:
    definition: FunctionDecl
    block: Block


@dataclass
class Start:
    functions: Sequence[Function]


@dataclass
class Atom:
    value: Token


@dataclass
class Identifier(Atom):
    pass


@dataclass
class Boolean(Atom):
    pass


@dataclass
class Integer(Atom):
    pass


@dataclass
class Float(Atom):
    pass
