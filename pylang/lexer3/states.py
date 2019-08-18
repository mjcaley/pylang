#!/usr/bin/env python3

from string import digits, hexdigits, octdigits

from .characters import INDENT, NEWLINE, WHITESPACE
from .exceptions import MismatchedBracketException
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
        while self.context.current in characters or not self.context.current:
            self.context.advance()

    def skip_whitespace(self):
        self.skip_while(WHITESPACE)

    def skip_empty_lines(self):
        # Weird implementation, might not work
        while self.context.current and self.match_next(NEWLINE):
            self.skip_while(NEWLINE)
            self.append_while(WHITESPACE + INDENT)

    def match(self, character):
        return character == self.context.current

    def match_next(self, character):
        return character == self.context.next

    def current_in(self, characters):
        return all([self.context.current in characters, self.context.current])

    def next_in(self, characters):
        return all([self.context.next in characters, self.context.next])

    def __call__(self):
        raise NotImplementedError


class Start(State):
    def __call__(self):
        state = FileStart(self.context)

        return state()


class FileStart(State):
    def __call__(self):
        return Operators(self.context), Token(TokenType.Indent, None)


class Operators(State):
    def __call__(self):
        position, character = self.context.advance()

        if not self.context.current:
            state = FileEnd(self.context)
            return state()

        if self.match('+'):
            if self.match_next('='):
                self.context.advance()
                return self, Token(TokenType.PlusAssign, position)
            return self, Token(TokenType.Plus, self.context.current_position)
        elif self.match('-'):
            if self.match_next('='):
                self.context.advance()
                return self, Token(TokenType.MinusAssign, position)
            return self, Token(TokenType.Minus, position)
        elif self.match('*'):
            if self.match_next('='):
                self.context.advance()
                return self, Token(TokenType.MultiplyAssign, position)
            elif self.match_next('*'):
                position = self.context.current_position
                self.context.advance()
                if self.match_next('='):
                    self.context.advance()
                    return self, Token(TokenType.ExponentAssign, position)
                else:
                    return self, Token(TokenType.Exponent, position)
            else:
                return self, Token(TokenType.Multiply, position)
        elif self.match('/'):
            if self.match_next('='):
                self.context.advance()
                return self, Token(TokenType.DivideAssign, position)
            return self, Token(TokenType.Divide, position)
        elif self.match('%'):
            if self.match_next('='):
                self.context.advance()
                return self, Token(TokenType.ModuloAssign, position)
            return self, Token(TokenType.Modulo, position)
        elif self.match('='):
            if self.match_next('='):
                self.context.advance()
                return self, Token(TokenType.Equal, position)
            else:
                return self, Token(TokenType.Assignment, position)
        elif self.match('!'):
            if self.match_next('='):
                self.context.advance()
                return self, Token(TokenType.NotEqual, position)
            else:
                return self, Token(TokenType.Error, position)
        elif self.match('<'):
            if self.match_next('='):
                self.context.advance()
                return self, Token(TokenType.LessThanOrEqual, position)
            else:
                return self, Token(TokenType.LessThan, position)
        elif self.match('>'):
            if self.match_next('='):
                self.context.advance()
                return self, Token(TokenType.GreaterThanOrEqual, position)
            else:
                return self, Token(TokenType.GreaterThan, position)
        elif self.match('.'):
            return self, Token(TokenType.Dot, position)
        elif self.match(':'):
            return self, Token(TokenType.Colon, position)
        elif self.match(','):
            return self, Token(TokenType.Comma, position)

        elif self.match('('):
            self.context.push_bracket(character)
            return self, Token(TokenType.LParen, position)
        elif self.match('['):
            self.context.push_bracket(character)
            return self, Token(TokenType.LSquare, position)
        elif self.match('{'):
            self.context.push_bracket(character)
            return self, Token(TokenType.LBrace, position)
        elif self.match(')'):
            try:
                self.context.pop_bracket('(')
            except MismatchedBracketException as e:
                return self, Token(TokenType.Error, position, f'Opening bracket was {e.expected}')
            else:
                return self, Token(TokenType.RParen, position)
        elif self.match(']'):
            try:
                self.context.pop_bracket('[')
            except MismatchedBracketException as e:
                return self, Token(TokenType.Error, position, f'Opening bracket was {e.expected}')
            else:
                return self, Token(TokenType.RSquare, position)
        elif self.match('}'):
            try:
                self.context.pop_bracket('{')
            except MismatchedBracketException as e:
                return self, Token(TokenType.Error, position, f'Opening bracket was {e.expected}')
            else:
                return self, Token(TokenType.RBrace, position)


class Number(State):
    def __call__(self):
        number = self.append_while(digits)
        return Operators(self.context), Token(TokenType.Integer, number)


class FileEnd(State):
    def __call__(self):
        state = End(self.context)

        return state, Token(TokenType.Dedent, None)


class End(State):
    def __call__(self):
        raise StopIteration

