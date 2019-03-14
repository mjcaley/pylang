#!/usr/bin/env python3

from .lexer import TokenType
from .parse_tree import Start, Function, Boolean, Integer, Float, Identifier, UnaryExpression


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

    def peek(self):
        return self.lexer.next_token

    def match(self, *token_types):
        for item in token_types:
            pass
            #TODO: finish

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

    def expression(self):
        return self.unary_expr()

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

        # TODO: parse parentheses expression

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

