#!/usr/bin/env python3

from enum import Enum

from lark import Lark, Token


PYLANG_GRAMMAR = '''
    start: statement+
    
    statement: expr ";"
    
    ?expr:   binary_expr
    binary_expr:    sum_expr
    ?sum_expr:   mul_expr
                | mul_expr (ADD_OP | SUB_OP) expr
    ?mul_expr:   atom
                | atom (MUL_OP | DIV_OP) expr
    ?integer: INT
    ?float: DECIMAL
    ?atom:   integer
            | float
            | "(" expr ")"
    
    ADD_OP: "+"
    SUB_OP: "-"
    MUL_OP: "*"
    DIV_OP: "/"
    PAREN_L: "("
    PAREN_R: ")"
    
    BOOL_TRUE: "true"
    BOOL_FALSE: "false"
    
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


parser = Lark(
    PYLANG_GRAMMAR,
    # parser='lalr',
    # lexer_callbacks={
    #     'NUMBER': integer_literal,
    #
    #     'ADD_OP': operator_to_enum,
    #     'SUB_OP': operator_to_enum,
    #     'MUL_OP': operator_to_enum,
    #     'DIV_OP': operator_to_enum,
    #
    #     'ASSIGN_OP': operator_to_enum,
    # }
)
