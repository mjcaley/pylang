#!/usr/bin/env python3

from collections import namedtuple
from enum import auto, Enum
from io import BytesIO, StringIO, TextIOWrapper
from string import digits


"""Lexer implemented as finite state machine.

States:
    Start
        Indent token
        transition to Operators

    Operators
        Operator/Indent/Dedent tokens
        transitions to Word state if a non-operator character is found
        transitions to Digit state if number character is found
        transitions to End if EOF file is found

    Word
        consumes character until non-word character is found (e.g. whitespace, newline, operator)
        if keyword, emits keyword token
        else emits Identifier token
        transitions to Operators

    Digit
        utility function: Number
            if 0 is first character, check if 0x, 0b or 0o
            consume until not a digit

        Number func
        if match_next == .
            # might be float or call
            consume .
            if match_next == 0-9
                # 0x123.0b123
                Number func
                emit Float token
                transition to Operators
            elif match_next == a-zA-Z_
                # 0x123.call_func
                emit Integer
                emit Dot
                transition to Word
            else
                # 0x123. newline or whitespace or operator
                emit Float (0x123.0)
                transition to Operators
        else
            emit Integer
            transition to Operators

    End
        Dedent token
        EOF token
        StopIteration exception

    Stream:
        contains text stream
        current position
        current character
        next character
        indent/dedent level

        utility functions
            advance
            consume

    Lexer
        instance of Stream
        initial state is Start

        iterator protocol that calls state(stream)
"""


class TokenType(Enum):
    Indent = auto()
    Dedent = auto()

    Newline = auto()

    Digits = auto()
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


Position = namedtuple('Position', ['index', 'line', 'column'])


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


Character = namedtuple('Character', ['position', 'character'])


class Stream:
    def __init__(self, data):
        if type(data) == str:
            self._data = StringIO(data, newline=None)
        elif type(data) == bytes:
            self._data = TextIOWrapper(BytesIO(data), encoding='utf-8', newline=None)
        else:
            self._data = data

        self._position = Position(index=-1, line=1, column=0)

    def __iter__(self):
        return self

    def __next__(self):
        character = self._data.read(1)

        if character == '':
            return Character(self._position, character)
        elif character == '\n':
            position = Position(
                index=self._position.index + 1,
                line=self._position.line,
                column=self._position.column)
            self._position = Position(
                index=position.index,
                line=position.line + 1,
                column=0)
            return Character(position, character)
        else:
            self._position = Position(
                index=self._position.index + 1,
                line=self._position.line,
                column=self._position.column + 1)

        return Character(self._position, character)


WHITESPACE = [
        # ASCII whitespace characters
        '\v', '\f', ' ',

        # Unicode whitespace
        '\u0085', '\u00a0', '\u1680', '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007',
        '\u2008', '\u2009', '\u200a', '\u2028', '\u2029', '\u202f', '\u205f', '\u3000',

        # Other whitespace characters
        '\u180e', '\u200b', '\u200c', '\u200d', '\u2060', '\ufeff'
]
NEWLINE = ['\n', '\r']
INDENT = ['\t', ' ']
ARITHMETIC_CHARACTERS = ['+', '-', '/', '*', '%', '^']
BRACKETS = ['(', ')', '[', ']', '{', '}']
RESERVED_CHARACTERS = ['!', '=', '<', '>', '.', ':',
                       ','] + ARITHMETIC_CHARACTERS + BRACKETS + INDENT + NEWLINE + WHITESPACE


class LexerState:
    def __init__(self, data):
        if type(data) == str:
            self._data = StringIO(data)
        elif type(data) == bytes:
            self._data = TextIOWrapper(BytesIO(data), encoding='utf-8')
        else:
            self._data = data

        self._current = ''
        self._current_position = Position(index=0, line=1, column=1)

        self._next = self._data.read(1)
        self._next_position = Position(index=0, line=1, column=1)

        self.beginning = True
        self._indents = [0]
        self._brackets = []

    def __iter__(self):
        return self

    def __next__(self):
        character = self.advance()

        return character

    @property
    def current(self):
        return self._current

    @property
    def current_position(self):
        return self._current_position

    @property
    def next(self):
        return self._next

    @property
    def next_position(self):
        return self._next_position

    # Mutating methods
    def advance(self):
        last = self._next
        self._next = self._data.read(1)

        if not last:
            pass
        elif last == '\n':
            self._next_position = Position(
                index=self.next_position.index + 1,
                line=self.next_position.line + 1,
                column=1
            )
            self.beginning = True
        elif last == '\r' and self.next != '\n':
            self._next_position = Position(
                index=self.next_position.index + 1,
                line=self.next_position.line + 1,
                column=1
            )
            self.beginning = True
        else:
            self._next_position = Position(
                index=self.next_position.index + 1,
                line=self.next_position.line,
                column=self.next_position.column + 1
            )

        return last


    def append(self):
        if not self.current:
            self._current_position = self.next_position
        next_character = self.advance()
        self._current += next_character

    def append_while(self, characters):
        while self.next in characters and self.next:
            self.append()

    def append_while_not(self, characters):
        while self.next not in characters and self.next:
            self.append()

    def consume(self):
        current = self._current
        self._current = ''

        return current

    def discard(self):
        self.consume()

    def skip(self):
        self.append_while(WHITESPACE)
        self.consume()

    def skip_until(self, characters):
        while self.next not in characters:
            self.advance()

    def skip_while(self, characters):
        while self.next in characters and self.next:
            self.advance()

    def skip_empty_lines(self):
        while self.current and self.match_next(NEWLINE):
            self.skip_while(NEWLINE)
            self.discard()
            self.append_while(WHITESPACE + INDENT)

    def match(self, characters):
        return characters == self.current

    def match_next(self, characters):
        return all([self.next in characters, self.next])

    def contains(self, characters):
        return all([self.current in characters, self.current])

    def next_contains(self, characters):
        return all([self.next in characters, self.next])

    # Indent management


    def push_bracket(self, left_token_type):
        self.brackets.append(left_token_type)
        return self.new_token(
            token_type=left_token_type
        )

    def pop_bracket(self, left_token_type, right_token_type):
        try:
            if self.brackets[-1] == left_token_type:
                self.new_token(
                    token_type=right_token_type
                )
            else:
                self.new_token(
                    token_type=TokenType.Error,
                    value=right_token_type
                )
        except IndexError:
            self.new_token(
                token_type=TokenType.Error,
                value=right_token_type
            )

    def is_indent_dedent(self):
        if self.beginning:
            self.append_while(self.INDENT)
            self.skip_empty_lines()
            indent = len(self.consume())
            top = self.indents[-1]
            self.beginning = False

            if indent > top:
                self.new_token(
                    token_type=TokenType.Indent,
                    value=indent
                )
                self.indents.append(indent)
                return True
            elif indent < top:
                dedent = self.indents.pop()
                self.new_token(
                    token_type=TokenType.Dedent,
                    value=dedent
                )
                return True

    def is_eof(self):
        return all([not self.current, not self.next])

    def new_token(self, token_type, value=None):
        token = Token(
            token_type=token_type,
            position=self.current_position,
            value=value
        )

        return token


class Lexer:
    def __init__(self, data):
        self._lexer_state = LexerState(data)
        self._state = self.file

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._state)

    def operator(self):
        while not self._lexer_state.is_eof():
            self._lexer_state.new_token(TokenType.Digits)


    def file(self):
        yield self._lexer_state.new_token(TokenType.Indent)
        self._state = self.operator
        yield self._lexer_state.new_token(TokenType.Dedent)
        yield self._lexer_state.new_token(TokenType.EOF)
