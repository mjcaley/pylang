#!/usr/bin/env python3


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


class InvalidNumberInputException(LexerException):
    pass
