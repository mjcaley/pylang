#!/usr/bin/env python3

from .lexer.lexer import Lexer
from .recursive_descent import Parser
from .printer import ParseTreePrinter


def parse(string):
    lexer = Lexer.from_stream(string)
    parser = Parser(lexer)
    tree = parser.parse()

    return tree


def print_tree(tree):
    tree_printer = ParseTreePrinter(tree)
    tree_printer.print_tree()
