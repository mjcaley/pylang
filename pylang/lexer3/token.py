#!/usr/bin/env python3

from enum import auto, Enum


class TokenType(Enum):
    Indent = auto()
    Dedent = auto()

    Newline = auto()

    Integer = auto()
    Float = auto()
    String = auto()

    Identifier = auto()

    # Keywords
    Function = 'func'
    Struct = 'struct'
    If = 'if'
    ElseIf = 'elif'
    Else = 'else'
    While = 'while'
    ForEach = 'for'
    And = 'and'
    Not = 'not'
    Or = 'or'
    True_ = 'true'
    False_ = 'false'
    Return = 'return'

    # Operators
    Dot = '.'
    Assignment = '='

    # Arithmetic operators
    Plus = '+'
    PlusAssign = '+='
    Minus = '-'
    MinusAssign = '-='
    Multiply = '*'
    MultiplyAssign = '*='
    Divide = '/'
    DivideAssign = '/='
    Modulo = '%'
    ModuloAssign = '%='
    Exponent = '**'
    ExponentAssign = '**='

    # Comparison operators
    Equal = '=='
    NotEqual = '!='
    LessThan = '<'
    GreaterThan = '>'
    LessThanOrEqual = '<='
    GreaterThanOrEqual = '>='

    LParen = '('
    RParen = ')'
    LBrace = '{'
    RBrace = '}'
    LSquare = '['
    RSquare = ']'

    Colon = ':'
    Comma = ','

    EOF = auto()

    Error = auto()


class Token:
    def __init__(self, token_type, position, value=None):
        self.token_type = token_type
        self.position = position
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
            f'token_type={repr(self.token_type)}, ' \
            f'position={repr(self.position)}, ' \
            f'value={repr(self.value)}'

    def __str__(self):
        return f'[{self.token_type}] - ' \
            f'line: {self.position.line}, ' \
            f'column: {self.position.column} - ' \
            f'{repr(self.value)}'
