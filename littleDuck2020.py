#!/usr/bin/env python

# Argument parsing
import argparse

# PLY library
import ply.lex as lex
import ply.yacc as yacc

# Misc
import sys

# Lexer

reserved = {
    "else": "ELSE",
    "float": "T_FLOAT",
    "if": "IF",
    "int": "T_INT",
    "print": "PRINT",
    "program": "PROGRAM",
    "var": "VAR",
}

literals = ["{", "}", ":", ",", ";", "(", ")"]

tokens = [
    "ASSIGN",
    "COMPOP",
    "EXPOP",
    "FLOAT",
    "ID",
    "INT",
    "LITERAL",
    "TERMOP",
] + list(reserved.values())


# Regular expressions rules
t_ASSIGN = r"="
t_LITERAL = r"\".*\""


def t_COMPOP(t):
    r"(<>|<|>)"
    t.type = "COMPOP"
    return t


def t_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_ID(t):
    r"[a-zA-Z]\w*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_TERMOP(t):
    r"[*/]"
    t.type = "TERMOP"
    return t


def t_EXPOP(t):
    r"[\+-]"
    t.type = "EXPOP"
    return t


def t_INT(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

# Parser


def p_p(p):
    """
    p   : PROGRAM ID ';' vars block
        | PROGRAM ID ';' block
    """


def p_empty(p):
    """
    empty   :
    """


def p_vars(p):
    """
    vars    : VAR idlist ':' type ';' varlists
    """


def p_varlists(p):
    """
    varlists    : idlist ':' type ';' varlists
                | empty
    """


def p_idlist(p):
    """
    idlist  : ID ',' idlist
            | ID
    """


def p_block(p):
    """
    block   : '{' statements '}'
    """


def p_statements(p):
    """
    statements  : statement statements
                | empty
    """


def p_statement(p):
    """
    statement   : assignment
                | conditional
                | writing
    """


def p_assignment(p):
    """
    assignment  : ID ASSIGN expression ';'
    """


def p_binary_operators(p):
    """
    exp         : term EXPOP exp
    expression  : exp COMPOP exp
    term        : term TERMOP factor
    """


def p_simple(p):
    """
    expression  : exp
    exp         : term
    term        : factor
    type        : T_FLOAT
    type        : T_INT
    var_cte     : FLOAT
    var_cte     : ID
    var_cte     : INT
    writinglist : LITERAL
    writinglist : expression
    """


def p_conditional(p):
    """
    conditional : IF '(' expression ')' block else ';'
    """


def p_else(p):
    """
    else    : ELSE block
            | empty
    """


def p_factor(p):
    """
    factor  : '(' expression ')'
            | TERMOP var_cte
            | var_cte
    """


def p_writing(p):
    """
    writing : PRINT '(' expression writinglist ')' ';'
    writing : PRINT '(' LITERAL writinglist ')' ';'
    """


def p_writinglist(p):
    """
    writinglist : ',' expression writinglist
                | ',' LITERAL writinglist
                | empty
    """


def p_error(p):
    print("Syntax error at token", p.type, "at line", p.lineno)


parser = yacc.yacc()

# Argument parser set up
argparser = argparse.ArgumentParser(description="LittleDuck 2020 lexer+parser")
argparser.add_argument(
    "file",
    metavar="F",
    type=str,
    help="LittleDuck 2020 source file to read",
    default=sys.stdin,
)

if __name__ == "__main__":
    args = argparser.parse_args()
    with open(args.file, mode="r") as file:
        parser.parse(file.read(), lexer=lexer)
