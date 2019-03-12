#!/usr/bin/env python3

from .lexer import TokenType
from .parse_tree import Start, Function


class ParserException(Exception):
    pass


class UnexpectedToken(ParserException):
    pass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = []
        self.token = None

    def consume(self, expected_token_type):
        pass

    def not_eof(self):
        return self.token.token_type != TokenType.EOF

    def report_error(self, message, token):
        self.errors.append(ParserException(message, token))

    def recover(self, skip_to_next_token=TokenType.Newline):
        while self.lexer.next_token.token_type != skip_to_next_token and \
              self.lexer.next_token.token_type != TokenType.EOF:
            self.token = self.lexer.emit()

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
