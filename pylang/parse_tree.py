#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Optional, Sequence, Union

from .lexer.token import Token


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


@dataclass
class String(Atom):
    pass


class Expression:
    pass


@dataclass
class BinaryExpression(Expression):
    left: Union[Expression, Atom]
    operator: Token
    right: Union[Expression, Atom]


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
    expression: Union[Expression, Atom]


@dataclass
class Statement:
    expression: Expression


@dataclass
class FunctionDecl:
    name: Identifier
    parameters: Sequence[Token]
    return_type: Optional[Identifier]


@dataclass
class Function:
    definition: FunctionDecl
    block: Sequence[Statement]
