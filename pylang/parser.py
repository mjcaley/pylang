#!/usr/bin/env python3

from pathlib import Path

from lark import Lark


def grammar():
    with open(Path(__file__).parent / 'pylang.lark') as g:
        return g.read()


def parser():
    return Lark(grammar(), parser='lalr')
