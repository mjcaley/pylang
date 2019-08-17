#!/usr/bin/env python3

from pylang.lexer3.context import Context
from pylang.lexer3.lexer import Lexer
from pylang.lexer3.states import Start


def test_from_stream():
    l = Lexer.from_stream('123')

    assert isinstance(l, Lexer)
    assert isinstance(l.state, Start)


def test_iter(mocker):
    l = Lexer(start_state=mocker.stub())
    iterator = iter(l)

    assert 'iterator' in locals()


def test_next(mocker):
    state = mocker.stub(name='new state')
    token = mocker.stub(name='token')

    l = Lexer(
        start_state=mocker.Mock(return_value=(state, token))
    )
    result = next(l)

    assert result == token
    assert l.state == state


def test_state(mocker):
    l = Lexer(start_state=mocker.stub())
    state = mocker.stub()
    l.state = state

    assert l.state == state
