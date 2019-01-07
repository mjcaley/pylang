#!/usr/bin/env python3

from lark import Lark, Visitor
# import llvmlite.binding as llvm
# import llvmlite.ir as ir

from pylang_ast import *


PYLANG_GRAMMAR = '''
    start: statement+
    
    statement: sum_expr EOL
    
    sum_expr: NUMBER ADD_OP NUMBER
    
    EOL: ";"
    
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
program = "42 + 24;"
tree = parser.parse(program)
print(tree.pretty())

class MyVisitor(Visitor):
    def __init__(self):
        self.ast = None
    
    def start(self, tree):
        print("start rule")
        self.ast = Start(tree)

    def statement(self, tree):
        print("statement rule")
        self.ast = Statement(tree)

    def sum_expr(self, tree):
        print("sum_expr rule")
        self.ast = SumExpression(tree.children[0], tree.children[2])


m = MyVisitor()
m.visit(tree)
print(repr(m.ast))

# llvm.initialize()
# llvm.initialize_native_target()
# llvm.initialize_native_asmprinter()

# module = ir.Module()
# sum_func = ir.Function(module, ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)]), 'sum')

# block = sum_func.append_basic_block()
