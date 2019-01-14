#!/usr/bin/env python3

from lark import Lark


GRAMMAR = '''
    start: statement+
    
    statement: _expr ";"
    
    _expr:   binary_expr
    ?binary_expr:    _sum_expr
    _sum_expr:  _prod_expr
                | _prod_expr ADD_OP _expr
                | _prod_expr SUB_OP _expr
    _prod_expr: unary_expr
                | unary_expr MUL_OP _expr
                | unary_expr DIV_OP _expr
    ?unary_expr:    NEGATIVE_OP unary_expr
                    | NOT_OP unary_expr
                    | atom
    integer: INT
    float: DECIMAL
    bool: [TRUE | FALSE]
    ?atom:  integer
            | float
            | bool
            | _PAREN_L _expr _PAREN_R
    
    ADD_OP: "+"
    SUB_OP: "-"
    MUL_OP: "*"
    DIV_OP: "/"
    _PAREN_L: "("
    _PAREN_R: ")"
    NEGATIVE_OP: "-"
    NOT_OP: "!"
    
    TRUE: "true"
    FALSE: "false"
    
    NULL: "null"
    
    %import common.WORD
    %import common.INT
    %import common.DECIMAL
    %ignore " "
'''


parser = Lark(GRAMMAR, parser='lalr')
