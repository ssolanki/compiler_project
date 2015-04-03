import os,sys
import time
import dlex
import ply.yacc as yacc
tokens = dlex.tokens
#from SymbolTable import *


# precedence = (
#  ('right','EQUALS','ADD_ASSIGN','MOD_ASSIGN','SUB_ASSIGN','MUL_ASSIGN','DIV_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','XOR_ASSIGN','OR_ASSIGN','AND_ASSIGN'),
#  ('left','OR_OP','AND_OP'),
#  ('left','NOTEQUALS','EQUALS_OP'),
#  ('left','L_OP','G_OP','LE_OP','GE_OP'),
#  ('left','ADD','MINUS'),
#  ('left','MULT','DIV','MOD'),
#  ('right', 'UELSE'),
#  ('right', 'ELSE')
# )

class Table(object):
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.child_tables = []
        self.variables = {}

    def add_table(self, obj):
        self.child_tables.append(obj)
        obj.parent = self

    def add_variable(self, obj, setType, setSize=0):
        if obj in self.variables:
            return False
        else:
            self.variables[obj] = {}
            self.variables[obj]['type'] = setType
            self.variables[obj]['size'] = setSize
            self.variables[obj]['offset'] = 'NA'
            return True

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.code = ""
        self.next = "next"
        self.place = ""
        self.count = 0

    def add_child(self, obj):
        self.children.append(obj)


mass = 0
errors = 0
labels = 0
offset = 0
type_size = {'int':4,'char':1,'float':4,'double':8,'function':0}
lineno = 1
global_scope = Table('Global_variables')
current_scope = global_scope
tableux = 1

i = 0
f = open('3ac.dot','wb')
f.write('strict digraph graphname {\n\n0 [label="program"]\n')
def print_all(n):
    global i
    global f
    ni = i
    i = i+1
    for c in n.children:
        a = '{} {} {} {} \n'.format(i,'[label="',c.data,'"];')
        f.write(a)
        a = '{} {} {} {} \n'.format(ni,'->',i,';')
        f.write(a)
        print_all(c)

def print_table(obj):
    # print "\nPrinting table", obj.data
    # for j in obj.variables:
    #     print j, ':', obj.variables[j]
    # print "Children of", obj.data, ":",
    # flag = False
    # for i in obj.child_tables:
    #     flag = True
    #     print i.data,
    # if(not flag):
    #     print "No child\n"
    # else:
    #     print " "
    # for i in obj.child_tables:
    #     print_table(i)
    i = 0

#--------------------yacc grammer rule for d programming langugage-------#


def p_startProgram(p):
    ''' Program : LIST_OF_STATEMENTS
                '''
    p[0] = p[1]
    print_all(p[0])
    global f
    f.write('\n\n}')
    f.close()
    p[0].code = p[1].code
    f = open('3ac.mass','wb')
    f.write(p[0].code)
    f.close()
    global global_scope
    print_table(global_scope)
    pass

def p_LIST_OF_STATEMENTS(p):
    ''' LIST_OF_STATEMENTS : LIST_OF_STATEMENTS STATEMENT
                        | STATEMENT
                        '''
    if(len(p)== 3):
        n = Node('STATEMENTS1')
        n.add_child(p[1])
        n.add_child(p[2])
        p[0] = n
        p[0].code = p[1].code + p[2].code
    else:
        p[0] = p[1]
        p[0].code = p[1].code
        p[0].next = p[1].next

def p_STATEMENT(p):
    ''' STATEMENT : EXPRESSION_STATEMENT                    
                    | DECISION_STATEMENT
                    | LOOP_STATEMENT
                    | RETURN_STATEMENT
                    | BREAK_STATEMENT 
                    | VARIABLE_DECLARATION
                    | FUNCTION_DECL
                    | VARIABLE_DEF
                    | TEMPLATES
                                       
                    '''
    p[0] = p[1]
    p[0].code = p[1].code
    p[0].next = p[1].next


#----------------------------------------------------------------

def p_FUNCTION_DECL(p):
    ''' FUNCTION_DECL : VARIABLE_TYPE IDENTIFIER LEFTPAR LIST_OF_PARAMETERS RIGHTPAR  LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES
                        | VARIABLE_TYPE IDENTIFIER LEFTPAR  RIGHTPAR  LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES                                                    
                        | VARIABLE_TYPE IDENTIFIER LEFTPAR LIST_OF_PARAMETERS RIGHTPAR NOTHROW STATEMENT  
                        | REF VARIABLE_TYPE IDENTIFIER LEFTPAR LIST_OF_PARAMETERS RIGHTPAR STATEMENT 
                        | AUTO IDENTIFIER LEFTPAR LIST_OF_PARAMETERS RIGHTPAR STATEMENT   
                        | VARIABLE_TYPE IDENTIFIER LEFTPAR VARIABLE_TYPE IDENTIFIER COMMA DOT DOT DOT RIGHTPAR STATEMENT  
                '''                
    if(len(p) == 9 ):
        n = Node('FUNCTION_DECL')

        global global_scope, current_scope, errors
        if not (global_scope == current_scope):
            errors += 1
            print "Error : line", t.lexer.lineno,": Function", p[2], "cannot be declared here."
        else:
            new_var = current_scope.add_variable(p[2], p[1] ,-1)
            if(not new_var):
                errors += 1
                print "Error : line", t.lexer.lineno,": Function", p[2], "declared multiple times."
        n.add_child(p[1])
        n.add_child(Node(p[2]))
        n.add_child(Node(p[3]))
        n.add_child(p[4])
        n.add_child(Node(p[5]))
        n.add_child(p[6])
        n.add_child(p[7])
        n.add_child(p[8])
        p[0] = n
        # a = p[7].code
        print 'sasds', p[4].code
        p[0].code = "\n" + p[2] + "_begin: " + p[4].code + "\n" + p[4].code + "\n" + p[7].code + "\nreturn;\n\n"
        p[0].next = p[7].next        

    elif(len(p)==8):
        if(1==2):
            i = 0
        elif(1==5):
            i = 0
        else:
            n = Node('FUNCTION_DECL2')
            global global_scope, current_scope, errors
            if not (global_scope == current_scope):
                errors += 1
                print "Error : line", t.lexer.lineno, ": Function", p[2], "cannot be declared here."
            else:
                new_var = current_scope.add_variable(p[2], p[1].data,-1)
                if(not new_var):
                    errors += 1
                    print "Error : line", t.lexer.lineno, ": Function", p[2], "declared multiple times."
            n.add_child(p[1])
            n.add_child(Node(p[2]))
            n.add_child(Node(p[3]))
            n.add_child(Node(p[4]))
            n.add_child(p[5])
            n.add_child(p[6])
            n.add_child(p[7])
            p[0] = n
            p[0].code = "\n" + p[2] + "_begin:\n" + p[6].code + "\nreturn;\n\n"
            p[0].next = p[6].next

    elif(len(p) == 7 ):
        if(p[1]!= 'AUTO' ):
            i = 0
    else:
        i = 0


def p_FUNCTION_DECL2(p):
    ''' FUNCTION_DECL :  IDENTIFIER LEFTPAR LIST_OF_PARAMETERS RIGHTPAR  LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES
                        | IDENTIFIER LEFTPAR RIGHTPAR  LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES                        
                    '''
    if(len(p)==8):                    
        n = Node('FUNCTION_DECL')
        global global_scope, current_scope, errors
        if not (global_scope == current_scope):
            errors += 1
            print "Error : line", t.lexer.lineno, ": Function", p[1], "cannot be declared here."
        else:
            new_var = current_scope.add_variable(p[1], 'void',-1)
            if(not new_var):
                errors += 1
                print "Error : line", t.lexer.lineno, ": Function", p[1], "declared multiple times."
        n.add_child(Node("VOID"))
        n.add_child(Node(p[1]))
        n.add_child(Node(p[2]))
        n.add_child(p[3])
        n.add_child(Node(p[4]))
        n.add_child(p[5])
        n.add_child(p[6])
        n.add_child(p[7])
        p[0] = n
        p[0].code = "\n" + p[1] + "_begin: " + p[3].code + "\n" + p[6].code + "\nreturn;\n\n"
        p[0].next = p[6].next                    

    else:
        n = Node('FUNCTION_DECL3')
        global global_scope, current_scope, errors
        if not (global_scope == current_scope):
            errors += 1
            print "Error : line", t.lexer.lineno,": Function", p[1], "cannot be declared here."
        else:
            new_var = current_scope.add_variable(p[1], 'void',-1)
            if(not new_var):
                errors += 1
                print "Error : line", t.lexer.lineno,": Function", p[1], "declared multiple times."
        n.add_child(Node("VOID"))
        n.add_child(Node(p[1]))
        n.add_child(Node(p[2]))
        n.add_child(Node(p[3]))
        n.add_child(p[4])
        n.add_child(p[5])
        n.add_child(p[6])
        p[0] = n
        p[0].code = "\n" + p[1] + "_begin:\n" + p[5].code + "\nreturn;\n\n"
        p[0].next = p[5].next
def p_LIST_OF_PARAMETERS (p):
    ''' LIST_OF_PARAMETERS : VARIABLE_TYPE IDENTIFIER COMMA LIST_OF_PARAMETERS
                    | VARIABLE_TYPE IDENTIFIER
                    '''
    if(len(p)==3):
        n = Node('PARAMETERS1')
        n.add_child(p[1])
        n.add_child(Node(p[2]))
        p[0] = n
        p[0].code = p[1].place + " " + p[2]

    elif(len(p)==5):
        n = Node('PARAMETERS2')
        n.add_child(p[1])
        n.add_child(Node(p[2]))
        n.add_child(Node(p[3]))
        n.add_child(p[4])
        p[0] = n
        p[0].code = "(" + p[1].place + p[2] + "," + p[4].code + ")"            
    
# def p_PARAMETER_TYPE (p):
#     ''' PARAMETER_TYPE : VARIABLE_TYPE IDENTIFIER
#                         | VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER
#                         | REF VARIABLE_TYPE IDENTIFIER
#                         | REF VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER 
#                         | IMMUTABLE VARIABLE_TYPE IDENTIFIER
#                         | IMMUTABLE VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER 
                        
#                         '''

def p_TEMPLATES(p):
    ''' TEMPLATES : VARIABLE_TYPE IDENTIFIER LEFTPAR TEMP_PARAMETERS_TYPE RIGHTPAR LEFTPAR LIST_OF_TEMP_PARAMETERS RIGHTPAR  STATEMENT
    '''

def p_TEMP_PARAMETERS_TYPE(p):
    ''' TEMP_PARAMETERS_TYPE : TEMP_PARAMETERS_TYPE COMMA IDENTIFIER
                    | IDENTIFIER
                    '''


def p_LIST_OF_TEMP_PARAMETERS(p):
    ''' LIST_OF_TEMP_PARAMETERS : LIST_OF_TEMP_PARAMETERS COMMA IDENTIFIER IDENTIFIER
                    | IDENTIFIER IDENTIFIER
    '''

########## RULE STILL REMAINING ########################

def p_EXPRESSION_STATEMENT(p):
    ''' EXPRESSION_STATEMENT : EXPRESSION SEMICOLON

                        '''
    n = Node('EXPRESSION_STATEMENT')
    n.add_child(p[1])
    n.add_child(Node(p[2][0]))
    p[0] = n
    p[0].code = p[1].code                        
    p[0].next = p[1].next          



def p_DECISION_STATEMENT (p):
    '''DECISION_STATEMENT : IF LEFTPAR SIMPLE_EXPRESSION RIGHTPAR STATEMENT
                        | IF LEFTPAR SIMPLE_EXPRESSION RIGHTPAR STATEMENT ELSE STATEMENT
                        '''

        
def p_LOOP_STATEMENT(p):
    '''LOOP_STATEMENT : FOR_LOOP
                        | WHILE_LOOP
                        '''

def p_FOR_LOOP(p):
    '''FOR_LOOP :       FOR LEFTPAR EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHTPAR STATEMENT
                        | FOR LEFTPAR EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHTPAR LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES
                        '''                      
    if(len(p)==10):
                  
        n = Node('FOR_LOOP1')
        n.add_child(Node(p[1]))
        n.add_child(Node(p[2]))
        n.add_child(p[3])
        n.add_child(Node(p[4][0]))
        n.add_child(p[5])
        n.add_child(Node(p[6][0]))
        n.add_child(p[7])
        n.add_child(Node(p[8]))
        n.add_child(p[9])
        p[0] = n
        global labels
        labels += 1
        p[0].code = "\nlabel_" + str(labels) + ":\n"+ p[9].code + "\n" + p[7].code + "\ngoto label_" + str(labels+1) + ";\n"
        labels += 1
        p[0].code += p[3].code + "\ngoto label_"+ str(labels) + ";\nlabel_" + str(labels) + ":\n"  + "\nif" + p[5].code + "\n" + "\ngoto label_" + str(labels-1) + ";\ngoto " + str(p[3].next) + ";\n" 
        p[0].next = p[9].next

    elif(len(p)==12):
        n = Node('FOR_LOOP2')
        n.add_child(Node(p[1]))
        n.add_child(Node(p[2]))
        n.add_child(p[3])
        n.add_child(Node(p[4][0]))
        n.add_child(p[5])
        n.add_child(Node(p[6][0]))
        n.add_child(p[7])
        n.add_child(Node(p[8]))
        n.add_child(p[9])
        n.add_child(p[10])
        n.add_child(p[11])
        p[0] = n
        global labels
        labels += 1
        p[0].code = "\nlabel_" + str(labels) + ":\n"+ p[10].code + "\n" + p[7].code + "\ngoto label_" + str(labels+1) + ";\n"
        labels += 1
        p[0].code += p[3].code + "\ngoto label_"+ str(labels) + ";\nlabel_" + str(labels) + ":\n"  + "\nif" + p[5].code + "\n" + "\ngoto label_" + str(labels-1) + ";\ngoto " + str(p[3].next) + ";\n" 
        p[0].next = p[10].next


def p_FOR_LOOP2(p):
    '''FOR_LOOP :  FOR LEFTPAR EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHTPAR SEMICOLON                                  
                        '''                      
                          
    n = Node('FOR_LOOP3')
    n.add_child(Node(p[1]))
    n.add_child(Node(p[2]))
    n.add_child(p[3])
    n.add_child(Node(p[4][0]))
    n.add_child(p[5])
    n.add_child(Node(p[6][0]))
    n.add_child(p[7])
    n.add_child(Node(p[8]))
    n.add_child(Node(p[9][0]))
    p[0] = n
    global labels
    labels += 1
    p[0].code = "\nlabel_" + str(labels) + ":\n" + p[7].code + "\ngoto label_" + str(labels+1) + ";\n"
    labels += 1
    p[0].code += p[3].code + "\ngoto label_"+ str(labels) + ";\nlabel_" + str(labels) + ":\n"  + "\nif" + p[5].code + "\n" + "\ngoto label_" + str(labels-1) + ";\ngoto " + str(p[3].next) + ";\n" 
    p[0].next = p[7].next


def p_WHILE_LOOP(p):
    ''' WHILE_LOOP :     WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR STATEMENT
                        | WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES
                        | WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR SEMICOLON
                        '''
    if(len(p)== 6 and p[5]!='SEMICOLON'):
        n = Node('WHILE_LOOP1')
        n.add_child(Node(p[1]))
        n.add_child(Node(p[2]))
        n.add_child(p[3])
        n.add_child(Node(p[4]))
        n.add_child(p[5][0])
        p[0] = n
        global labels
        labels += 1
        p[0].code = "\nlabel_" + str(labels) + ":\n" + p[5].code + "\ngoto label_" + str(labels+1) + ";\n"
        labels += 1
        p[0].code += "\nlabel_" + str(labels) + ":\nif" + p[3].code + "\ngoto label_" + str(labels-1) + ";\ngoto " + str(p[5].next) + ";\n" 
        p[0].next = p[5].next

    elif(len(p)== 8):
        n = Node('WHILE_LOOP2')
        n.add_child(Node(p[1]))
        n.add_child(Node(p[2]))
        n.add_child(p[3])
        n.add_child(Node(p[4]))
        n.add_child(p[5])
        n.add_child(p[6])
        n.add_child(p[7])
        p[0] = n
        global labels
        labels += 1
        p[0].code = "label_" + str(labels) + ":\n" + p[6].code + "\ngoto label_" + str(labels+1) + ";\n"
        labels += 1
        p[0].code += "\nlabel_" + str(labels) + ":\nif" + p[3].code + "\ngoto label_" + str(labels-1) + ";\ngoto " + str(p[6].next) + ";\n" 
        p[0].next = p[6].next
    else:                        
        n = Node('WHILE_LOOP3')
        n.add_child(Node(p[1]))
        n.add_child(Node(p[2]))
        n.add_child(p[3])
        n.add_child(Node(p[4]))
        n.add_child(Node(p[5]))
        p[0] = n
        global labels
        labels += 1
        p[0].code = "\nlabel_" + str(labels) + ":\nif" + p[3].code + "\ngoto label_" + str(labels) + ";\ngoto " + str(p[3].next) + ";\n" 
        p[0].next = p[3].next

#---------------------------------------------------------------

def p_VARIABLE_DEF(p):
    ''' VARIABLE_DEF : ENUM ENUM_VARIABLE_TYPE LEFTBRACES LISTOF_VAR_DECLARATIONS RIGHTBRACES SEMICOLON
                            | ENUM COLON STRING_CONSTANT LEFTBRACES LISTOF_VAR_DECLARATIONS RIGHTBRACES 
                            | ENUM LEFTBRACES LISTOF_VAR_DECLARATIONS RIGHTBRACES
                        '''

def p_ENUM_VARIABLE_TYPE(p):
    ''' ENUM_VARIABLE_TYPE : ENUM
                        '''

def p_VARIABLE_DECLARATION(p):
    ''' VARIABLE_DECLARATION : VARIABLE_TYPE LISTOF_VAR_DECLARATIONS SEMICOLON
        '''
    n = Node('VARIABLE_DECLARATION')    
    n.add_child(p[1])
    n.add_child(p[2])
    n.add_child(Node(p[3]))
    global current_scope, offset
    for i in current_scope.variables:
        if(current_scope.variables[i]['type']=='NA'):
            current_scope.variables[i]['type'] = p[1].data
        if(current_scope.variables[i]['offset']=='NA'):
            current_scope.variables[i]['offset'] = offset
            if not current_scope.variables[i]['size']==-1:
                offset += type_size[p[1].data]
    p[0] = n
    p[0].code =  p[2].code
    p[0].next =  p[2].next    

def p_LISTOF_VAR_DECLARATIONS(p):
    '''LISTOF_VAR_DECLARATIONS : VAR_INITIALIZE COMMA LISTOF_VAR_DECLARATIONS 
                    | VAR_INITIALIZE
                    '''
    if(len(p)==4):
        n = Node('LISTOF_VAR_DECLARATIONS')
        global current_scope, errors
        new_var = current_scope.add_variable(p[1], 'NA')
        if(not new_var):
            errors += 1
            print "Error : line", t.lexer.lineno,": Variable", p[1], "declared multiple times in same scope."
        n.add_child(p[1])
        n.add_child(Node(p[2]))
        n.add_child(p[3])
        p[0] = n
        p[0].code = p[3].code
        p[0].next =  p[3].next 
    else:
        p[0] = p[1]
        p[0].code = p[1].code
        p[0].next = p[1].next

def p_VAR_INITIALIZE(p):
    '''VAR_INITIALIZE : VAR_DECLARATION_ID
                            |  VAR_DECLARATION_ID EQUALS EXPRESSION 
                            '''
    if(len(p)==4):
        n = Node(p[2][0])
        n.add_child(p[1])
        n.add_child(p[3])
        p[0] = n
        p[0].code = p[3].code + "\n_x1 = " + p[3].place + ";\n" + p[1].code+ " = _x1;\n"
        p[0].next = p[3].next
    else:
        p[0] = p[1]
        p[0].code = p[1].code
        p[0].next = p[1].next

def p_VAR_DECLARATION_ID(p):
    ''' VAR_DECLARATION_ID : IDENTIFIER
                    | IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET
                    | IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET LEFTBRACKET INT_CONSTANT RIGHTBRACKET
                    | LEFTBRACKET INT_CONSTANT RIGHTBRACKET IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET   
                    | LEFTBRACKET INT_CONSTANT RIGHTBRACKET LEFTBRACKET INT_CONSTANT RIGHTBRACKET IDENTIFIER
                    
                    '''         #inp[string] array1;
#  SEE IF NEEED OF NODE(VAR_DE)
    if(len(p) == 2 ):
        # print 'sahil  ', p[1]
        global current_scope, errors
        new_var = current_scope.add_variable(p[1], 'NA')
        if(not new_var):
            errors += 1
            print "Error : line", t.lexer.lineno,": Variable", p[1], "declared multiple times in same scope."

        p[0] = Node(p[1])
        p[0].code = ""
        p[0].place = p[1][0]

        #print p[1]
    elif(len(p) == 5):
        n = Node('VAR_DECLARATION_ID2')
        global current_scope, errors
        new_var = current_scope.add_variable(p[1], 'NA', p[3].data)
        if(not new_var):
            errors += 1
            print "Error : line", t.lexer.lineno,": Variable", p[1], "declared multiple times in same scope."
        n.add_child(Node(p[1]))
        n.add_child(Node(p[2]))
        n.add_child(p[3])
        n.add_child(Node(p[4]))
        p[0] = n
        global mass
        mass += 1
        new_var = "_t" + str(mass)
        p[0].code = p[3].code + "\n"
        p[0].place = p[1] + "[" +  new_var + "]"
        p[0].next = p[3].next 

# DYNAMIC ARRAY NOT SUPPORTED
    else:
        n = Node('VAR_DECLARATION_ID3')

        # elif(p[4]=='LEFTBRACKET'):      #a[1][1]  [1]a[2] [1][2]a

        # else:
            
                    
def p_VARIABLE_TYPE (p):
    ''' VARIABLE_TYPE : INT 
                      | FLOAT
                      | CHAR
                      | BOOL
                      | LONG                      
                      | DOUBLE
                      | VOID
                      | SHORT
                      '''
    p[0] = Node(p[1])
    p[0].code = ''
    if(not (p[0]== 'INT' or p[0] =='FLOAT') ):
        p[0].place = p[1]    


def p_RETURN_STATEMENT(p):
    '''RETURN_STATEMENT : RETURN EXPRESSION SEMICOLON
                    | RETURN SEMICOLON
                    '''
    if(len(p)==3):                    
        n = Node('RETURN_STATEMENT1')    
        n.add_child(Node(p[1]))
        n.add_child(Node(p[2][0]))
        p[0] = n
        p[0].code = 'return ' + ";\n"                    
    else:
        n = Node('RETURN_STATEMENT2')
        n.add_child(Node(p[1]))
        n.add_child(p[2])
        n.add_child(Node(p[3][0]))
        p[0] = n
        p[0].code = p[2].code + "\n_x1 = " + p[2].place + ";\nreturn _x1;\n"
        p[0].next = p[2].next   

def p_BREAK_STATEMENT(p):
    ''' BREAK_STATEMENT : BREAK SEMICOLON
                    '''
    n = Node('BREAK_STATEMENT')
    n.add_child(Node(p[1]))
    n.add_child(Node(p[2][0]))
    p[0] = n
    p[0].code = 'break ' + ";\n"    

# def p_CONTINUE_STATEMENT(p):
#     ''' CONTINUE_STATEMENT : CONTINUE_STATEMENT SEMICOLON
#                     '''
#     n = Node('CONTINUE_STATEMENT')
#     n.add_child(Node(p[1]))
#     n.add_child(Node(p[2]))
#     p[0] = n
#     p[0].code = 'continue ' + ";\n"    


def p_EXPRESSION (p):
    ''' EXPRESSION : DATA_OBJECT EQUALS EXPRESSION
                    | DATA_OBJECT PLUS_EQUAL EXPRESSION
                    | DATA_OBJECT MINUS_EQUAL EXPRESSION
                    | DATA_OBJECT NOR_EQUAL EXPRESSION
                    | DATA_OBJECT OR_EQUAL EXPRESSION                     
                    | SIMPLE_EXPRESSION
                    | LEFTPAR EXPRESSION RIGHTPAR
                    '''
    if(len(p)==2):
        p[0] = p[1]
        p[0].code = p[1].code
        p[0].next = p[1].next        

    elif(len(p)==4):
        n = Node(p[2][0])
        n.add_child(p[1])
        n.add_child(p[3])
        p[0] = n
        if(p[2]=='EQUALS'):
            p[0].code = p[1].code + p[3].code + "\n" + p[1].place + " = " + p[3].place + ";\n"
            p[0].place = p[1].place
        else:
            global mass
            mass += 1
            new_var = "_t" + str(mass)
            p[0].code = p[1].code + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = "+ p[3].place+ ";\n" + new_var + " = _x1 + _x2;\n" + p[1].place + " = " + new_var + ";\n"
            p[0].place = new_var
        p[0].next = p[3].next


    # elif(len(p)==3):
    #     if(p[2] == 'PLUSPLUS'):
    #         n = NODE('EXPRESSION')
    #         n.add_child(p[1])
    #         n1 = Node(p[2])
    #         n1.code = " + 1;\n"
    #         n1.place = ' - 1'
    #         n.add_child(n1)

    #         p[0] = n
    #         p[0].code = p[1] + " = " + p[1] + p[2].code
    #         p[0].place = p[1] + p[2].place
    #         p[0].next = p[2].next

    #     elif(p[2] == 'MINUSMINUS'):
    #         n = NODE('EXPRESSION')
    #         n.add_child(p[1])
    #         n1 = Node(p[2])
    #         n1.code = " - 1;\n"
    #         n1.place = ' + 1'

    #         n.add_child(n1)

    #         p[0] = n
    #         p[0].code = p[1] + " = " + p[1] + p[2].code
    #         p[0].place = p[1] + p[2].place
    #         p[0].next = p[2].next
    
    else:
        n = Node(p[2])
        n.add_child(p[1])
        n.add_child(p[3])        
        p[0] = n
        global mass
        mass += 1
        new_var = "_t" + str(mass)
        p[0].code = p[1].code + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = "+ p[3].place+ ";\n" + new_var + " = _x1 + _x2;\n" + p[1].place + " = " + new_var + ";\n"
        p[0].place = new_var
        p[0].next = p[3].next


def p_SIMPLE_EXPRESSION (p):
    ''' SIMPLE_EXPRESSION : SIMPLE_EXPRESSION AND RELATIONAL_EXPRESSION
                        | SIMPLE_EXPRESSION OR RELATIONAL_EXPRESSION   
                        | RELATIONAL_EXPRESSION
                        '''
    if(len(p)==2):
        p[0] = p[1]
        p[0].code = p[1].code
        p[0].next = p[1].next        
        
    else:
        if(p[2]=='AND'):
            n = Node(p[2])
            n.add_child(p[1])
            n.add_child(p[3])
            p[0] = n
            global labels, mass
            labels += 1
            mass += 1
            new_var = "_t" + str(mass)
            false_1 = "\nlabel_" + str(labels) + ":\n" + new_var + " = 0;\n"
            p[0].code = p[1].code + "\n" + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = " + p[3].place + ";\n"
            p[0].code += "if _x1 == 0 goto label_" + str(labels) + ";\nif _x2 == 0 goto label_" + str(labels) + ";\n"
            p[0].code += new_var + " = 1;\ngoto label_" + str(labels+1) + ";\n" + false_1 + "\nlabel_" + str(labels+1) + ":\n"
            labels += 1
            p[0].place = new_var
            p[0].next = p[3].next    
        else:
            n = Node(p[2])
            n.add_child(p[1])
            n.add_child(p[3])
            p[0] = n
            global labels, mass
            labels += 1
            mass += 1
            new_var = "_t" + str(mass)
            true_1 = "\nlabel_" + str(labels) + ":\n" + new_var + " = 1;\n"
            p[0].code = p[1].code + "\n" + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = " + p[3].place + ";\n"
            p[0].code += "if _x1 > 0 goto label_" + str(labels) + ";\nif _x2 > 0 goto label_" + str(labels) + ";\n"
            p[0].code += new_var + " = 0;\ngoto label_" + str(labels+1) + ";\n" + true_1 + "\nlabel_" + str(labels+1) + ":\n"
            labels += 1
            p[0].place = new_var
            p[0].next = p[3].next            

def p_RELATIONAL_EXPRESSION (p):
    ''' RELATIONAL_EXPRESSION : SUM_EXPRESSION LESSER SUM_EXPRESSION
                        | SUM_EXPRESSION GREATER SUM_EXPRESSION
                        | SUM_EXPRESSION LESSER_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION GREATER_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION NOT_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION EQUAL_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION
                        '''
    if(len(p)==2):
        p[0] = p[1]
        p[0].code = p[1].code
        p[0].next = p[1].next        
    else:
        # print 'sahil22' , p[2]                       
        if(p[2][1]=='LESSER'):
            n = Node(p[2])
            n.add_child(p[1])
            n.add_child(p[3])
            p[0] = n
            global mass
            mass += 1
            new_var = "_t" + str(mass)
            p[0].code = "\n" + new_var + " = 0;\n" + p[1].code + "\n" + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = " + p[3].place + ";\n"
            p[0].code += "if _x1 < _x2 " + new_var + " = 1;\n" 
            p[0].place = new_var
            p[0].next = p[3].next

        elif(p[2][1]=='GREATER'):
            n = Node(p[2])
            n.add_child(p[1])
            n.add_child(p[3])
            p[0] = n
            global mass
            mass += 1
            new_var = "_t" + str(mass)
            p[0].code = "\n" + new_var + " = 0;\n" + p[1].code + "\n" + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = " + p[3].place + ";\n"
            p[0].code += "if _x1 > _x2 " + new_var + " = 1;\n" 
            p[0].place = new_var
            p[0].next = p[3].next

        elif(p[2][1]=='LESSER_EQUAL'):
            n = Node(p[2])
            n.add_child(p[1])
            n.add_child(p[3])
            p[0] = n
            global mass
            mass += 1
            new_var = "_t" + str(mass)
            p[0].code = "\n" + new_var + " = 1;\n" + p[1].code + "\n" + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = " + p[3].place + ";\n"
            p[0].code += "if _x1 > _x2 " + new_var + " = 0;\n" 
            p[0].place = new_var
            p[0].next = p[3].next

        elif(p[2][1]=='GREATER_EQUAL'):
            n = Node(p[2])
            n.add_child(p[1])
            n.add_child(p[3])
            p[0] = n
            global mass
            mass += 1
            new_var = "_t" + str(mass)
            p[0].code = "\n" + new_var + " = 1;\n" + p[1].code + "\n" + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = " + p[3].place + ";\n"
            p[0].code += "if _x1 < _x2 " + new_var + " = 0;\n" 
            p[0].place = new_var
            p[0].next = p[3].next    
        elif(p[2][1]=='NOT_EQUAL'):
            n = Node(p[2])
            n.add_child(p[1])
            n.add_child(p[3])
            p[0] = n
            global mass
            mass += 1
            new_var = "_t" + str(mass)
            p[0].code = "\n" + new_var + " = 1;\n" + p[1].code + "\n" + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = " + p[3].place + ";\n"
            p[0].code += "if _x1 == _x2 " + new_var + " = 0;\n" 
            p[0].place = new_var
            p[0].next = p[3].next            

        elif(p[2][1]=='EQUAL_EQUAL'):        
            n = Node(p[2])
            n.add_child(p[1])
            n.add_child(p[3])
            p[0] = n
            global mass
            mass += 1
            new_var = "_t" + str(mass)
            p[0].code = "\n" + new_var + " = 0;\n" + p[1].code + "\n" + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = " + p[3].place + ";\n"
            p[0].code += "if _x1 == _x2 " + new_var + " = 1;\n" 
            p[0].place = new_var
            p[0].next = p[3].next
                
def p_SUM_EXPRESSION(p):
    ''' SUM_EXPRESSION : SUM_EXPRESSION PLUS UNARY_EXPRESSION
                        | SUM_EXPRESSION MINUS UNARY_EXPRESSION
                        | SUM_EXPRESSION STAR UNARY_EXPRESSION
                        | SUM_EXPRESSION DIVIDE UNARY_EXPRESSION
                        | SUM_EXPRESSION MOD UNARY_EXPRESSION                         
                        | UNARY_EXPRESSION
                        '''
    if(len(p)==2):
        p[0] = p[1]
        p[0].code = p[1].code
        p[0].next = p[1].next

    else:                    
        n = Node(p[2][0])
        n.add_child(p[1])
        n.add_child(p[3])
        p[0] = n
        global mass
        mass += 1
        new_var = "_t" + str(mass)
        p[0].code = p[1].code + "\n" + p[3].code + "\n_x1 = " + p[1].place + ";\n_x2 = " + p[3].place + ";\n"
        if(p[2]=='PLUS'):
            p[0].code += new_var + " = _x1 + _x2;\n"
        elif(p[2]=='MINUS'):
            p[0].code += new_var + " = _x1 - _x2;\n"
        elif(p[2]=='STAR'):
            p[0].code += new_var + " = _x1 * _x2;\n"
        elif(p[2]=='DIVIDE'):
            p[0].code += new_var + " = _x1 / _x2;\n"
        elif(p[2]=='MOD'):
            p[0].code += new_var + " = _x1 % _x2;\n"
        
        p[0].place = new_var
        p[0].next = p[3].next 

            
def p_UNARY_EXPRESSION(p):
    ''' UNARY_EXPRESSION : UNARY_OPERATOR UNARY_EXPRESSION
                        | UNARY_EXPRESSION UNARY_OPERATOR 
                        | factor
                        '''
    if(len(p)==2):
        p[0] = p[1]
        p[0].code = p[1].code
        p[0].next = p[1].next
    else:
        if(p[1].code == " + 1;\n" or p[1].code == " - 1;\n"):
            n = Node('UNARY_EXPRESSION1')
            n.add_child(p[1])
            n.add_child(Node(p[2]))
            p[0] = n
            p[0].code = p[2].code + " = " + p[2].code + p[1].code
            p[0].place = p[2]
            p[0].next = p[1].next

        elif(p[2].code == " + 1;\n" or p[2].code == " - 1;\n"):  
            n = Node('UNARY_EXPRESSION2')
            n.add_child(Node(p[1]))
            n.add_child(p[2])
            p[0] = n
            p[0].code = p[1].code + " = " + p[1].code + p[2].code
            p[0].place = p[1].place + p[2].place
            p[0].next = p[2].next

def p_UNARY_OPERATOR(p):
    '''UNARY_OPERATOR : PLUSPLUS
                | MINUSMINUS
                '''
    # print 'PPPPPP'                
    if(p[1][1]=='PLUSPLUS'):        
        p[0] = Node(p[1])
        p[0].code = " + 1;\n"
        p[0].place = ' - 1'    
    elif(p[1][1] == 'MINUSMINUS'):
        p[0] = Node(p[1])
        p[0].code = " - 1;\n"
        p[0].place = ' + 1'


def p_factor(p):
    ''' factor : DATA_OBJECT
                | OTHER_EXPR
                '''
    p[0] = p[1]
    p[0].code = p[1].code
    p[0].next = p[1].next                

def p_DATA_OBJECT(p):
    ''' DATA_OBJECT : IDENTIFIER
                | IDENTIFIER LEFTBRACKET EXPRESSION RIGHTBRACKET
                | IDENTIFIER LEFTBRACKET EXPRESSION RIGHTBRACKET LEFTBRACKET EXPRESSION RIGHTBRACKET                
                |  IDENTIFIER DOT IDENTIFIER
                '''
#  DOUBT
    if(len(p)==2):
        p[0] = Node(p[1])
        p[0].code = ""
        p[0].place = p[1][0]

    elif(len(p)==5): 
        n = Node('DATA_OBJECT1')
        n.add_child(Node(p[1]))
        n.add_child(Node(p[2][0]))
        n.add_child(p[3])
        n.add_child(Node(p[4][0]))
        p[0] = n
        global mass
        mass += 1
        new_var = "_t" + str(mass)
        p[0].code = p[3].code + "\n" + new_var + " = " + p[3].place + ";\n"
        p[0].place = p[1] + "[" + new_var + "]"
        p[0].next = p[3].next                         
    elif(len(p)==8):
        i = 0
# DOUBLE ARRAY NOT HANDLED RIGHT NOW
    else:
        i = 0
# CLASS FUNCTIONS NOT HANDLED

def p_OTHER_EXPR(p):
    ''' OTHER_EXPR : LEFTBRACKET LIST_OF_CONSTANTS RIGHTBRACKET
                    | CONSTANT                    
                    | FUNCTION_INSTANCE                    
        '''                    
    if(len(p)==2):
        p[0] = p[1]
        p[0].code = p[1].code
        p[0].next = p[1].next 


def p_FUNCTION_INSTANCE (p):
    ''' FUNCTION_INSTANCE : IDENTIFIER LEFTPAR FUNC_ARGUMENTS RIGHTPAR
            '''

def p_FUNC_ARGUMENTS(p):
    ''' FUNC_ARGUMENTS : LIST_OF_FUNCTION_ARGUMENTS
            |
            '''    
        
def p_LIST_OF_FUNCTION_ARGUMENTS(p):
    ''' LIST_OF_FUNCTION_ARGUMENTS : LIST_OF_FUNCTION_ARGUMENTS COMMA EXPRESSION
                    | EXPRESSION
                    '''

def p_LIST_OF_CONSTANTS(p):
    ''' LIST_OF_CONSTANTS : STRING_CONSTANT COLON SIMPLE_EXPRESSION COMMA LIST_OF_CONSTANTS
                            | STRING_CONSTANT COLON SIMPLE_EXPRESSION
                    '''

def p_CONSTANT(p):
    ''' CONSTANT : INT_CONST
                    | FLOAT_CONST
                    | CHAR_CONST
                    | STR_CONST
                    '''
    if(len(p)==2):
        p[0] = p[1]
        p[0].code = p[1].code
        p[0].next = p[1].next 

def p_INT_CONST(p):
    ''' INT_CONST : INT_CONSTANT
                '''
    p[0] = Node(p[1][0])
    p[0].code = ""
    p[0].place = p[1][0]

def p_FLOAT_CONST (p):
    ''' FLOAT_CONST : FLOAT_CONSTANT
                '''
    p[0] = Node(p[1][0])
    p[0].code = ""
    p[0].place = p[1][0]

def p_CHAR_CONST (p):
    ''' CHAR_CONST : CHAR_CONSTANT
                '''
    p[0] = Node(p[1][0])
    p[0].code = ""
    p[0].place = p[1][0]


def p_STR_CONST (p):
    ''' STR_CONST : STRING_CONSTANT
                '''
    p[0] = Node(p[1][0])
    p[0].code = ""
    p[0].place = p[1][0]
    
def p_LEFTBRACES(p):
    ''' LEFTBRACES : LEFTBRACE
                    '''
    p[0] = Node(p[1])
    p[0].code = ""
    global current_scope, tableux
    new_scope = Table(tableux)
    tableux += 1
    current_scope.add_table(new_scope)
    current_scope = new_scope

def p_RIGHTBRACES(p):
    ''' RIGHTBRACES : RIGHTBRACE
                    '''
    p[0] = Node(p[1])
    p[0].code = ""
    global current_scope
    current_scope = current_scope.parent
    
def p_error(p):
    print "Parse Time Error!! at ",t.type," ", t.value," ", t.lineno

import logging
logging.basicConfig(
    level=logging.INFO,
    filename="parselog.txt"
)

parser = yacc.yacc()
data =''' int main(int c, int x) { int i , j=1,k=0 ; k = i+j; } '''
data1 = ' int i = 2+4 ; '

print parser.parse(data, debug=logging.getLogger())
# print parser.parse(data, debug=logging.getLogger())