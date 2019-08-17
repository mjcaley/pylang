#!/usr/bin/env python3

import pytest

from lexer3.stream import Stream

from io import StringIO


def test_iterator_returns_self():
    s = Stream('a')

    assert s is iter(s)


@pytest.mark.parametrize('test_input,expected', [
    ('a', 'a'),
    (b'a', 'a'),
    (StringIO('a'), 'a')
])
def test_first_character(test_input, expected):
    s = Stream(test_input)
    result = next(s)

    assert result.position.index == 0
    assert result.position.line == 1
    assert result.position.column == 1
    assert result.character == expected


@pytest.mark.parametrize('test_input', [
    'a', b'a', StringIO('a')
])
def test_eof(test_input):
    s = Stream(test_input)
    next(s)
    result = next(s)

    assert result.position is None
    assert result.character == ''


@pytest.mark.parametrize('test_input', [
    '\na',
    '\r\na',
    '\ra',
    b'\na',
    b'\r\na',
    b'\ra',
    StringIO('\na')
])
def test_newline(test_input):
    s = Stream(test_input)
    next(s)
    result = next(s)

    assert result.position.index == 1
    assert result.position.line == 2
    assert result.position.column == 1
    assert result.character == 'a'
