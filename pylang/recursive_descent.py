#!/usr/bin/env python3

from .lexer import TokenType
from .parse_tree import Start, Function, Boolean, Integer, Float, Identifier, UnaryExpression, ProductExpression, \
    SumExpression, AssignmentExpression


class ParserException(Exception):
    pass


class UnexpectedToken(ParserException):
    pass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = []
        self.token = self.lexer.emit()

    def advance(self):
        self.token = self.lexer.emit()
        return self.token

    def consume(self):
        token = self.token
        self.advance()

        return token

    def peek(self):
        return self.lexer.next_token

    def match(self, *token_types):
        for item in token_types:
            pass
            # TODO: finish

    def not_eof(self):
        return self.token.token_type != TokenType.EOF

    def report_error(self, message, token):
        self.errors.append(ParserException(message, token))

    def recover(self, skip_to_next_token=TokenType.Newline):
        while self.peek().token_type != skip_to_next_token and \
                self.peek().token_type != TokenType.EOF:
            self.advance()

    def parse(self):
        try:
            return self.start()
        except ParserException:
            print('Irrecoverable error occurred when parsing')

    def start(self):
        functions = []
        self.token = self.lexer.emit()
        if self.token.token_type != TokenType.Start:
            raise ParserException('Could not find Start token')

        while self.not_eof():
            func_token = self.token
            try:
                functions.append(self.function())
            except ParserException:
                self.report_error('Unable to parse function', func_token)

        return Start(functions=functions)

    def function(self):
        pass

    def block(self):
        statements = []

        if self.token.token_type != TokenType.Indent:
            raise UnexpectedToken
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
            raise UnexpectedToken
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
        if self.token.token_type == TokenType.Plus or \
                self.token.token_type == TokenType.Minus:
            operator = self.token
            self.advance()
            right = self.expression()
            return SumExpression(left, operator, right)
        else:
            return left

    def product_expr(self):
        left = self.unary_expr()
        if self.token.token_type == TokenType.Multiply or \
                self.token.token_type == TokenType.Divide:
            operator = self.token
            self.advance()
            right = self.expression()
            return ProductExpression(left, operator, right)
        else:
            return left

    def unary_expr(self):
        if self.token.token_type == TokenType.Minus:
            operation = self.token
            self.advance()
            expression = self.expression()
            return UnaryExpression(operation, expression)
        else:
            return self.atom()

    def atom(self):
        try:
            return self.float()
        except UnexpectedToken:
            pass

        try:
            return self.integer()
        except UnexpectedToken:
            pass

        try:
            return self.bool()
        except UnexpectedToken:
            pass

        try:
            return self.identifier()
        except UnexpectedToken:
            pass

        if self.token.token_type == TokenType.LParen:
            self.advance()
            expr = self.expression()
            if self.token.token_type == TokenType.RParen:
                return expr
            else:
                raise UnexpectedToken

        raise UnexpectedToken

    def bool(self):
        if self.token.token_type == TokenType.True_:
            self.advance()
            return Boolean(True)
        elif self.token.token_type == TokenType.False_:
            self.advance()
            return Boolean(False)
        else:
            raise UnexpectedToken

    def integer(self):
        if self.token.token_type == TokenType.Integer:
            node = Integer(value=self.token.value)
            self.advance()
            return node
        else:
            raise UnexpectedToken

    def float(self):
        if self.token.token_type == TokenType.Float:
            node = Float(self.token.value)
            self.advance()
            return node
        else:
            raise UnexpectedToken

    def identifier(self):
        if self.token.token_type == TokenType.Identifier:
            node = Identifier(self.token.value)
            self.advance()
            return node
        else:
            raise UnexpectedToken
