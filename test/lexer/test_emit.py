#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer, TokenType


@pytest.mark.parametrize('test_input,token_type', [
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

    ['=', TokenType.Assignment],

    ['==', TokenType.Equal],
    ['!=', TokenType.NotEqual],
    ['<', TokenType.LessThan],
    ['<=', TokenType.LessThanOrEqual],
    ['>', TokenType.GreaterThan],
    ['>=', TokenType.GreaterThanOrEqual],
])
def test_operators(test_input, token_type):
    l = Lexer(test_input)
    l.emit()
    result = l.emit()

    assert token_type == result.token_type


@pytest.mark.parametrize('test_input,expected', [
    ['\r', TokenType.Newline],
    ['\n', TokenType.Newline],
    ['\r\n', TokenType.Newline],
    ['.', TokenType.Dot],
    [':', TokenType.Colon],
    [',', TokenType.Comma]
])
def test_emit_other_operators(test_input, expected):
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


@pytest.mark.parametrize('test_input,expected', [
    ['42', TokenType.Integer],
    ['42.42', TokenType.Float],
    ['.42', TokenType.Float]
])
def test_emit_numbers(test_input, expected):
    l = Lexer(test_input)
    l.emit()
    token = l.emit()

    assert expected == token.token_type


def test_emit_error():
    l = Lexer('!')
    l.emit()
    result = l.emit()

    assert TokenType.Error == result.token_type


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


@pytest.mark.parametrize('test_input,expected', [
    ['abc+', 'abc'],
    ['abc-', 'abc'],
    ['abc*', 'abc'],
    ['abc/', 'abc'],
    ['abc%', 'abc'],
    ['abc(', 'abc'],
    ['abc)', 'abc'],
    ['abc[', 'abc'],
    ['abc]', 'abc'],
    ['abc{', 'abc'],
    ['abc}', 'abc'],
    ['abc,', 'abc'],
    ['abc=', 'abc'],
    ['abc:', 'abc'],
    ['abc<', 'abc'],
    ['abc>', 'abc']
])
def test_identifier_doesnt_consume_operators(test_input, expected):
    l = Lexer(test_input)
    l.emit()

    assert expected == l.emit().value


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
    ['42', 3],
    ['42\n', 4],
    ['\t42\n42', 7]
])
def test_eof(test_input, num_tokens):
    l = Lexer(test_input)

    for token in range(num_tokens):
        assert TokenType.EOF != l.emit()

    assert TokenType.EOF == l.emit().token_type
