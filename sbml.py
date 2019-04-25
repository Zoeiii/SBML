from ast import literal_eval
class Node:
    def __init__(self):
        print("init node")

    def evaluate(self):
        return 0

    def execute(self):
        return 0

    def find_type(self):
        return "dummy"

class NameNode:
    def __init__(self,v):
        self.value = v;

    def evaluate(self):
        return self.value;

class NumberNode(Node):
    def __init__(self, v):
        self.type = "NUMBER"
        if ('.' in v):
            self.type = "NUMBERREAL"
            self.value = float(v)
        else:
            self.type = "NUMBERINT"
            self.value = int(v)

    def evaluate(self):
        return self.value

    def find_type(self):
        return self.type

class NegatNode(Node):
    def __init__(self, v):
        self.type = "NUMBER"
        self.v = -v.evaluate()

    def evaluate(self):
        return self.v

    def find_type(self):
        return self.type

class StringNode(Node):
    def __init__(self, v):
        self.value = v
        self.type = "STRING"

    def evaluate(self):
        return self.value

    def find_type(self):
        return self.type

class ListNode(Node):
    def __init__(self, v):
        self.type = "LIST"
        if(v == '['):
            self.v = []
        else:
            self.v = [v.evaluate()]

    def evaluate(self):
        return self.v

    def find_type(self):
        return self.type

class TupleNode(Node):
    def __init__(self, v):
        self.type = "TUPLE"
        if v == '(':
            self.v = ()
        else:
            self.v = tuple(v)

    def evaluate(self):
        return self.v

    def find_type(self):
        return self.type

class BooleanNode(Node):
    def __init__(self, v):
        self.type = "BOOLEAN"
        if v == 'True' or v is True:
            self.v = True
        elif v == 'False' or v is False:
            self.v = False

    def evaluate(self):
        return self.v

    def find_type(self):
        return self.type

class NotNode(Node):
    def __init__(self, v):
        self.type = "BOOLEAN"
        self.v = v.evaluate()
        if self.v:
            self.v = False
        else:
            self.v = True

    def evaluate(self):
        return self.v

    def find_type(self):
        return self.type

class IndexNode(Node): #a[b], list or string
    def __init__(self, v1, v2):
        if (v1.find_type() != 'LIST' or v1.find_type() != 'STRING')and 'INT' not in v2.find_type():
            raise TypeError()
        self.type = v1.find_type()
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        input1 = self.v1.evaluate()
        input2 = self.v2.evaluate()
        if input2 >= len(input1) or input2 < 0:
            raise IndexError()
        return input1[input2]

    def find_type(self):
        self.type = FindTypeNode(self.evaluate()).find_type()
        return self.type

class BopNode(Node):
    def __init__(self, op, v1, v2):
        if v1.find_type() == v2.find_type() or ('NUMBER' in v1.find_type() and 'NUMBER' in v2.find_type()):
            pass
        else:
            raise TypeError()
        self.v1 = v1
        self.v2 = v2
        self.op = op
        self.type = self.v1.find_type()

    def evaluate(self):
        # print(self.v1.find_type(), self.v2.find_type())
        # print(self.op, self.v1.evaluate(), self.v2.evaluate())
        if self.op == '+':
            if 'NUMBER' not in self.v1.find_type() and self.v1.find_type() != 'STRING' and self.v1.find_type() != 'LIST':
                raise TypeError()
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
            if 'INT' not in self.v1.find_type() or 'INT' not in self.v2.find_type():
                raise TypeError()
            return self.v1.evaluate() // self.v2.evaluate()
        elif self.op == 'mod':
            if 'INT' not in self.v1.find_type() or 'INT' not in self.v2.find_type():
                raise TypeError()
            return self.v1.evaluate() % self.v2.evaluate()
        elif self.op == '**':
            return self.v1.evaluate() ** self.v2.evaluate()

    def find_type(self):
        self.type = FindTypeNode(self.evaluate()).find_type()
        return self.type

class CompareNode(Node): #for string and number
    def __init__(self, op, v1, v2):
        self.type = "BOOLEAN"
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        # print(self.v1.evaluate(), self.op, self.v2.evaluate())
        # print(self.v1.find_type(), self.v2.find_type())
        # do operation on 2 different type
        if self.v1.find_type() == self.v2.find_type() or ('NUMBER' in self.v1.find_type() and 'NUMBER' in self.v2.find_type()) \
                or (self.op == 'in' and (self.v2.find_type() != 'LIST' or self.v2.find_type() != 'STRING')) \
                or(self.op == '#' and self.v2.find_type() == 'TUPLE' and self.v1.find_type() == 'NUMBERINT') \
                or(self.op == '::' and self.v2.find_type() == 'LIST'):
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
                return [self.v1.evaluate()] + self.v2.evaluate()
            elif self.op == '#':
                # print(self.v1.evaluate(), self.op, self.v2.evaluate())
                # print(self.v1.find_type(), self.v2.find_type())
                # if self.v2.find_type()!= 'TUPLE':
                #     raise TypeError()
                return self.v2.evaluate()[self.v1.evaluate()-1]

            raise TypeError()

    def find_type(self):
        self.type = FindTypeNode(self.evaluate()).find_type()
        return self.type

class FindTypeNode(Node):
    def __init__(self, v):
        self.v = v

    def evaluate(self):
        return self.v

    def find_type(self):
        if self.v == 'True' or self.v == 'False' or self.v is True or not self.v:
            self.type = 'BOOLEAN'
        elif isinstance(self.v, str):
            self.type = 'STRING'
        elif isinstance(self.v, int):
            self.type = 'NUMBERINT'
        elif isinstance(self.v, float):
            self.type = 'NUMBERREAL'
        elif isinstance(self.v, tuple):
            self.type = 'TUPLE'
        elif isinstance(self.v, list):
            self.type = 'LIST'
        return self.type

class PrintNode(Node):
    def __init__(self, v):
        self.value = v
        self.type = v.find_type()

    def execute(self):
        self.value = self.value.evaluate()
        if self.type == 'STRING':
            self.value = '\'' + self.value + '\''
        print(self.value)
reserved = {
    'div': 'DIV',
    'mod': 'MODULES',
    'andalso': 'AND',
    'orelse': 'OR',
    'not': 'NOT',
    'in': 'IN'
 }
tokens = [
    'SEMICOLON', 'LPAREN', 'RPAREN',
    'NUMBER', 'STRING', 'LIST',
    'LBRAK', 'RBRAK', 'COMMA',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
     'POWER', 'GREATER', 'LESS', 'GREATERTHAN',
    'LESSTHAN', 'EQUAL', 'NOTEQUAL', 'TUPLEINDEX',
    'TRUE', 'FALSE', 'CONCAT', 'NAME', 'EQUALS'
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
    t.value = StringNode(literal_eval("'%s'" % t.value))#remove escape char
    return t

def t_Name(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    t.value = NameNode(t.value)

# Ignored characters
t_ignore = " \t"


def t_error(t):
    raise SyntaxError()


# Build the lexer
import ply.lex as lex

lex.lex(debug=0)

# Parsing rules
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left',  'GREATER', 'LESS', 'GREATERTHAN', 'LESSTHAN', 'EQUAL', 'NOTEQUAL'),
    ('right', 'CONCAT'),
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULES', 'DIV'),
    ('right', 'POWER'),
    ('left', 'LBRAK', 'RBRAK', 'INDEX'),
    ('left', 'TUPLEINDEX'),
    ('left', 'LPAREN', 'RPAREN'),
    ('right', 'UMINUS')
)


def p_print_smt(t):
    """
    print_smt : expression SEMICOLON
    """
    t[0] = PrintNode(t[1])

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    NameNode[t[1]] = t[3]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = NameNode[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = NegatNode(t[2])

def p_expression_binop(t):#the subtraction should only work on number
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
    t[0] = ListNode(t[1])

def p_list(t):
    '''expression : LBRAK in_list RBRAK '''
    t[0] = t[2]

def p_in_list(t):
    '''in_list : expression'''
    t[0] = ListNode(t[1])

def p_in_list2(t):
    '''in_list : in_list COMMA expression'''
    t[0] = t[1]
    t[0].evaluate().append(t[3].evaluate())

def p_tuple(t):
    '''expression : LPAREN in_tuple RPAREN'''
    t[0] = TupleNode(t[2].evaluate())

def p_in_tuple(t):
    '''in_tuple : expression'''
    t[0] = ListNode(t[1])

def p_in_tuple2(t):
    '''in_tuple : in_tuple COMMA expression'''
    t[0] = t[1]
    t[0].evaluate().append(t[3].evaluate())

def p_tuple_empty(t):
    '''expression : LPAREN RPAREN'''
    t[0] = TupleNode(t[1])

def p_tuple_index(t):
    '''expression : TUPLEINDEX expression expression %prec TUPLEINDEX'''
    t[0] = CompareNode(t[1], t[2], t[3])

def p_indexing(t):
    '''expression : expression LBRAK expression RBRAK %prec INDEX'''
    t[0] = IndexNode(t[1], t[3])

def p_expression_types(t):
    '''expression : STRING
        | NUMBER
        | LIST
        | TRUE
        | FALSE
        '''
    t[0] = t[1]
def p_error(t):
    raise SyntaxError()


import ply.yacc as yacc

yacc.yacc(debug=0)

import sys

if (len(sys.argv) != 2):
    sys.exit("invalid arguments")
fd = open(sys.argv[1], 'r')
code = ""

for line in fd:
    code += line.strip()

try:
    lex.input(code)
    while True:
        token = lex.token()
        if not token: break
        # print(token)
    ast = yacc.parse(code)
    ast.execute()

except Exception or SyntaxError or IndexError:
    print("SYNTAX ERROR")
except ZeroDivisionError or TypeError:
    print("SEMANTIC ERROR")
