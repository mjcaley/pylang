#!/usr/bin/env python3

from .lexer import TokenType
from .parse_tree import Block, FunctionDecl, Function, Boolean, Integer, Float, Identifier, UnaryExpression, ProductExpression, \
    SumExpression, AssignmentExpression


class ParserException(Exception):
    pass


class UnexpectedTokenError(ParserException):
    def __init__(self, expected=None, received=None, position=None, message=None):
        self.expected = expected
        self.received = received
        self.position = position
        self.message = message


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = []
        self.token = self.lexer.emit()

    def current(self):
        return self.token

    def next(self):
        return self.lexer.token

    def match_current(self, token_type):
        return self.current().token_type == token_type

    def match_next(self, token_type):
        return self.next().token_type == token_type

    def match(self, current_type, next_type=None):
        return all([
            self.match_current(current_type),
            True if next_type is None else self.match_next(next_type)
        ])

    def advance(self):
        self.token = self.lexer.emit()
        return self.token

    def consume(self):
        token = self.token
        self.advance()

        return token

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
                received=self.current().token_type,
                position=self.current().position,
                message=f'Found {self.current().token_type}:{self.current().token_type.value} '
                        f'and expected {token_type}{token_type.value} at '
                        f'position: {self.current().position}'
            )

    def eof(self):
        return self.match(TokenType.EOF)

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
        functions = []

        if self.token.token_type != TokenType.Indent:
            raise UnexpectedTokenError('Could not find Start token')
        self.consume()

        while not self.match(TokenType.Dedent):
            try:
                functions.append(self.function())
            except UnexpectedTokenError:
                self.recover(TokenType.Function)
        self.consume()

        return functions

    def parameters(self):
        params = [self.identifier()]

        while self.token.token_type == TokenType.Comma:
            self.advance()
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

        if self.token.token_type != TokenType.Assignment:
            raise UnexpectedTokenError
        self.advance()
        if self.token.token_type != TokenType.Newline:
            raise UnexpectedTokenError
        self.advance()

        statements = self.block()

        return Function(definition, statements)

    def block(self):
        statements = []

        if self.token.token_type != TokenType.Indent:
            raise UnexpectedTokenError
        self.advance()
        while self.token.token_type != TokenType.Dedent and \
                self.token.token_type != TokenType.EOF:
            statements.append(self.statement())
        if self.token.token_type == TokenType.Dedent:
            self.advance()

        return statements

    def statement(self):
        expr = self.expression()
        if self.token.token_type == TokenType.Newline:
            self.advance()
        else:
            raise UnexpectedTokenError
        return expr

    def expression(self):
        return self.assignment_expr()

    def assignment_expr(self):
        left = self.sum_expr()
        if self.token.token_type == TokenType.Assignment:
            operator = self.token
            self.advance()
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
        if self.match(TokenType.Multiply) or self.match(TokenType.Divide):
            operator = self.token
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

        if self.token.token_type == TokenType.LParen:
            self.advance()
            expr = self.expression()
            if self.token.token_type == TokenType.RParen:
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
        return Integer(value=self.consume_try(TokenType.Digits))

    def float(self):
        if self.match(TokenType.Dot, TokenType.Digits):
            start = self.consume()
            right = self.consume()
            start.value = float('0.' + str(right.value))

            return Float(value=start)
        elif self.match(TokenType.Digits, TokenType.Dot):
            start = self.consume()
            self.consume()
            right = self.consume_try(TokenType.Digits)
            start.value = float(str(start.value) + '.' + str(right.value))

            return Float(value=start)
        else:
            raise UnexpectedTokenError(expected=TokenType.Digits, received=self.current())

    def identifier(self):
        return Identifier(value=self.consume_try(TokenType.Identifier))
