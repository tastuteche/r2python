
# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

tokens = [
    'NAME', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'NUM_CONST'
]

reserved = {
    "NULL": "NULL_CONST",
    #    "NA": "NUM_CONST",
    #    "TRUE": "NUM_CONST",
    #    "FALSE": "NUM_CONST",
    #    "Inf": "NUM_CONST",
    #    "NaN": "NUM_CONST",
    #    "NA_integer_": "NUM_CONST",
    #    "NA_real_": "NUM_CONST",
    #    "NA_character_": "NUM_CONST",
    #    "NA_complex_": "NUM_CONST",
    "function": "FUNCTION",
    "while": "WHILE",
    "repeat": "REPEAT",
    "for": "FOR",
    "if": "IF",
    "in": "IN",
    "else": "ELSE",
    "next": "NEXT",
    "break": "BREAK",
    "...": "SYMBOL",
}
t_NUM_CONST = r'NA|TRUE|FALSE|Inf|NaN|NA_integer_|NA_real_|NA_character_|NA_complex_'
tokens += reserved.values()


# Tokens
# t_c =  r'{' #brace
#t_c =  r'('
#t_c =  r'['
#t_c =  r'?'
#t_c =  r'*'


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
#t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


t_LE = r'<='
#t_LEFT_ASSIGN = r'<-'
#t_LEFT_ASSIGN = r'<<-'
t_LT = r'<'
t_GE = r'>='
t_GT = r'>'
t_NE = r'!='
t_EQ = r'=='
t_EQ_ASSIGN = r'='
t_NS_GET_INT = r':::'
t_NS_GET = r'::'
t_LEFT_ASSIGN = r':=|<-|<<-'
t_AND2 = r'&&'
t_AND = r'&'
t_OR2 = r'\|\|'
t_OR = r'\|'
t_LBB = r'\[\['

tokens += ['NS_GET_INT', 'OR2', 'LEFT_ASSIGN', 'EQ', 'NS_GET', 'AND2',
           'GE', 'LBB', 'NE', 'LE', 'GT', 'LT', 'AND', 'OR', 'EQ_ASSIGN']


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules
t_QUESTION = r'\?'
t_TILDE_ = r'~'
t_COLON = r':'
t_CARET = r'\^'
t_AT_SIGN = r'@'
t_DOLLAR = r'\$'
t_LBRACKET = r'\['

tokens += ['RIGHT_ASSIGN', 'QUESTION', 'AT_SIGN', 'TILDE_', 'UNOT', 'LOW',
           'SPECIAL', 'UPLUS', 'COLON', 'DOLLAR', 'LBRACKET', 'NOT', 'CARET', 'TILDE']

precedence = (
    ("left", 'QUESTION'),
    ("left", "LOW", "WHILE", "FOR", "REPEAT",),
    ("right", "IF",),
    ("left", "ELSE",),
    ("right", "LEFT_ASSIGN",),
    ("right", "EQ_ASSIGN",),
    ("left", "RIGHT_ASSIGN",),
    ("left", 'TILDE_', "TILDE",),
    ("left", "OR", "OR2",),
    ("left", "AND", "AND2",),
    ("left", "UNOT", "NOT",),
    ("nonassoc", "GT", "GE", "LT", "LE", "EQ", "NE",),
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'DIVIDE'),
    ("left", "SPECIAL",),
    ("left", 'COLON'),
    ("left", "UMINUS", "UPLUS",),
    ("right", 'CARET'),
    ("left", 'DOLLAR', 'AT_SIGN'),
    ("left", "NS_GET", "NS_GET_INT",),
    ("nonassoc", 'LPAREN', 'LBRACKET', "LBB",),
)

# DICTIONARY OF names
names = {}


def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]


def p_statement_expr(t):
    'statement : expression'
    print(t[1])


def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] in ['+', '-', '*', '/']:
        t[0] = "%s %s %s" % (t[1], t[2], t[3])


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]


def p_expression_number(t):
    'expression : NUMBER'
    t[0] = str(t[1])


def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0


def p_error(t):
    print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)
