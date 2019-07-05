#!/usr/bin/env python3

from collections import namedtuple
from enum import auto, Enum
from io import BytesIO, StringIO, TextIOWrapper
from string import digits


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


class Lexer:
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

    def __init__(self, data):
        if type(data) == str:
            self.data = StringIO(data)
        elif type(data) == bytes:
            self.data = TextIOWrapper(BytesIO(data), encoding='utf-8')
        else:
            self.data = data

        self.current = ''
        self.current_position = Position(index=0, line=1, column=1)

        self.next = self.data.read(1)
        self.next_position = Position(index=0, line=1, column=1)

        self.beginning = True
        self.indents = [0]
        self.brackets = []

        self.token = Token(
            token_type=TokenType.Indent,
            position=self.current_position,
            value=0
        )

    def advance(self):
        last = self.next
        self.next = self.data.read(1)

        if not last:
            pass
        elif last == '\n':
            self.next_position = Position(
                index=self.next_position.index + 1,
                line=self.next_position.line + 1,
                column=1
            )
            self.beginning = True
        elif last == '\r' and self.next != '\n':
            self.next_position = Position(
                index=self.next_position.index + 1,
                line=self.next_position.line + 1,
                column=1
            )
            self.beginning = True
        else:
            self.next_position = Position(
                index=self.next_position.index + 1,
                line=self.next_position.line,
                column=self.next_position.column + 1
            )

        return last

    def __iter__(self):
        return self

    def __next__(self):
        return self.emit()

    def append(self):
        if not self.current:
            self.current_position = self.next_position
        next_character = self.advance()
        self.current += next_character

    def append_while(self, characters):
        while self.next in characters and self.next:
            self.append()

    def append_while_not(self, characters):
        while self.next not in characters and self.next:
            self.append()

    def consume(self):
        current = self.current
        self.current = ''

        return current

    def discard(self):
        self.consume()

    def skip(self):
        self.append_while(self.WHITESPACE)
        self.consume()

    def skip_until(self, characters):
        while self.next not in characters:
            self.advance()

    def skip_while(self, characters):
        while self.next in characters and self.next:
            self.advance()

    def skip_empty_lines(self):
        while self.current and self.match_next(self.NEWLINE):
            self.skip_while(self.NEWLINE)
            self.discard()
            self.append_while(self.WHITESPACE + self.INDENT)

    def match(self, characters):
        return characters == self.current

    def match_next(self, characters):
        return all([self.next in characters, self.next])

    def contains(self, characters):
        return all([self.current in characters, self.current])

    def next_contains(self, characters):
        return all([self.next in characters, self.next])

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
        self.token = token
        return token

    def emit(self):
        next_token = self.token

        if self.is_indent_dedent():
            return next_token

        self.skip_while(self.WHITESPACE + self.INDENT)

        self.append()

        if self.is_eof():
            if self.indents:
                dedent = self.indents.pop()
                self.new_token(token_type=TokenType.Dedent, value=dedent)
            else:
                self.new_token(token_type=TokenType.EOF)
            return next_token

        if self.match('\n'):
            self.new_token(token_type=TokenType.Newline, value=self.discard())
        elif self.match('\r'):
            if self.match_next('\n'):
                self.append()
            self.new_token(token_type=TokenType.Newline, value=self.discard())

        elif self.match('+'):
            if self.match_next('='):
                self.append()
                self.new_token(token_type=TokenType.PlusAssign, value=self.discard())
            else:
                self.new_token(token_type=TokenType.Plus, value=self.discard())
        elif self.match('-'):
            if self.match_next('='):
                self.append()
                self.new_token(token_type=TokenType.MinusAssign, value=self.discard())
            else:
                self.new_token(token_type=TokenType.Minus, value=self.discard())
        elif self.match('*'):
            if self.match_next('='):
                self.append()
                self.new_token(token_type=TokenType.MultiplyAssign, value=self.discard())
            elif self.match_next('*'):
                self.append()
                if self.match_next('='):
                    self.append()
                    self.new_token(token_type=TokenType.ExponentAssign, value=self.discard())
                else:
                    self.new_token(token_type=TokenType.Exponent, value=self.discard())
            else:
                self.new_token(token_type=TokenType.Multiply, value=self.discard())
        elif self.match('/'):
            if self.match_next('='):
                self.append()
                self.new_token(token_type=TokenType.DivideAssign, value=self.discard())
            else:
                self.new_token(token_type=TokenType.Divide, value=self.discard())
        elif self.match('%'):
            if self.match_next('='):
                self.append()
                self.new_token(token_type=TokenType.ModuloAssign, value=self.discard())
            else:
                self.new_token(token_type=TokenType.Modulo, value=self.discard())

        elif self.match('='):
            if self.match_next('='):
                self.append()
                self.new_token(token_type=TokenType.Equal, value=self.discard())
            else:
                self.new_token(token_type=TokenType.Assignment, value=self.discard())
        elif self.match('!'):
            if self.match_next('='):
                self.append()
                self.new_token(token_type=TokenType.NotEqual, value=self.discard())
            else:
                self.new_token(token_type=TokenType.Error, value=self.consume())
        elif self.match('<'):
            if self.match_next('='):
                self.append()
                self.new_token(token_type=TokenType.LessThanOrEqual, value=self.discard())
            else:
                self.new_token(token_type=TokenType.LessThan, value=self.discard())
        elif self.match('>'):
            if self.match_next('='):
                self.append()
                self.new_token(token_type=TokenType.GreaterThanOrEqual, value=self.discard())
            else:
                self.new_token(token_type=TokenType.GreaterThan, value=self.discard())

        elif self.match('.'):
            self.new_token(token_type=TokenType.Dot, value=self.discard())
        elif self.match(':'):
            self.new_token(token_type=TokenType.Colon, value=self.discard())
        elif self.match(','):
            self.new_token(token_type=TokenType.Comma, value=self.discard())

        elif self.match('('):
            self.push_bracket(TokenType.LParen)
            self.discard()
        elif self.match('['):
            self.push_bracket(TokenType.LSquare)
            self.discard()
        elif self.match('{'):
            self.push_bracket(TokenType.LBrace)
            self.discard()

        elif self.match(')'):
            self.pop_bracket(TokenType.LParen, TokenType.RParen)
            self.discard()
        elif self.match(']'):
            self.pop_bracket(TokenType.LSquare, TokenType.RSquare)
            self.discard()
        elif self.match('}'):
            self.pop_bracket(TokenType.LBrace, TokenType.RBrace)
            self.discard()

        elif self.contains(digits):
            self.append_while(digits)
            while self.match_next('_'):
                self.advance()
                self.append_while(digits)
            self.new_token(TokenType.Digits, int(self.consume()))

        else:
            self.append_while_not(self.RESERVED_CHARACTERS)

            if self.match('func'):
                self.new_token(token_type=TokenType.Function, value=self.consume())
            elif self.match('struct'):
                self.new_token(token_type=TokenType.Struct, value=self.consume())
            elif self.match('if'):
                self.new_token(token_type=TokenType.If, value=self.consume())
            elif self.match('elif'):
                self.new_token(token_type=TokenType.ElseIf, value=self.consume())
            elif self.match('else'):
                self.new_token(token_type=TokenType.Else, value=self.consume())
            elif self.match('while'):
                self.new_token(token_type=TokenType.While, value=self.consume())
            elif self.match('for'):
                self.new_token(token_type=TokenType.ForEach, value=self.consume())
            elif self.match('and'):
                self.new_token(token_type=TokenType.And, value=self.consume())
            elif self.match('or'):
                self.new_token(token_type=TokenType.Or, value=self.consume())
            elif self.match('not'):
                self.new_token(token_type=TokenType.Not, value=self.consume())
            elif self.match('true'):
                self.consume()
                self.new_token(token_type=TokenType.True_, value=True)
            elif self.match('false'):
                self.consume()
                self.new_token(token_type=TokenType.False_, value=False)
            elif self.match('return'):
                self.new_token(token_type=TokenType.Return, value=self.consume())
            else:
                self.new_token(token_type=TokenType.Identifier, value=self.consume())

        return next_token
