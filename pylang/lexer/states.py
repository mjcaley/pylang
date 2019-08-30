#!/usr/bin/env python3

from string import digits, hexdigits, octdigits

from .characters import INDENT, NEWLINE, RESERVED_CHARACTERS, WHITESPACE
from .exceptions import InvalidNumberInputException, MismatchedBracketException, MismatchedIndentException
from .token import Token, TokenType


class State:
    def __init__(self, context):
        self.context = context

    def append_while(self, characters):
        string = ''
        while self.context.current in characters and self.context.current:
            string += self.context.current
            self.context.advance()
        return string

    def append_while_not(self, characters):
        string = ''
        while self.context.current not in characters and self.context.current:
            string += self.context.current
            self.context.advance()
        return string

    def skip_until(self, characters):
        while self.context.current not in characters or not self.context.current:
            self.context.advance()

    def skip_while(self, characters):
        while self.context.current in characters and self.context.current:
            self.context.advance()

    def skip_whitespace(self):
        self.skip_while(WHITESPACE)

    def match(self, character):
        return character == self.context.current

    def match_next(self, character):
        return character == self.context.next

    def current_in(self, characters):
        return all([self.context.current in characters, self.context.current])

    def next_in(self, characters):
        return all([self.context.next in characters, self.context.next])

    @property
    def eof(self):
        return not any([self.context.current, self.context.next])

    def __call__(self):
        raise NotImplementedError


class Start(State):
    def __call__(self):
        state = FileStart(self.context)

        return state()


class FileStart(State):
    def __call__(self):
        self.context.advance()
        self.context.advance()
        self.context.push_indent(0)

        return IsEOF(self.context), Token(TokenType.Indent, None)


class IsEOF(State):
    def __call__(self):
        if self.eof:
            state = Dedent(self.context, target_indent=0)
            return state()
        else:
            state = Indent(self.context)
            return state()


class Indent(State):
    def __call__(self):
        position = self.context.current_position

        # Skip if not at beginning of line
        if position.column != 1:
            state = Operators(self.context)
            return state()

        while True:
            whitespace = len(self.append_while(INDENT))
            self.skip_whitespace()
            if self.current_in(NEWLINE):
                self.context.advance()
            else:
                break

        if self.eof:
            state = IsEOF(self.context)
            return state()
        
        if self.context.bracket:
            state = Operators(self.context)
            return state()

        if whitespace > self.context.indent:
            self.context.push_indent(whitespace)
            return Operators(self.context), Token(TokenType.Indent, position)
        elif whitespace == self.context.indent:
            state = Operators(self.context)
            return state()
        elif whitespace < self.context.indent:
            state = Dedent(self.context, target_indent=whitespace)
            return state()


class Dedent(State):
    def __init__(self, *args, target_indent, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_indent = target_indent

    def __call__(self):
        if self.target_indent == self.context.indent:
            if self.match(''):
                state = FileEnd(self.context)
                return state()
            else:
                state = IsEOF(self.context)
                return state()
        elif self.target_indent < self.context.indent:
            self.context.pop_indent()
            return self, Token(TokenType.Dedent, self.context.current_position)


class Operators(State):
    def __call__(self):
        position = self.context.current_position
        character = self.context.current

        if self.eof:
            state = IsEOF(self.context)
            return state()

        is_eof = IsEOF(self.context)
        if self.match('+'):
            self.context.advance()
            if self.match('='):
                self.context.advance()
                return is_eof, Token(TokenType.PlusAssign, position)
            return is_eof, Token(TokenType.Plus, position)
        elif self.match('-'):
            self.context.advance()
            if self.match('='):
                self.context.advance()
                return is_eof, Token(TokenType.MinusAssign, position)
            return is_eof, Token(TokenType.Minus, position)
        elif self.match('*'):
            self.context.advance()
            if self.match('='):
                self.context.advance()
                return is_eof, Token(TokenType.MultiplyAssign, position)
            elif self.match('*'):
                self.context.advance()
                if self.match('='):
                    self.context.advance()
                    return is_eof, Token(TokenType.ExponentAssign, position)
                else:
                    return is_eof, Token(TokenType.Exponent, position)
            else:
                return is_eof, Token(TokenType.Multiply, position)
        elif self.match('/'):
            self.context.advance()
            if self.match('='):
                self.context.advance()
                return is_eof, Token(TokenType.DivideAssign, position)
            return is_eof, Token(TokenType.Divide, position)
        elif self.match('%'):
            self.context.advance()
            if self.match('='):
                self.context.advance()
                return is_eof, Token(TokenType.ModuloAssign, position)
            return is_eof, Token(TokenType.Modulo, position)
        elif self.match('='):
            self.context.advance()
            if self.match('='):
                self.context.advance()
                return is_eof, Token(TokenType.Equal, position)
            else:
                return is_eof, Token(TokenType.Assignment, position)
        elif self.match('!'):
            self.context.advance()
            if self.match('='):
                self.context.advance()
                return is_eof, Token(TokenType.NotEqual, position)
            else:
                return is_eof, Token(TokenType.Error, position)
        elif self.match('<'):
            self.context.advance()
            if self.match('='):
                self.context.advance()
                return is_eof, Token(TokenType.LessThanOrEqual, position)
            else:
                return is_eof, Token(TokenType.LessThan, position)
        elif self.match('>'):
            self.context.advance()
            if self.match('='):
                self.context.advance()
                return is_eof, Token(TokenType.GreaterThanOrEqual, position)
            else:
                return is_eof, Token(TokenType.GreaterThan, position)
        elif self.match('.'):
            self.context.advance()
            return is_eof, Token(TokenType.Dot, position)
        elif self.match(':'):
            self.context.advance()
            return is_eof, Token(TokenType.Colon, position)
        elif self.match(','):
            self.context.advance()
            return is_eof, Token(TokenType.Comma, position)

        elif self.match('('):
            self.context.advance()
            self.context.push_bracket(character)
            return is_eof, Token(TokenType.LParen, position)
        elif self.match('['):
            self.context.advance()
            self.context.push_bracket(character)
            return is_eof, Token(TokenType.LSquare, position)
        elif self.match('{'):
            self.context.advance()
            self.context.push_bracket(character)
            return is_eof, Token(TokenType.LBrace, position)
        elif self.match(')'):
            self.context.advance()
            try:
                self.context.pop_bracket('(')
            except MismatchedBracketException as e:
                return is_eof, Token(TokenType.Error, position, f'Opening bracket was {e.expected}')
            else:
                return is_eof, Token(TokenType.RParen, position)
        elif self.match(']'):
            self.context.advance()
            try:
                self.context.pop_bracket('[')
            except MismatchedBracketException as e:
                return is_eof, Token(TokenType.Error, position, f'Opening bracket was {e.expected}')
            else:
                return is_eof, Token(TokenType.RSquare, position)
        elif self.match('}'):
            self.context.advance()
            try:
                self.context.pop_bracket('{')
            except MismatchedBracketException as e:
                return is_eof, Token(TokenType.Error, position, f'Opening bracket was {e.expected}')
            else:
                return is_eof, Token(TokenType.RBrace, position)
        elif self.match('\n'):
            self.context.advance()
            return is_eof, Token(TokenType.Newline, position)

        elif self.current_in(digits):
            state = Number(self.context)
            return state()

        elif self.match('"'):
            state = String(self.context)
            return state()

        elif not self.current_in(RESERVED_CHARACTERS + list(digits)):
            state = Word(self.context)
            return state()


class Number(State):
    def consume_number(self, characters):
        value = self.append_while(characters)

        while self.match('_'):
            if self.next_in(characters):
                self.context.advance()
                value += self.append_while(characters)
            else:
                raise InvalidNumberInputException

        return value

    def read_number(self):
        if self.match('0') and self.match_next('x'):
            self.context.advance()
            self.context.advance()
            return '0x' + self.consume_number(hexdigits)
        elif self.match('0') and self.match_next('b'):
            self.context.advance()
            self.context.advance()
            return '0b' + self.consume_number(['0', '1'])
        elif self.match('0') and self.match_next('o'):
            self.context.advance()
            self.context.advance()
            return '0o' + self.consume_number(octdigits)
        elif self.current_in(digits):
            return self.consume_number(digits)
        else:
            raise InvalidNumberInputException

    def __call__(self):
        position = self.context.current_position

        try:
            first_number = self.read_number()
        except InvalidNumberInputException:
            return IsEOF(self.context), Token(TokenType.Error, position)

        if self.match('.') and self.next_in(digits):
            self.context.advance()
            try:
                second_number = self.read_number()
            except InvalidNumberInputException:
                return IsEOF(self.context), Token(TokenType.Error, position)

            value = first_number + '.' + second_number
            return IsEOF(self.context), Token(TokenType.Float, position, value)
        elif self.match('.') and not self.next_in(digits):
            return IsEOF(self.context), Token(TokenType.Integer, position, first_number)
        else:
            return IsEOF(self.context), Token(TokenType.Integer, position, first_number)


class String(State):
    ESCAPE_CHARS = {
        '0': '\0',
        'a': '\a',
        'b': '\b',
        'f': '\f',
        'n': '\n',
        'r': '\r',
        't': '\t',
        'v': '\v',
        '\\': '\\',
        '"': '"',
    }

    def __call__(self):
        position = self.context.current_position

        self.context.advance()

        value = ''
        while not self.eof:
            if self.match('"'):
                self.context.advance()
                return IsEOF(self.context), Token(TokenType.String, position, value)
            elif self.current_in(NEWLINE):
                return IsEOF(self.context), Token(TokenType.Error, self.context.current_position)
            elif self.match('\\'):
                # Expect a escape character
                self.context.advance()
                if self.current_in(self.ESCAPE_CHARS.keys()):
                    value += self.ESCAPE_CHARS[self.context.current]
                    self.context.advance()
                else:
                    return (
                        IsEOF(self.context),
                        Token(TokenType.Error, self.context.current_position, 'Unknown escape character')
                    )
            else:
                value += self.context.current
                self.context.advance()

        if self.eof:
            return IsEOF(self.context), Token(TokenType.Error, position)


class Word(State):
    def __call__(self):
        position = self.context.current_position
        value = self.append_while_not(RESERVED_CHARACTERS)
        is_eof = IsEOF(self.context)

        if value == 'func':
            return is_eof, Token(TokenType.Function, position, value)
        elif value == 'struct':
            return is_eof, Token(TokenType.Struct, position, value)
        elif value == 'if':
            return is_eof, Token(TokenType.If, position, value)
        elif value == 'elif':
            return is_eof, Token(TokenType.ElseIf, position, value)
        elif value == 'else':
            return is_eof, Token(TokenType.Else, position, value)
        elif value == 'while':
            return is_eof, Token(TokenType.While, position, value)
        elif value == 'for':
            return is_eof, Token(TokenType.ForEach, position, value)
        elif value == 'and':
            return is_eof, Token(TokenType.And, position, value)
        elif value == 'not':
            return is_eof, Token(TokenType.Not, position, value)
        elif value == 'or':
            return is_eof, Token(TokenType.Or, position, value)
        elif value == 'true':
            return is_eof, Token(TokenType.True_, position, value)
        elif value == 'false':
            return is_eof, Token(TokenType.False_, position, value)
        elif value == 'return':
            return is_eof, Token(TokenType.Return, position, value)
        else:
            return is_eof, Token(TokenType.Identifier, position, value)


class FileEnd(State):
    def __call__(self):
        self.context.pop_indent()
        state = End(self.context)

        return state, Token(TokenType.Dedent, None)


class End(State):
    def __call__(self):
        raise StopIteration

