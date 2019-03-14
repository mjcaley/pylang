#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer, Position, TokenType


@pytest.mark.parametrize('test_input', [
    'string',
    'bytes'.encode('utf-8')
])
def test_init_string(test_input):
    l = Lexer(test_input)

    assert 'l' in locals()


def test_init_file(tmp_path):
    from pathlib import Path
    p = Path(tmp_path) / 'example.pylang'
    p.write_text('string', 'utf-8')
    with open(p) as file:
        l = Lexer(file)

    assert 'l' in locals()


def test_init_variables():
    l = Lexer('string')

    assert l.next_token.token_type == TokenType.Start
    assert l.current == ''
    assert l.next == 's'
    assert l.start_pos == Position(0, 1, 1)
    assert l.end_pos == Position(0, 1, 1)
    assert l.beginning is True
    assert l.indents == [0]
    assert l.brackets == []


def test_increment_position():
    l = Lexer('string')

    assert l.start_pos == Position(index=0, line=1, column=1)
    assert l.end_pos == Position(index=0, line=1, column=1)
    l.increment_position()
    assert l.end_pos == Position(index=1, line=1, column=2)


def test_discard_current():
    l = Lexer('string')
    l.current = 'string'
    l.discard_current()

    assert l.current == ''


def test_append_to_current():
    l = Lexer('string')

    assert l.current == ''
    l.append_to_current()
    assert l.current == 's'


def test_set_token_default():
    l = Lexer('string')
    l.append_to_current()
    l.set_token(TokenType.Identifier)

    assert '' == l.current
    assert TokenType.Identifier == l.next_token.token_type
    assert 's' == l.next_token.value
    assert Position(0, 1, 1) == l.next_token.start_position
    assert Position(1, 1, 2) == l.next_token.end_position


def test_set_token_with_arguments():
    l = Lexer('42')
    l.append_to_current()
    l.set_token(TokenType.Integer, cast_func=int, clobber=False)

    assert '4' == l.current
    assert TokenType.Integer == l.next_token.token_type
    assert 4 == l.next_token.value
    assert Position(index=0, line=1, column=1) == l.next_token.start_position
    assert Position(index=1, line=1, column=2) == l.next_token.end_position


@pytest.mark.parametrize('test_input,start_position,end_position', [
    ['\n', Position(index=1, line=2, column=1), Position(index=1, line=2, column=1)],
    ['\r', Position(index=1, line=2, column=1), Position(index=1, line=2, column=1)],
    ['\r\n', Position(index=2, line=2, column=1), Position(index=2, line=2, column=1)]
])
def test_newline(test_input, start_position, end_position):
    l = Lexer(test_input)
    l.beginning = False

    assert Position(index=0, line=1, column=1) == l.start_pos
    assert False is l.beginning
    l.emit()
    assert start_position == l.start_pos
    assert end_position == l.end_pos
    assert True is l.beginning


def test_skip():
    l = Lexer('\v\f \u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008'
              '\u2009\u200a\u2028\u2029\u202f\u205f\u3000\u180e\u200b\u200c\u200d\u2060\ufeff'
              'string')
    l.append_to_current()
    l.skip()

    assert Position(index=28, line=1, column=29) == l.start_pos


@pytest.mark.parametrize('test_input,expected', [
    ['\r', TokenType.Newline],
    ['\n', TokenType.Newline],
    ['\r\n', TokenType.Newline],
    ['42', TokenType.Integer],
    ['42.42', TokenType.Float],
    ['.42', TokenType.Float],
    ['.', TokenType.Dot],
    ['=', TokenType.Assignment],
    ['==', TokenType.Equal],
    ['!=', TokenType.NotEqual],
    ['>', TokenType.GreaterThan],
    ['>=', TokenType.GreaterThanOrEqual],
    ['<', TokenType.LessThan],
    ['<=', TokenType.LessThanOrEqual],
    ['+', TokenType.Plus],
    ['+=', TokenType.PlusAssign],
    ['-', TokenType.Minus],
    ['-=', TokenType.MinusAssign],
    ['*', TokenType.Multiply],
    ['*=', TokenType.MultiplyAssign],
    ['/', TokenType.Divide],
    ['/=', TokenType.DivideAssign],
    ['%', TokenType.Modulo],
    ['%=', TokenType.ModuloAssign],
    ['**', TokenType.Exponent],
    ['**=', TokenType.ExponentAssign],
    [':', TokenType.Colon],
    [',', TokenType.Comma]
])
def test_emit_token(test_input, expected):
    l = Lexer(test_input)
    l.emit()
    token = l.emit()

    assert expected == token.token_type


@pytest.mark.parametrize('test_input,l_token,r_token', [
    ['[]', TokenType.LSquare, TokenType.RSquare],
    ['{}', TokenType.LBrace, TokenType.RBrace],
    ['()', TokenType.LParen, TokenType.RParen],
])
def test_emit_brackets(test_input, l_token, r_token):
    l = Lexer(test_input)
    l.emit()

    assert l_token == l.emit().token_type
    assert r_token == l.emit().token_type


@pytest.mark.parametrize('test_input', [
    '[]',
    '{}',
    '()'
])
def test_bracket_stack(test_input):
    l = Lexer(test_input)

    assert 0 == len(l.brackets)
    l.emit()
    assert 1 == len(l.brackets)
    l.emit()
    assert 0 == len(l.brackets)


@pytest.mark.parametrize('test_input,expected', [
    ['func', TokenType.Function],
    ['struct', TokenType.Struct],
    ['if', TokenType.If],
    ['elif', TokenType.ElseIf],
    ['else', TokenType.Else],
    ['while', TokenType.While],
    ['for', TokenType.ForEach],
    ['and', TokenType.And],
    ['or', TokenType.Or],
    ['not', TokenType.Not],
    ['true', TokenType.True_],
    ['false', TokenType.False_]
])
def test_emit_keyword(test_input, expected):
    l = Lexer(test_input)
    l.emit()

    assert expected == l.emit().token_type


def test_identifier():
    l = Lexer('_abc123')
    l.emit()

    assert TokenType.Identifier == l.emit().token_type


@pytest.mark.parametrize('test_input', [
    '    42\n42',
    ' 42\n42',
    '\t42\n42'
])
def test_single_indent_and_dedent(test_input):
    l = Lexer(test_input)
    l.emit()

    assert TokenType.Indent == l.emit().token_type
    l.emit()    # ignore token
    assert TokenType.Newline == l.emit().token_type
    assert TokenType.Dedent == l.emit().token_type


@pytest.mark.parametrize('test_input', [
    '    42\n        42\n',
    ' 42\n  42\n',
    '\t42\n\t\t42\n'
])
def test_multilevel_indent_and_dedent(test_input):
    l = Lexer(test_input)
    l.emit()

    assert TokenType.Indent == l.emit().token_type
    l.emit()    # ignore token
    assert TokenType.Newline == l.emit().token_type
    assert TokenType.Indent == l.emit().token_type
    l.emit()    # ignore token
    assert TokenType.Newline == l.emit().token_type
    assert TokenType.Dedent == l.emit().token_type
    assert TokenType.Dedent == l.emit().token_type


@pytest.mark.parametrize('test_input,num_tokens', [
    ['42', 2],
    ['42\n', 3],
    ['\t42\n42', 6]
])
def test_eof(test_input, num_tokens):
    l = Lexer(test_input)

    for token in range(num_tokens):
        assert TokenType.EOF != l.emit()

    assert TokenType.EOF == l.emit().token_type
