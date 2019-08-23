#!/usr/bin/env python3

WHITESPACE = [
        # ASCII whitespace characters
        '\v', '\f', ' ',

        # Unicode whitespace
        '\u0085', '\u00a0', '\u1680', '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007',
        '\u2008', '\u2009', '\u200a', '\u2028', '\u2029', '\u202f', '\u205f', '\u3000',

        # Other whitespace characters
        '\u180e', '\u200b', '\u200c', '\u200d', '\u2060', '\ufeff'
]
NEWLINE = ['\n', '\r']
INDENT = ['\t', ' ']
ARITHMETIC_CHARACTERS = ['+', '-', '/', '*', '%', '^']
BRACKETS = ['(', ')', '[', ']', '{', '}']
RESERVED_CHARACTERS = ['!', '=', '<', '>', '.', ':',
                       ','] + ARITHMETIC_CHARACTERS + BRACKETS + INDENT + NEWLINE + WHITESPACE
