#!/usr/bin/env python3

from pylang import parser, pylang_ast as ast
from pylang.interpreter import OperatorToEnum, ToLiteral


def test_parser():
    program = '12 + 24;'

def test_ast_printer():
    program = '12 + 24;'

    p = parser.parser
    parse_tree = p.parse(program)
    print(parse_tree)
    m = ast.ToAST()
    abtract_syntax_tree = m.transform(parse_tree)

    a = ast.ASTPrinter()
    a.visit(abtract_syntax_tree)

def test_operator_to_enum():
    program = '1 + 2;'

    p = parser.parser
    parse_tree = p.parse(program)
    print(parse_tree)
    o = OperatorToEnum()
    tree = o.transform(parse_tree)
    print(tree)


def test_to_literal():

    program = '1;'

    p = parser.parser
    parse_tree = p.parse(program)
    print(parse_tree)
    o = ToLiteral()
    tree = o.transform(parse_tree)
    print(tree)
