#!/usr/bin/env python3

import pytest

from pylang.lexer import Lexer


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
