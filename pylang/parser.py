#!/usr/bin/env python3

from lark import Lark
import llvmlite.binding as llvm
import llvmlite.ir as ir

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

print(parser.parse("42 + 24;"))


llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

module = ir.Module()
sum_func = ir.Function(module, ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)]), 'sum')

block = sum_func.append_basic_block()
block.
