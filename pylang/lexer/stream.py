#!/usr/bin/env python3

from collections import namedtuple
from io import BytesIO, StringIO, TextIOWrapper


Character = namedtuple('Character', ['position', 'character'])
Position = namedtuple('Position', ['index', 'line', 'column'])


class Stream:
    def __init__(self, data):
        if type(data) == str:
            self._data = StringIO(data, newline=None)
        elif type(data) == bytes:
            self._data = TextIOWrapper(BytesIO(data), encoding='utf-8', newline=None)
        else:
            self._data = data

        self._position = Position(index=-1, line=1, column=0)

    def __iter__(self):
        return self

    def __next__(self):
        character = self._data.read(1)

        if character == '':
            return Character(None, character)
        elif character == '\n':
            position = Position(
                index=self._position.index + 1,
                line=self._position.line,
                column=self._position.column + 1)
            self._position = Position(
                index=position.index,
                line=position.line + 1,
                column=0)
            return Character(position, character)
        else:
            self._position = Position(
                index=self._position.index + 1,
                line=self._position.line,
                column=self._position.column + 1)

        return Character(self._position, character)
