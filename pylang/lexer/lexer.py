#!/usr/bin/env python3

from typing import Callable

from .context import Context
from .states import Start
from .stream import Stream


class Lexer:
    def __init__(self, start_state: Callable):
        self._state = start_state

    @classmethod
    def from_stream(cls, data):
        context = Context(Stream(data))
        state = Start(context)

        return cls(state)

    def __iter__(self):
        return self

    def __next__(self):
        self.state, token = self.state()

        return token

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state
