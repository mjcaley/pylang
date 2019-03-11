#!/usr/bin/env python3

from collections import namedtuple
from enum import auto, Enum
from io import BytesIO, StringIO, TextIOWrapper
from string import digits


class TokenType(Enum):
    Start = auto()

    Indent = auto()
    Dedent = auto()

    Newline = auto()

    Digit = auto()
    String = auto()

    Identifier = auto()

    # Keywords
    Function = auto()
    Struct = auto()
    If = auto()
    While = auto()
    ForEach = auto()

    # Operators
    Dot = auto()

    LParen = auto()
    RParen = auto()
    LBrace = auto()
    RBrace = auto()
    Colon = auto()
    Semicolon = auto()

    EOF = auto()


class Token:
    def __init__(self, token_type, start_position, end_position, value=None):
        self.token_type = token_type
        self.start_position = start_position
        self.end_position = end_position
        self.value = value

    def __len__(self):
        return self.end_position.index - self.start_position.index

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
            f'token_type={repr(self.token_type)}, ' \
            f'start_position={repr(self.start_position)}, ' \
            f'end_position={repr(self.end_position)}, ' \
            f'value={repr(self.value)}'

    def __str__(self):
        return f'[{self.token_type}] - ' \
            f'line: {self.start_position.line}, ' \
            f'column: {self.start_position.column}, ' \
            f'length: {len(self)}'


Position = namedtuple('Position', ['index', 'line', 'column'])


"""
prime lexer with newline as next, start and end position is -1 index
emit token, emits newline
"""

SKIP = [
        # ASCII whitespace characters
        '\t', '\n', '\v', '\f', '\r', ' ',

        # Unicode whitespace
        '\u0085', '\u00a0', '\u1680', '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007',
        '\u2008', '\u2009', '\u200a', '\u2028', '\u2029', '\u202f', '\u205f', '\u3000',

        # Other whitespace characters
        '\u180e', '\u200b', '\u200c', '\u200d', '\u2060', '\ufeff']
NEWLINE = ['\n', '\r']
INDENT = ['\t', ' ']


class LexerException(Exception):
    pass


class Lexer:
    def __init__(self, data):
        if type(data) == str:
            self.data = StringIO(data)
        elif type(data) == bytes:
            self.data = TextIOWrapper(BytesIO(data), encoding='utf-8')
        else:
            self.data = data

        self.current = ''
        self.next = self.data.read(1)
        self.start_pos = Position(0, 1, 1)
        self.end_pos = Position(0, 1, 1)

        self.next_token = None
        self.set_token(TokenType.Start)

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

    def set_token(self, token_type, cast_func=str):
        self.next_token = Token(token_type, self.start_pos, self.end_pos, cast_func(self.current))
        self.discard_current()

    def newline(self):
        line_number = self.start_pos.line + 1
        length = self.end_pos.index - self.start_pos.index
        self.start_pos = Position(self.start_pos.index, line_number, 1)
        self.end_pos = Position(self.end_pos.index, line_number, length)

    def emit(self):
        """Emit a single token."""

        next_token = self.next_token
        if not self.current and not self.next:
            self.set_token(TokenType.EOF)
            return next_token
        else:
            self.append_to_current()

        if self.current == '\n':
            self.set_token(TokenType.Newline)
            self.discard_current()
            self.newline()
        elif self.current == '\r':
            if self.next == '\n':
                self.append_to_current()
            self.set_token(TokenType.Newline)
            self.discard_current()
            self.newline()
        elif self.current in digits:
            while self.next in digits:
                self.append_to_current()
            self.set_token(TokenType.Digit, int)
            self.discard_current()
        else:
            raise LexerException(self)

        return next_token
