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

    Integer = auto()
    Float = auto()                  # 4.2 or .42
    String = auto()

    Identifier = auto()

    # Keywords
    Function = auto()               # func
    Struct = auto()                 # struct
    If = auto()                     # if
    ElseIf = auto()                 # elif
    Else = auto()                   # else
    While = auto()                  # while
    ForEach = auto()                # for
    And = auto()                    # and
    Not = auto()                    # not
    Or = auto()                     # or
    True_ = auto()                  # true
    False_ = auto()                 # false

    # Operators
    Dot = auto()                    # .
    Assignment = auto()             # =

    # Arithmetic operators
    Add = auto()                    # +
    AddAssign = auto()              # +=
    Subtract = auto()               # -
    SubtractAssign = auto()         # -=
    Multiply = auto()               # *
    MultiplyAssign = auto()         # *=
    Divide = auto()                 # /
    DivideAssign = auto()           # /=
    Modulo = auto()                 # %
    ModuloAssign = auto()           # %=
    Exponent = auto()               # **
    ExponentAssign = auto()         # **=

    # Comparison operators
    Equal = auto()                  # ==
    NotEqual = auto()               # !=
    LessThan = auto()               # <
    GreaterThan = auto()            # >
    LessThanOrEqual = auto()        # <=
    GreaterThanOrEqual = auto()     # >=

    LParen = auto()
    RParen = auto()
    LBrace = auto()
    RBrace = auto()
    LSquare = auto()
    RSquare = auto()

    Colon = auto()
    Comma = auto()

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

SKIP = [
        # ASCII whitespace characters
        '\v', '\f', ' ',

        # Unicode whitespace
        '\u0085', '\u00a0', '\u1680', '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007',
        '\u2008', '\u2009', '\u200a', '\u2028', '\u2029', '\u202f', '\u205f', '\u3000',

        # Other whitespace characters
        '\u180e', '\u200b', '\u200c', '\u200d', '\u2060', '\ufeff']
NEWLINE = ['\n', '\r']
INDENT = ['\t', ' ']
ARITHMETIC_CHARACTERS = ['+', '-', '/', '*', '%', '^']
RESERVED_CHARACTERS = ['!', '=', '<', '>', '.', ':'] + ARITHMETIC_CHARACTERS + INDENT + NEWLINE + SKIP


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

        self.beginning = True
        self.indents = [0]
        self.brackets = []

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

    def set_token(self, token_type, cast_func=str, clobber=True):
        self.next_token = Token(token_type, self.start_pos, self.end_pos, cast_func(self.current))
        if clobber:
            self.discard_current()

    def newline(self):
        line_number = self.start_pos.line + 1
        length = self.end_pos.index - self.start_pos.index
        self.start_pos = Position(self.start_pos.index, line_number, 1)
        self.end_pos = Position(self.end_pos.index, line_number, max(1, length))
        if not self.brackets:
            # Inside a bracket, ignore indent/dedent
            self.beginning = True

    def skip(self):
        if self.current in SKIP and self.current:
            while self.next in SKIP and self.next:
                self.append_to_current()
            self.discard_current()
            self.append_to_current()

    def emit(self):
        """Emit a single token."""

        next_token = self.next_token

        if not self.current and not self.next:
            self.set_token(TokenType.EOF)
            return next_token

        # Indent and dedent handling for significant whitespace
        if self.beginning:
            while self.next in INDENT and self.next:
                self.append_to_current()
            indent_length = len(self.current.replace('\t', ' '))
            indent_top = self.indents[-1]
            if indent_length == indent_top:
                self.beginning = False
                self.discard_current()
            elif indent_length > indent_top:
                self.beginning = False
                self.indents.append(indent_length)
                self.set_token(TokenType.Indent, len)
                return next_token
            elif indent_length in self.indents:
                self.indents.pop()
                self.set_token(TokenType.Dedent, clobber=False)
                return next_token
            else:
                raise LexerException('Invalid indentation', self.start_pos)

        self.append_to_current()

        self.skip()

        if self.current == '\n':
            self.set_token(TokenType.Newline)
            self.newline()
        elif self.current == '\r':
            if self.next == '\n':
                self.append_to_current()
            self.set_token(TokenType.Newline)
            self.newline()
        elif self.current in digits:
            while self.next in digits and self.next:
                self.append_to_current()
            if self.next == '.':
                self.append_to_current()
                while self.next in digits and self.next:
                    self.append_to_current()
                self.set_token(TokenType.Float)
            else:
                self.set_token(TokenType.Integer, int)
        elif self.current == '.':
            if self.next in digits and self.next:
                self.append_to_current()
                while self.next in digits and self.next:
                    self.append_to_current()
                self.set_token(TokenType.Float)
            else:
                self.set_token(TokenType.Dot)
        elif self.current == '=':
            if self.next == '=':
                self.append_to_current()
                self.set_token(TokenType.Equal)
            else:
                self.set_token(TokenType.Assignment)
        elif self.current == '!':
            if self.next == '=':
                self.append_to_current()
                self.set_token(TokenType.NotEqual)
            else:
                raise LexerException('Expected = following !', self.start_pos)
        elif self.current == '>':
            if self.next == '=':
                self.append_to_current()
                self.set_token(TokenType.GreaterThanOrEqual)
            else:
                self.set_token(TokenType.GreaterThan)
        elif self.current == '<':
            if self.next == '=':
                self.append_to_current()
                self.set_token(TokenType.LessThanOrEqual)
            else:
                self.set_token(TokenType.LessThan)

        elif self.current == '+':
            if self.next == '=':
                self.append_to_current()
                self.set_token(TokenType.AddAssign)
            else:
                self.set_token(TokenType.Add)
        elif self.current == '-':
            if self.next == '=':
                self.append_to_current()
                self.set_token(TokenType.SubtractAssign)
            else:
                self.set_token(TokenType.Subtract)
        elif self.current == '*':
            if self.next == '*':
                self.append_to_current()
                if self.next == '=':
                    self.append_to_current()
                    self.set_token(TokenType.ExponentAssign)
                else:
                    self.set_token(TokenType.Exponent)
            elif self.next == '=':
                self.append_to_current()
                self.set_token(TokenType.MultiplyAssign)
            else:
                self.set_token(TokenType.Multiply)
        elif self.current == '/':
            if self.next == '=':
                self.append_to_current()
                self.set_token(TokenType.DivideAssign)
            else:
                self.set_token(TokenType.Divide)
        elif self.current == '%':
            if self.next == '=':
                self.append_to_current()
                self.set_token(TokenType.ModuloAssign)
            else:
                self.set_token(TokenType.Modulo)

        elif self.current == ':':
            self.set_token(TokenType.Colon)
        elif self.current == ',':
            self.set_token(TokenType.Comma)

        elif self.current == '[':
            self.brackets.append(self.current)
            self.set_token(TokenType.LSquare)
        elif self.current == ']':
            if self.brackets[-1] != '[':
                raise LexerException(f'Mismatched bracket at {self.start_pos.line}:{self.start_pos.column}')
            self.brackets.pop()
            self.set_token(TokenType.RSquare)
        elif self.current == '{':
            self.brackets.append(self.current)
            self.set_token(TokenType.LBrace)
        elif self.current == '}':
            if self.brackets[-1] != '{':
                raise LexerException(f'Mismatched bracket at {self.start_pos.line}:{self.start_pos.column}')
            self.brackets.pop()
            self.set_token(TokenType.RBrace)
        elif self.current == '(':
            self.brackets.append(self.current)
            self.set_token(TokenType.LParen)
        elif self.current == ')':
            if self.brackets[-1] != '(':
                raise LexerException(f'Mismatched bracket at {self.start_pos.line}:{self.start_pos.column}')
            self.brackets.pop()
            self.set_token(TokenType.RParen)

        elif self.current:
            while self.next and self.next not in RESERVED_CHARACTERS:
                self.append_to_current()

            if self.current == 'func':
                self.set_token(TokenType.Function)
            elif self.current == 'struct':
                self.set_token(TokenType.Struct)
            elif self.current == 'if':
                self.set_token(TokenType.If)
            elif self.current == 'elif':
                self.set_token(TokenType.ElseIf)
            elif self.current == 'else':
                self.set_token(TokenType.Else)
            elif self.current == 'while':
                self.set_token(TokenType.While)
            elif self.current == 'for':
                self.set_token(TokenType.ForEach)
            elif self.current == 'and':
                self.set_token(TokenType.And)
            elif self.current == 'or':
                self.set_token(TokenType.Or)
            elif self.current == 'not':
                self.set_token(TokenType.Not)
            elif self.current == 'true':
                self.set_token(TokenType.True_)
            elif self.current == 'false':
                self.set_token(TokenType.False_)
            else:
                self.set_token(TokenType.Identifier)
        else:
            raise LexerException(self)

        return next_token
