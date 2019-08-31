#!/usr/bin/env python3

from .lexer.token import TokenType
from .parse_tree import FunctionDecl, Function, Boolean, Integer, Float, Identifier, String, \
    UnaryExpression, ProductExpression, SumExpression, AssignmentExpression, \
    Branch


class ParserException(Exception):
    pass


class UnexpectedTokenError(ParserException):
    def __init__(self, expected=None, received=None, position=None, message=None):
        self.expected = expected
        self.received = received
        self.position = position
        self.message = message

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
            f'expected={repr(self.expected)}, ' \
            f'received={repr(self.received)}, ' \
            f'position={repr(self.position)}, ' \
            f'message={repr(self.message)}' \
            ')'

    def __str__(self):
        return repr(self)


class Parser:
    def __init__(self, lexer):
        self._lexer = iter(lexer)
        self.errors = []
        self._current = None
        self._next = None

        self.advance()
        self.advance()

    @property
    def current(self):
        return self._current

    @property
    def next(self):
        return self._next

    def match_current(self, token_type):
        return self.current and self.current.token_type == token_type

    def match_next(self, token_type):
        return self.current and self.next.token_type == token_type

    def match(self, current_type, next_type=None):
        return all([
            self.match_current(current_type),
            True if next_type is None else self.match_next(next_type)
        ])

    def advance(self):
        self._current = self._next
        try:
            self._next = next(self._lexer)
        except StopIteration:
            self._next = None

        return self.current

    def consume(self):
        current = self.current
        self.advance()

        return current

    def consume_if(self, token_type):
        if self.match(token_type):
            return self.consume()
        else:
            return None

    def consume_try(self, token_type):
        if self.match(token_type):
            return self.consume()
        else:
            raise UnexpectedTokenError(
                expected=token_type,
                received=self.current,
                message=f'Expected {token_type} and found {self.current}'
            )

    def eof(self):
        return self.current is None and self.next is None

    def recover(self, skip_to_next_token=TokenType.Newline):
        while not self.match_next(skip_to_next_token) and \
                not self.eof():
            self.advance()

    def parse(self):
        try:
            return self.start()
        except ParserException:
            print('Irrecoverable error occurred when parsing')

    def start(self):
        return self.block()

    def parameters(self):
        params = [self.identifier()]

        while self.consume_if(TokenType.Comma):
            params.append(self.identifier())

        return params

    def function_decl(self):
        self.consume_try(TokenType.Function)
        name = self.identifier()

        self.consume_try(TokenType.LParen)
        parameters = []
        try:
            parameters = self.parameters()
        except UnexpectedTokenError:
            pass
        self.consume_try(TokenType.RParen)

        if self.consume_if(TokenType.Colon):
            return_type = self.identifier()
            return FunctionDecl(name, parameters, return_type)
        else:
            return FunctionDecl(name, parameters, None)

    def function(self):
        definition = self.function_decl()

        self.consume_try(TokenType.Assignment)
        self.consume_try(TokenType.Newline)

        statements = self.block()

        return Function(definition, statements)

    def block(self):
        statements = []

        self.consume_try(TokenType.Indent)
        while not self.match(TokenType.Dedent):
            statements.append(self.statement())
        self.consume_try(TokenType.Dedent)

        return statements

    def if_statement(self):
        if self.match(TokenType.If) or self.match(TokenType.ElseIf):
            self.consume()
        condition = self.expression()

        self.consume_if(TokenType.Colon)
        self.consume_if(TokenType.Newline)

        then_block = self.block()

        if self.match(TokenType.ElseIf):
            else_block = self.if_statement()
            return Branch(condition, then_block, else_block)
        elif self.consume_if(TokenType.Else):
            self.consume_try(TokenType.Colon)
            self.consume_try(TokenType.Newline)
            else_block = self.block()

            return Branch(condition, then_block, else_block)
        else:
            return Branch(condition, then_block, [])

    def statement(self):
        if self.match(TokenType.Function):
            return self.function()
        elif self.match(TokenType.If):
            return self.if_statement()
        else:
            expr = self.expression()
            self.consume_try(TokenType.Newline)

            return expr

    def expression(self):
        return self.assignment_expr()

    def assignment_expr(self):
        left = self.sum_expr()
        if self.match(TokenType.Assignment):
            operator = self.consume()
            right = self.expression()
            return AssignmentExpression(left, operator, right)
        else:
            return left

    def sum_expr(self):
        left = self.product_expr()

        operator = self.consume_if(TokenType.Plus) or self.consume_if(TokenType.Minus)
        if operator:
            right = self.expression()
            return SumExpression(left, operator, right)
        else:
            return left

    def product_expr(self):
        left = self.unary_expr()
        if self.match(TokenType.Multiply) or self.match(TokenType.Divide) or self.match(TokenType.Modulo):
            operator = self._current
            self.advance()
            right = self.expression()
            return ProductExpression(left, operator, right)
        else:
            return left

    def unary_expr(self):
        operation = self.consume_if(TokenType.Minus)
        if operation:
            expression = self.expression()
            return UnaryExpression(operation, expression)
        else:
            return self.atom()

    def atom(self):
        try:
            return self.float()
        except UnexpectedTokenError:
            pass

        try:
            return self.integer()
        except UnexpectedTokenError:
            pass

        try:
            return self.bool()
        except UnexpectedTokenError:
            pass

        try:
            return self.identifier()
        except UnexpectedTokenError:
            pass

        if self._current.token_type == TokenType.LParen:
            self.advance()
            expr = self.expression()
            if self._current.token_type == TokenType.RParen:
                return expr
            else:
                raise UnexpectedTokenError

        raise UnexpectedTokenError

    def bool(self):
        try:
            return Boolean(self.consume_try(TokenType.True_))
        except UnexpectedTokenError:
            return Boolean(self.consume_try(TokenType.False_))

    def integer(self):
        return Integer(value=self.consume_try(TokenType.Integer))

    def float(self):
        return Float(value=self.consume_try(TokenType.Float))

    def identifier(self):
        return Identifier(value=self.consume_try(TokenType.Identifier))

    def string(self):
        return String(value=self.consume_try(TokenType.String))
