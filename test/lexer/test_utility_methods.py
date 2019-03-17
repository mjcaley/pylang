#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer, Position, TokenType


@pytest.mark.parametrize('test_input', [
    'abc',
    b'abc'
])
def test_init_data(test_input):
    l = Lexer(test_input)

    assert 'l' in locals()


def test_init_file(tmpdir):
    from pathlib import Path
    file = Path(tmpdir) / 'file.txt'
    file.touch()

    with open(file) as f:
        l = Lexer(f)
        assert 'l' in locals()


def test_advance_empty_string():
    l = Lexer('')

    character = l.advance()

    assert '' == character
    assert Position(index=0, line=1, column=1) == l.next_position


def test_advance_no_newline():
    l = Lexer('abc')

    character = l.advance()
    assert 'a' == character
    assert Position(index=1, line=1, column=2)

    character = l.advance()
    assert 'b' == character
    assert Position(index=2, line=1, column=3)

    character = l.advance()
    assert 'c' == character
    assert Position(index=3, line=1, column=4)


def test_advance_windows_newline():
    l = Lexer('a\r\nb')

    l.advance()
    l.advance()
    character = l.advance()

    assert '\n' == character
    assert 'b' == l.next
    assert Position(index=3, line=2, column=1) == l.next_position


def test_advance_unix_newline():
    l = Lexer('a\nb')

    l.advance()
    character = l.advance()

    assert '\n' == character
    assert 'b' == l.next
    assert Position(index=2, line=2, column=1) == l.next_position


def test_advance_mac_newline():
    l = Lexer('a\rb')

    l.advance()
    character = l.advance()

    assert '\r' == character
    assert 'b' == l.next
    assert Position(index=2, line=2, column=1) == l.next_position


def test_append():
    l = Lexer('abc')

    assert '' == l.current
    l.append()
    assert 'a' == l.current


def test_append_while():
    l = Lexer('aaabc')
    l.append_while('a')

    assert 'aaa' == l.current


def test_append_while_multiple():
    from string import ascii_lowercase
    l = Lexer('abc123')
    l.append_while(ascii_lowercase)

    assert 'abc' == l.current


def test_consume():
    l = Lexer('abc')
    l.append()
    l.append()
    l.append()

    result = l.consume()
    assert 'abc' == result
    assert '' == l.current


def test_skip():
    l = Lexer('    ')
    l.skip()

    assert '' == l.current
    assert Position(index=4, line=1, column=5) == l.next_position


@pytest.mark.parametrize('test_input,character,expected', [
    ['a', 'a', True],
    ['a', 'b', False]
])
def test_match(test_input, character, expected):
    l = Lexer(test_input)
    l.append()

    assert expected is l.match(character)


def test_match_next():
    l = Lexer('abc')

    assert l.match_next('a')


def test_match_next_multiple():
    from string import ascii_lowercase
    l = Lexer('abc')

    assert l.match_next(ascii_lowercase)


def test_skip_until():
    l = Lexer('aaabc')
    l.skip_until('b')

    assert '' == l.current
    assert 'b' == l.next


def test_skip_while():
    l = Lexer('aaabc')
    l.skip_while('a')

    assert '' == l.current
    assert 'b' == l.next


@pytest.mark.parametrize('test_input,position', [
    ['    \n', Position(index=5, line=2, column=1)],
    [' \n \n', Position(index=4, line=3, column=1)]
])
def test_skip_empty_lines(test_input, position):
    l = Lexer(test_input)
    l.append_while(l.INDENT)
    l.skip_empty_lines()

    assert l.next_position == position


def test_contains_true():
    from string import ascii_lowercase
    l = Lexer('abcdef')
    l.append()

    assert l.contains(ascii_lowercase)


def test_contains_false():
    from string import digits
    l = Lexer('abcdef')
    l.append()

    assert not l.contains(digits)


def test_next_contains_true():
    from string import digits
    l = Lexer('a123')
    l.append()

    assert l.next_contains(digits)


def test_next_contains_false():
    from string import digits
    l = Lexer('abc')
    l.append()

    assert not l.next_contains(digits)


@pytest.mark.parametrize('test_input,expected', [
    ['(', TokenType.LParen],
    ['[', TokenType.LSquare],
    ['{', TokenType.LBrace]
])
def test_push_bracket(test_input, expected):
    l = Lexer(test_input)
    result = l.push_bracket(expected)

    assert expected == result.token_type


def test_pop_bracket():
    l = Lexer('')
    l.push_bracket('left')
    l.pop_bracket('left', 'right')

    assert 'right' == l.token.token_type


def test_pop_bracket_wrong_right_bracket():
    l = Lexer('')
    l.push_bracket(TokenType.LParen)
    l.pop_bracket(TokenType.LSquare, TokenType.RSquare)

    assert TokenType.Error == l.token.token_type
    assert TokenType.RSquare == l.token.value


def test_pop_bracket_extra_right_bracket():
    l = Lexer('')
    l.pop_bracket(TokenType.LParen, TokenType.RParen)

    assert TokenType.Error == l.token.token_type
    assert TokenType.RParen == l.token.value


def test_new_token():
    from pylang.lexer import TokenType
    l = Lexer('123')
    l.append()
    l.append()
    l.append()
    l.new_token(
        token_type=TokenType.Integer,
        value=l.consume()
    )

    assert TokenType.Integer == l.token.token_type
    assert '123' == l.token.value
    assert Position(
        index=0,
        line=1,
        column=1
    ) == l.token.position
