#!/usr/bin/env python3

from lark import Lark


PYLANG_GRAMMAR = '''
    start: NUMBER
    
    ADD_OP: "+"
    SUB_OP: "-"
    MUL_OP: "*"
    DIV_OP: "/"
    PAREN_L: "("
    PAREN_R: ")"
    
    %import common.WORD
    %import common.NUMBER
    %ignore " "
'''

parser = Lark(PYLANG_GRAMMAR)

print(parser.parse("42"))
