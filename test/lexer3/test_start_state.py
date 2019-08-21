#!/usr/bin/env python3

from pylang.lexer3.states import Start


def test_call_to_file_start(context, mocker):
    s = Start(context=context(''))
    mocked_indent = mocker.patch('pylang.lexer3.states.FileStart')
    called_instance = mocked_indent()()
    result = s()

    assert result == called_instance
