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
t_COMPOP = r"(<>|<|>)"
t_EXPOP = r"[\+-]"
t_LITERAL = r"\".*\""
t_TERMOP = r"[\*/]"

def t_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_ID(t):
    r"[a-zA-Z]\w*"
    t.type = reserved.get(t.value, "ID")
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
    p   : pprime1 vars block
        | pprime1 block
    """

def p_pprime1(p):
    """
    pprime1  : PROGRAM ID ';'
    """

def p_empty(p):
    """
    empty   :
    """


def p_vars(p):
    """
    vars    : VAR varlists
    """


def p_varlists(p):
    """
    varlists    : varlistsprime1 varlists
                | varlistsprime1 
    """

def p_varlistsprime1(p):
    """
    varlistsprime1   : idlist ':' type ';'
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

def p_exp(p):
    """
    exp         : term EXPOP exp
                | term
    """

def p_expression(p):
    """
    expression  : exp COMPOP exp
                | exp
    """

def p_term(p):
    """
    term    : factor TERMOP term 
            | factor
    """


def p_type(p):
    """
    type        : T_FLOAT
                | T_INT
    """

def p_varcte(p):
    """
    varcte     : FLOAT
               | ID
               | INT
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
            | TERMOP varcte
            | varcte
    """

def p_writing(p):
    """
    writing : PRINT '(' writinglist ')' ';'
    """

def p_writinglist(p):
    """
    writinglist : expression ',' writinglist
                | LITERAL ',' writinglist
                | expression
                | LITERAL
    """

def p_error(p):
    print("Syntax error at token", p.type, "at line", p.lineno)


parser = yacc.yacc()

# Argument parser set up
argparser = argparse.ArgumentParser(description="LittleDuck 2020 lexer+parser")
argparser.add_argument(
    "generator",
    choices=['PLY', 'ANTLR4'],
    help="whether to use PLY or ANTLR4 as the lexer+parser generator tool",
    type=str,
)
argparser.add_argument(
    "file",
    default=sys.stdin,
    help="LittleDuck 2020 source file to read",
    metavar="F",
    type=str,
)

if __name__ == "__main__":
    args = argparser.parse_args()
    with open(args.file, mode="r") as file:
        parser.parse(file.read(), lexer=lexer)
