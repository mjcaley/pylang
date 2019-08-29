#!/usr/bin/env python3

import pytest

from pylang.lexer.states import End


def test_raise_stop_iteration():
    e = End(None)

    with pytest.raises(StopIteration):
        e()