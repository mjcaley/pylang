#!/usr/bin/env python3

from typing import Iterator

from .exceptions import MismatchedBracketException, MismatchedIndentException


class Context:
    def __init__(self, stream: Iterator):
        self._stream = stream

        self._indents = []
        self._brackets = []

        self._current = ''
        self._current_position = None

        self._next = ''
        self._next_position = None

    @property
    def indent(self):
        return self._indents[-1]

    def push_indent(self, length):
        if self._indents:
            top = self._indents[-1]
            if top > length:
                raise MismatchedIndentException
        self._indents.append(length)

    def pop_indent(self):
        try:
            return self._indents.pop()
        except IndexError:
            raise MismatchedIndentException

    def push_bracket(self, bracket):
        self._brackets.append(bracket)

    def pop_bracket(self, expected):
        top = self._brackets.pop()
        if top != expected:
            raise MismatchedBracketException(expected=expected, found=top)
        else:
            return top

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

    def advance(self):
        self._current_position, self._current = self._next_position, self._next
        self._next_position, self._next = next(self._stream)

        return self._current_position, self._current
