import sys

# dictionary of names
names = {}
# dictionary of function names
fun_names = {}


class Node:

    def __init__(self):
        print("init node")

    def evaluate(self):
        return 0

    def execute(self):
        return 0


class NumberNode(Node):
    def __init__(self, v):
        if '.' in v:
            self.value = float(v)
        else:
            self.value = int(v)

    def evaluate(self):
        return self.value


class NegatNode(Node):
    def __init__(self, v):
        self.v = v

    def evaluate(self):
        return -self.v.evaluate()


class StringNode(Node):

    def __init__(self, v):
        self.value = v

    def evaluate(self):
        return self.value


class ListNode(Node):

    def __init__(self, v):

        self.v = v

    def evaluate(self):

        a = []

        if self.v is None:
            return a

        for i in range(len(self.v)):
            a.append(self.v[i].evaluate())

        return a


class TupleNode(Node):

    def __init__(self, v):

        self.v = v

    def evaluate(self):

        a = []

        if self.v is None:
            return a

        for i in range(len(self.v)):
            a.append(self.v[i].evaluate())

        return tuple(a)


class BooleanNode(Node):

    def __init__(self, v):
        if v == 'True' or v is True:
            self.v = True
        elif v == 'False' or v is False:
            self.v = False

    def evaluate(self):
        return self.v


class NotNode(Node):
    def __init__(self, v):
        self.v = v

    def evaluate(self):
        return not self.v.evaluate()


class IndexNode(Node):  # a[b], list or string
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        input1 = self.v1.evaluate()
        input2 = self.v2.evaluate()
        if input2 >= len(input1) or input2 < 0:
            raise IndexError()
        return input1[input2]


class BopNode(Node):

    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if self.op == '+':
            return self.v1.evaluate() + self.v2.evaluate()
        elif self.op == '-':
            return self.v1.evaluate() - self.v2.evaluate()
        elif self.op == '*':
            return self.v1.evaluate() * self.v2.evaluate()
        elif self.op == '/':
            if self.v2.evaluate() == 0:
                raise ZeroDivisionError()
            return self.v1.evaluate() / self.v2.evaluate()
        elif self.op == 'div':
            if self.v2.evaluate() == 0:
                raise ZeroDivisionError()
            if not isinstance(self.v1.evaluate(), int) or not isinstance(self.v1.evaluate(), int):
                raise TypeError()
            return self.v1.evaluate() // self.v2.evaluate()
        elif self.op == 'mod':
            if not isinstance(self.v1.evaluate(), int) or not isinstance(self.v1.evaluate(), int):
                raise TypeError()
            return self.v1.evaluate() % self.v2.evaluate()
        elif self.op == '**':
            return self.v1.evaluate() ** self.v2.evaluate()


class CompareNode(Node):  # for string and number

    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):

        # do operation on 2 different type
        if self.op == 'andalso':
            return BooleanNode(self.v1.evaluate() and self.v2.evaluate()).evaluate()
        elif self.op == 'orelse':
            return BooleanNode(self.v1.evaluate() or self.v2.evaluate()).evaluate()
        elif self.op == '<':
            return BooleanNode(self.v1.evaluate() < self.v2.evaluate()).evaluate()
        elif self.op == '>':
            return BooleanNode(self.v1.evaluate() > self.v2.evaluate()).evaluate()
        elif self.op == '==':
            return BooleanNode(self.v1.evaluate() == self.v2.evaluate()).evaluate()
        elif self.op == '<>':
            return BooleanNode(self.v1.evaluate() != self.v2.evaluate()).evaluate()
        elif self.op == '<=':
            return BooleanNode(self.v1.evaluate() <= self.v2.evaluate()).evaluate()
        elif self.op == '>=':
            return BooleanNode(self.v1.evaluate() >= self.v2.evaluate()).evaluate()
        elif self.op == 'in':
            return BooleanNode(self.v1.evaluate() in self.v2.evaluate()).evaluate()
        elif self.op == '::':
            if not isinstance(self.v2.evaluate(), list):
                raise TypeError()
            return [self.v1.evaluate()] + self.v2.evaluate()
        elif self.op == '#':
            if not isinstance(self.v2.evaluate(), tuple) and not isinstance(self.v1.evaluate(), int):
                print(self.v2.evaluate())
                raise TypeError()
            return self.v2.evaluate()[self.v1.evaluate() - 1]


class BlockNode(Node):
    def __init__(self, sl):
        self.statementList = sl

    def evaluate(self):
        if self.statementList is not None:
            for statement in self.statementList:
                statement.evaluate()


class NameNode(Node):

    def __init__(self, v):
        self.v = v

    def evaluate(self):
        try:
            temp = names[self.v]
            return temp
        except LookupError:
            raise Exception


class AssignmentNode(Node):

    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        names[self.v1] = self.v2.evaluate()


class IndexAssignmentNode(Node):
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def evaluate(self):
        if self.v1 in names:
            names[self.v1][self.v2.evaluate()] = self.v3.evaluate()
        else:
            raise TypeError()


class Index2DAssignmentNode(Node):

    def __init__(self, v1, v2, v3, v4):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4

    def evaluate(self):
        index = self.v2.evaluate()
        index2 = self.v3.evaluate()
        if self.v1.evaluate() in names and isinstance(index, int):
            names[self.v1.evaluate()][index][index2] = self.v4.evaluate()
        else:
            raise TypeError()


class IfNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        if self.v1.evaluate():
            self.v2.evaluate()


class IfElseNode(Node):
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def evaluate(self):
        if self.v1.evaluate():
            self.v2.evaluate()
        else:
            self.v3.evaluate()


class WhileNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        while self.v1.evaluate():
            self.v2.evaluate()


class FunctionNode(Node):
    def __init__(self, name, params, block, output):
        self.name = name
        self.params = params
        self.block = block
        self.output = output

    def evaluate(self):
        self.block.evaluate()


class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def evaluate(self):
        fn = fun_names[self.name]
        new_dic = {}
        for i in range(len(fn.params)):
            new_dic[fn.params[i]] = self.args[i].evaluate()
        global names
        old_vars = names
        names = new_dic
        fn.evaluate()
        result = fn.output.evaluate()
        names = old_vars
        return result


class PrintNode(Node):

    def __init__(self, e):
        self.e = e

    def evaluate(self):
        print(self.e.evaluate())


reserved = {
    'div': 'DIV',
    'mod': 'MODULES',
    'andalso': 'AND',
    'orelse': 'OR',
    'not': 'NOT',
    'in': 'IN',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'fun': 'FUN'
}

tokens = [
             'SEMICOLON', 'LPAREN', 'RPAREN',
             'NUMBER', 'STRING', 'LIST',
             'LBRAK', 'RBRAK', 'COMMA', 'L_CURLY', 'R_CURLY',
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
             'POWER', 'GREATER', 'LESS', 'GREATERTHAN',
             'LESSTHAN', 'EQUAL', 'NOTEQUAL', 'TUPLEINDEX',
             'TRUE', 'FALSE', 'CONCAT', 'EQUALS', 'ID'
         ] + list(reserved.values())

# Tokens
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_POWER = r'\*\*'
t_LBRAK = r'\['
t_RBRAK = r'\]'
t_GREATER = r'<'
t_LESS = r'>'
t_GREATERTHAN = r'>='
t_LESSTHAN = r'<='
t_EQUAL = r'=='
t_NOTEQUAL = r'<>'
t_TUPLEINDEX = '\#'
t_CONCAT = '::'
t_EQUALS = '='
t_L_CURLY = '{'
t_R_CURLY = '}'


def t_TRUE(t):
    'True'
    t.value = BooleanNode(t.value)
    return t


def t_FALSE(t):
    'False'
    t.value = BooleanNode(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_NUMBER(t):
    r'((-?\d*(\d\.|\.\d)\d* | \d+) [e]-?\d+)|(-?\d*(\d\.|\.\d)\d* | \d+)'
    try:
        t.value = NumberNode(t.value)
    except ValueError:
        print("SYNTAX ERROR")
        t.value = 0
    return t


def t_STRING(t):
    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''  # double or single quote
    t.value = t.value[1:len(t.value) - 1]
    t.value = StringNode(literal_eval("'%s'" % t.value))  # remove escape char
    return t


# Ignored characters
t_ignore = " \t"


def t_error(t):
    # print("t_error?")
    raise SyntaxError()


# Build the lexer

import ply.lex as lex

lex.lex(debug=0)
# Parsing rules
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'GREATER', 'LESS', 'GREATERTHAN', 'LESSTHAN', 'EQUAL', 'NOTEQUAL'),
    ('right', 'CONCAT'),
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULES', 'DIV'),
    ('right', 'POWER'),
    ('left', 'TUPLEINDEX'),
    ('left', 'LBRAK', 'RBRAK'),
    ('right', 'UMINUS'),
)


def p_program(t):
    'program : functions block'

    t[0] = t[2]


def p_function(t):
    'functions : functions function'
    t[0] = t[1] + [t[2]]


def p_function1(t):
    'functions : function'
    t[0] = [t[1]]


def p_function2(t):
    'function : FUN ID LPAREN params RPAREN EQUALS block expression SEMICOLON'
    t[0] = FunctionNode(t[2], t[4], t[7], t[8])
    fun_names[t[2]] = t[0]


def p_parms2(p):
    'params : params COMMA ID'
    p[0] = p[1] + [p[3]]


def p_parms(p):
    'params : ID'
    p[0] = [p[1]]


def p_function_call(t):
    'expression : function_call'
    t[0] = t[1]


def p_function_call2(p):
    'function_call : ID LPAREN args RPAREN'
    p[0] = FunctionCall(p[1], p[3])


def p_args2(p):
    'args : args COMMA expression'
    p[0] = p[1] + [p[3]]


def p_args(p):
    'args : expression'
    p[0] = [p[1]]


def p_block(p):
    '''block : L_CURLY statement_list R_CURLY'''
    p[0] = BlockNode(p[2])


def p_empty_block(p):
    ''' block : L_CURLY R_CURLY'''
    p[0] = BlockNode(None)


def p_statement_list(p):
    '''
     statement_list : statement_list statement
    '''
    p[0] = p[1] + [p[2]]


def p_statement_list_val(p):
    '''
    statement_list : statement
    '''
    p[0] = [p[1]]


def p_stat_format(t):
    '''statement : expression SEMICOLON
            | block
    '''
    t[0] = t[1]


def p_statement_assign(t):
    '''statement : ID EQUALS expression SEMICOLON'''
    t[0] = AssignmentNode(t[1], t[3])


def p_indexNode_statement_assign(t):
    '''statement : ID  LBRAK expression RBRAK EQUALS expression SEMICOLON'''
    t[0] = IndexAssignmentNode(t[1], t[3], t[6])


def p_indexNode2D_statement_assign(t):
    '''statement : ID  LBRAK expression RBRAK LBRAK expression RBRAK EQUALS expression SEMICOLON'''
    t[0] = Index2DAssignmentNode(t[1], t[3], t[6], t[9])


def p_expression_ID(t):
    'expression : ID'
    t[0] = NameNode(t[1])


def p_if_statement(t):
    'statement : IF LPAREN expression RPAREN block'

    t[0] = IfNode(t[3], t[5])


def p_if_else_statement(t):
    'statement : IF LPAREN expression RPAREN block ELSE block'

    t[0] = IfElseNode(t[3], t[5], t[7])


def p_while_statement(t):
    'statement : WHILE LPAREN expression RPAREN block'

    t[0] = WhileNode(t[3], t[5])


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'

    t[0] = NegatNode(t[2])


def p_expression_binop(t):  # the subtraction should only work on number

    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression DIV expression
                  | expression MODULES expression
                  | expression POWER expression
                  '''
    t[0] = BopNode(t[2], t[1], t[3])


def p_expression_comapre(t):  # return boolean only

    '''expression : expression GREATER expression
                  | expression LESS expression
                  | expression LESSTHAN expression
                  | expression GREATERTHAN expression
                  | expression EQUAL expression
                  | expression NOTEQUAL expression
                  | expression IN expression
                  | expression OR expression
                  | expression AND expression
                  | expression CONCAT expression
                  '''

    t[0] = CompareNode(t[2], t[1], t[3])


def p_expression_not(t):
    'expression : NOT expression'

    t[0] = NotNode(t[2])


def p_parenthesized(t):
    '''expression : LPAREN expression RPAREN '''

    t[0] = t[2]


def p_list_empty(t):
    '''expression : LBRAK RBRAK'''

    t[0] = ListNode(None)


def p_list(t):
    '''expression : LBRAK in_list RBRAK '''

    t[0] = ListNode(t[2])


def p_in_list(t):
    '''in_list : expression'''

    t[0] = [t[1]]


def p_in_list2(t):
    '''in_list : in_list COMMA expression'''

    t[0] = t[1] + [t[3]]


def p_tuple(t):
    '''expression : LPAREN in_tuple RPAREN'''
    t[0] = TupleNode(t[2])


def p_in_tuple(t):
    '''in_tuple : expression'''

    t[0] = [t[1]]


def p_in_tuple2(t):
    '''in_tuple : in_tuple COMMA expression'''
    t[0] = t[1] + [t[3]]


def p_tuple_empty(t):
    '''expression : LPAREN RPAREN'''
    t[0] = TupleNode(None)


def p_tuple_index(t):
    '''expression : TUPLEINDEX expression expression %prec TUPLEINDEX'''
    t[0] = CompareNode(t[1], t[2], t[3])


def p_indexing(t):
    '''expression : expression LBRAK expression RBRAK'''
    t[0] = IndexNode(t[1], t[3])


def p_expression_types(t):
    '''expression : STRING
        | NUMBER
        | LIST
        | TRUE
        | FALSE
        '''
    t[0] = t[1]


def p_print_statement(p):
    '''statement : PRINT LPAREN expression RPAREN SEMICOLON'''
    p[0] = PrintNode(p[3])


def p_error(t):
    sys.exit("SYNTAX ERROR")


import ply.yacc as yacc

yacc.yacc(debug=0)

import sys

if (len(sys.argv) != 2):
    sys.exit("invalid arguments")

with open(sys.argv[1], 'r') as myfile:
    code = myfile.read().replace('\n', '')

try:
    lex.input(code)
    # while True:
    #     token = lex.token()
    #     if not token: break
    #     print(token)
    root = yacc.parse(code)
    root.evaluate()


except Exception:
    print("SEMANTIC ERROR")
