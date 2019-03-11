#!/usr/bin/env python3

from collections import namedtuple
from enum import auto, Enum
from io import BytesIO, StringIO, TextIOWrapper
from string import digits


class TokenType(Enum):
    Indent = auto()
    Dedent = auto()

    Integer = auto()
    Float = auto()
    String = auto()

    Identifier = auto()

    # Keywords
    Function = auto()
    Struct = auto()
    If = auto()
    While = auto()
    ForEach = auto()

    LParen = auto()
    RParen = auto()
    LBrace = auto()
    RBrace = auto()
    Colon = auto()
    Semicolon = auto()


class Token:
    def __init__(self, token_type, position, value):
        self.token_type = token_type
        self.position = position
        self.value = value


Position = namedtuple('Position', ['index', 'line', 'column'])


"""
prime lexer with newline as next, start and end position is -1 index
emit token, emits newline
"""


class Lexer:
    def __init__(self, data):
        if type(data) == str:
            self.data = StringIO(data)
        elif type(data) == bytes:
            self.data = TextIOWrapper(BytesIO(data), encoding='utf-8')
        else:
            self.data = data

        self.current = ''
        self.next = '\n'
        self.start_pos = Position(-1, 0, 0)
        self.end_pos = Position(-1, 0, 0)

    def is_eof(self):
        return bool(self.next)

    def increment_position(self):
        self.end_pos = Position(
            self.end_pos.index + 1,
            self.end_pos.line,
            self.end_pos.column + 1
        )

    def discard_current(self):
        self.current = ''
        self.start_pos = self.end_pos

    def append_to_current(self):
        self.current += self.next
        self.increment_position()
        self.next = self.data.read(1)

    def emit(self):
        """Emit a single token."""

        while not self.is_eof():
            if self.next == '\n':

