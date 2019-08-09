#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from enum import auto, Enum
from io import BytesIO, StringIO, TextIOWrapper
from string import digits, octdigits, hexdigits


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
            return Character(None, character)
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


class LexerException(Exception):
    pass


class MismatchedIndentException(LexerException):
    def __init__(self, expected, found):
        self.expected = expected
        self.found = found


class MismatchedBracketException(LexerException):
    def __init__(self, expected, found):
        self.expected = expected
        self.found = found


class LexerContext:
    def __init__(self):
        self._indents = []
        self._brackets = []

    def push_indent(self, length):
        if self._indents:
            top = self._indents[-1]
            if top > length:
                raise MismatchedIndentException(expected=top, found=length)
        self._indents.append(length)

    def pop_indent(self, until):
        try:
            index = self._indents.index(until) + 1  # One ahead of matched indent
        except ValueError:
            raise MismatchedIndentException(expected=until, found=None)

        self._indents, popped = self._indents[:index], [level for level in reversed(self._indents[index:])]

        return popped

    def push_bracket(self, bracket):
        self._brackets.append(bracket)

    def pop_bracket(self, expected):
        top = self._brackets.pop()
        if top != expected:
            raise MismatchedBracketException(expected=expected, found=top)
        else:
            return top


class Lexer:
    def __init__(self, data):
        self.stream = Stream(data)
        self.context = LexerContext()
        self.state = self.start()

        self._current = ''
        self._current_position = None

        self._next = ''
        self._next_position = None

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.state)

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

    def transition(self, state):
        self.state = state()
        return self.state

    def transition_and_yield(self, state):
        new_state = self.transition(state)
        return next(new_state)

    def advance(self):
        self._current_position, self._current = self._next_position, self._next
        self._next_position, self._next = next(self.stream)

        return self._current_position, self._current

    # def append(self):
    #     if not self.current:
    #         self._current_position = self._next_position
    #     next_character = self.advance()
    #     self._current += next_character

    def append_while(self, characters):
        string = ''
        while self._next in characters and self._next:
            _, character = self.advance()
            string += character
        return string

    def append_while_not(self, characters):
        string = ''
        while self.next not in characters and self.next:
            _, character = self.advance()
            string += character
        return string

    def skip_until(self, characters):
        while self.current not in characters or not self.current:
            self.advance()

    def skip_while(self, characters):
        while self.current in characters or not self.current:
            self.advance()

    def skip_whitespace(self):
        self.skip_while(WHITESPACE)

    def skip_empty_lines(self):
        # Weird implementation, might not work
        while self.current and self.match_next(NEWLINE):
            self.skip_while(NEWLINE)
            self.append_while(WHITESPACE + INDENT)

    def match(self, character):
        return character == self.current

    def match_next(self, character):
        return character == self.next

    def current_in(self, characters):
        return all([self.current in characters, self.current])

    def next_in(self, characters):
        return all([self.next in characters, self.next])

    def is_indent_dedent(self):
        if self._start_of_line:
            self.append_while(INDENT)
            self.skip_empty_lines()
            indent = len(self.consume())
            top = self._indents[-1]
            self._start_of_line = False

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

    def start(self):
        self.advance()
        if not self.current:
            self.transition(self.operators)
            yield Token(TokenType.Indent, None)

    def operators(self):
        while True:
            position, character = self.advance()

            if not self.current:
                # End of file
                yield self.transition_and_yield(self.end)

            if self.match('+'):
                if self.match_next('='):
                    self.advance()
                    yield Token(TokenType.PlusAssign, position)
                yield Token(TokenType.Plus, self.current_position)
            elif self.match('-'):
                if self.match_next('='):
                    self.advance()
                    yield Token(TokenType.MinusAssign, position)
                yield Token(TokenType.Minus, position)
            elif self.match('*'):
                if self.match_next('='):
                    self.advance()
                    yield Token(TokenType.MultiplyAssign, position)
                elif self.match_next('*'):
                    position = self.current_position
                    self.advance()
                    if self.match_next('='):
                        self.advance()
                        yield Token(TokenType.ExponentAssign, position)
                    else:
                        yield Token(TokenType.Exponent, position)
                else:
                    yield Token(TokenType.Multiply, position)
            elif self.match('/'):
                if self.match_next('='):
                    self.advance()
                    yield Token(TokenType.DivideAssign, position)
                yield Token(TokenType.Divide, position)
            elif self.match('%'):
                if self.match_next('='):
                    self.advance()
                    yield Token(TokenType.ModuloAssign, position)
                yield Token(TokenType.Modulo, position)
            elif self.match('='):
                if self.match_next('='):
                    self.advance()
                    yield Token(TokenType.Equal, position)
                else:
                    yield Token(TokenType.Assignment, position)
            elif self.match('!'):
                if self.match_next('='):
                    self.advance()
                    yield Token(TokenType.NotEqual, position)
                else:
                    yield Token(TokenType.Error, position)
            elif self.match('<'):
                if self.match_next('='):
                    self.advance()
                    yield Token(TokenType.LessThanOrEqual, position)
                else:
                    yield Token(TokenType.LessThan, position)
            elif self.match('>'):
                if self.match_next('='):
                    self.advance()
                    yield Token(TokenType.GreaterThanOrEqual, position)
                else:
                    yield Token(TokenType.GreaterThan, position)
            elif self.match('.'):
                yield Token(TokenType.Dot, position)
            elif self.match(':'):
                yield Token(TokenType.Colon, position)
            elif self.match(','):
                yield Token(TokenType.Comma, position)

            elif self.match('('):
                self.context.push_bracket(character)
                yield Token(TokenType.LParen, position)
            elif self.match('['):
                self.context.push_bracket(character)
                yield Token(TokenType.LSquare, position)
            elif self.match('{'):
                self.context.push_bracket(character)
                yield Token(TokenType.LBrace, position)
            elif self.match(')'):
                try:
                    self.context.pop_bracket('(')
                except MismatchedBracketException as e:
                    yield Token(TokenType.Error, position, f'Opening bracket was {e.expected}')
                else:
                    yield Token(TokenType.RParen, position)
            elif self.match(']'):
                try:
                    self.context.pop_bracket('[')
                except MismatchedBracketException as e:
                    yield Token(TokenType.Error, position, f'Opening bracket was {e.expected}')
                else:
                    yield Token(TokenType.RSquare, position)
            elif self.match('}'):
                try:
                    self.context.pop_bracket('{')
                except MismatchedBracketException as e:
                    yield Token(TokenType.Error, position, f'Opening bracket was {e.expected}')
                else:
                    yield Token(TokenType.RBrace, position)

            elif self.current_in(digits):
                yield self.transition_and_yield(self.number)
            elif self.match('"'):
                yield self.transition_and_yield(self.string)
            elif not self.current_in(RESERVED_CHARACTERS):
                yield self.transition_and_yield(self.word)

    def number(self):
        pass

    def string(self):
        pass

    def word(self):
        pass

    def end(self):
        yield Token(TokenType.Dedent, None)
