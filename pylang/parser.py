#!/usr/bin/env python3

from enum import Enum

from lark import Lark, Token


GRAMMAR = '''
    start: statement+
    
    statement: _expr ";"
    
    _expr:   binary_expr
    ?binary_expr:    _sum_expr
    _sum_expr:   _prod_expr
                | _prod_expr ADD_OP _expr
                | _prod_expr SUB_OP _expr
    _prod_expr:   unary_expr
                | unary_expr MUL_OP _expr
                | unary_expr DIV_OP _expr
    ?unary_expr:    NEGATIVE_OP unary_expr
                    | NOT_OP unary_expr
                    | _atom
    _atom:   integer
            | float
            | true
            | false
            | _PAREN_L _expr _PAREN_R
    integer:    INT
    float:      DECIMAL
    true:   TRUE
    false:  FALSE
    
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


class Operator(Enum):
    Add = '+'
    Subtract = '-'
    Multiply = '*'
    Divide = '/'

    Assign = '='


def operator_to_enum(token):
    return Token.new_borrow_pos(token.type, Operator(token), token)


def integer_literal(token):
    return Token.new_borrow_pos(token.type, int(token), token)


def float_literal(token):
    return Token.new_borrow_pos(token.type, float(token), token)


parser = Lark(GRAMMAR)
