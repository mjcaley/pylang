#!/usr/bin/env python3

from enum import Enum

from lark import Lark, Token


GRAMMAR = '''
    start: statement+
    
    statement: expr ";"
    
    expr:   binary_expr
    binary_expr:    _sum_expr
    _sum_expr:   _mul_expr
                | _mul_expr ADD_OP expr
                | _mul_expr SUB_OP expr
    _mul_expr:   unary_expr
                | unary_expr MUL_OP expr
                | unary_expr DIV_OP expr
    ?unary_expr:    NEGATIVE_OP unary_expr
                    | NOT_OP unary_expr
                    | atom
    atom:   INT         -> integer
            | DECIMAL   -> float
            | TRUE      -> true
            | FALSE     -> false
            | PAREN_L expr PAREN_R
    
    ADD_OP: "+"
    SUB_OP: "-"
    MUL_OP: "*"
    DIV_OP: "/"
    PAREN_L: "("
    PAREN_R: ")"
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
