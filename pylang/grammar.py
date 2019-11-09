#!/usr/bin/env python3

import logging

from lark import Lark
from lark.indenter import Indenter


logging.basicConfig(level=logging.DEBUG)


class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = ['LPAREN', 'LBRACE', 'LSQUARE']
    CLOSE_PAREN_types = ['RPAREN', 'RBRACE', 'RSQUARE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4


parser = Lark(r'''
    start: _NL* stmt+
    
    block: _INDENT stmt+ _DEDENT
    stmt: function_def
             | if_stmt
             | for_stmt
             | while_stmt
             | struct_stmt
             | import_stmt
             | expr _NL
             
    // Struct rules
    struct_stmt: _single_struct | _multi_struct
    _single_struct: _STRUCT type_definition
    _multi_struct: _STRUCT _NL _INDENT type_definition+ _DEDENT
    type_definition: IDENTIFIER _COLON _NL type_block
    type_block: _INDENT (type_decl _NL)+ _DEDENT
    type_decl: IDENTIFIER _COLON IDENTIFIER
    
    // Import rules
    import_stmt: _IMPORT _module _NL
    _module: IDENTIFIER (_DOT IDENTIFIER)*
    
    // Function rules
    function_def: _function_decl ASSIGN _NL block
    _function_decl: _FUNC IDENTIFIER _LPAREN param_decl? _RPAREN return?
    return: _COLON IDENTIFIER
    param_decl: IDENTIFIER (_COMMA IDENTIFIER)*
    
    // Conditional statement rules
    if_stmt: _IF condition _COLON _NL then elif_stmt?
    ?elif_stmt: (_ELIF condition _COLON _NL then elif_stmt?) | else_stmt
    else_stmt: _ELSE _COLON _NL then
    condition: expr
    then: block
    
    // Loop statement rules
    for_stmt: _FOR expr _COLON _NL block
    while_stmt: _WHILE expr _COLON _NL block
    
    // Expression rules
    ?expr: assign_expr
    ?assign_expr: or_expr _assign_op assign_expr | or_expr
    ?or_expr: or_expr _OR and_expr | and_expr
    ?and_expr: and_expr _AND sum_expr | sum_expr
    ?sum_expr: sum_expr (PLUS | MINUS) product_expr | product_expr
    ?product_expr: product_expr (MULTIPLY | DIVIDE | MODULUS) exponent_expr | exponent_expr
    ?exponent_expr: exponent_expr EXPONENT unary_expr | unary_expr
    ?unary_expr: (NOT | PLUS | MINUS) unary_expr | _call_expr
    
    _call_expr: field_access
              | call 
              | subscript 
              | atom
    field_access: _call_expr _DOT atom
    call: _call_expr _LPAREN [expr (_COMMA expr)*] _RPAREN 
    subscript: _call_expr _LSQUARE expr _RSQUARE 
    
    ?atom: _integer
         | _float
         | IDENTIFIER
         | ESCAPED_STRING
         | TRUE
         | FALSE
         | _LPAREN expr _RPAREN
        
    _integer: HEX | BIN | OCT | INTEGER
    _float: FLOAT
    //INTEGER: "0".."9" | ("1".."9" INT? ( "_" INT)*)
    INTEGER: INT
    HEX: "0x" HEXDIGIT+
    BIN: "0b" "0".."1"+
    OCT: "0o" "0".."7"+
    FLOAT: INTEGER _DOT INTEGER
    
    _assign_op: ASSIGN
              | PLUS_ASSIGN
              | MINUS_ASSIGN
              | MULTIPLY_ASSIGN
              | DIVIDE_ASSIGN
              | MODULUS_ASSIGN
              | EXPONENT_ASSIGN
    
    _IMPORT: "import"
    _FUNC: "func"
    _STRUCT: "struct"
    _IF: "if"
    _ELIF: "elif"
    _ELSE: "else"
    _FOR: "for"
    _WHILE: "while"
    _AND: "and"
    _OR: "or"
    NOT: "not"
    TRUE: "true"
    FALSE: "false"
    _RETURN: "return"
    
    _DOT: "."
    ASSIGN: "="
    
    PLUS: "+"
    PLUS_ASSIGN: "+="
    MINUS: "-"
    MINUS_ASSIGN: "-="
    MULTIPLY: "*"
    MULTIPLY_ASSIGN: "*="
    DIVIDE: "/"
    DIVIDE_ASSIGN: "/="
    MODULUS: "%"
    MODULUS_ASSIGN: "%="
    EXPONENT: "**"
    EXPONENT_ASSIGN: "**="
        
    EQUAL: "=="
    NOT_EQUAL: "!="
    LESS_THAN: "<"
    GREATER_THAN: ">"
    LESS_OR_EQUAL: "<="
    GEATER_OR_EQUAL: ">="
        
    _LPAREN: "("
    _RPAREN: ")"
    _LCALL: "("
    _RCALL: ")"
    _LBRACE: "{"
    _RBRACE: "}"
    _LSQUARE: "["
    _RSQUARE: "]"
    
    _COLON: ":"
    _COMMA: ","
    
    _NL: /(\r?\n[\t ]*)+/
    
    %import common.CNAME -> IDENTIFIER
    %import common.INT
    %import common.DECIMAL
    %import common.ESCAPED_STRING
    %import common.HEXDIGIT
    %import common.WS_INLINE
    %declare _INDENT _DEDENT
    %ignore WS_INLINE
    
''', parser='lalr', postlex=TreeIndenter(), debug=True)

parser2 = Lark('''
?start: expr

?expr: expr ADD expr
    | expr SUB expr
    | expr MUL expr
    | expr DIV expr
    | expr MOD expr
    | _LP expr _RP
    | NEG expr -> unary_expr
    | expr ASSIGN expr
    | atom

?atom: INT | "a".."z"

ASSIGN.10: "="
ADD.1: "+"
SUB.1: "-"
MUL.2: "*"
DIV.2: "/"
MOD.2: "%"
_LP.3: "("
_RP.3: ")"
NEG.4: "-"

%import common.INT
%import common.WS_INLINE
%ignore WS_INLINE
''', parser='lalr')
