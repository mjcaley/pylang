#!/usr/bin/env python3

from pylang import parser, pylang_ast as ast

def test_ast_printer():
    program = '''12 + 24;'''

    p = parser.parser
    parse_tree = p.parse(program)
    print(parse_tree)
    m = parser.ToAST()
    abtract_syntax_tree = m.transform(parse_tree)

    a = ast.ASTPrinter()
    a.visit(abtract_syntax_tree)
