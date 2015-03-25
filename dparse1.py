import os,sys
import time
import dlex
import ply.yacc as yacc
tokens = dlex.tokens

def p_startProgram(t):
    ''' Program : LIST_OF_DECLARATIONS
                '''
    t[0] = t[1]
    #print t[0]

def p_LIST_OF_DECLARATIONS(t):
    '''LIST_OF_DECLARATIONS : LIST_OF_DECLARATIONS DECLARATION
                        | DECLARATION
                        '''                        
    if( len(t) == 3):
        t[0]=t[1]+[t[2]]
    else:
        t[0] = t[1]
        # print t[0]

    #print t[0]
# RIGHT NOW ONLY VAR_DECLARATION WORKING SO WE ARE USING ONLY THIS RULE
def p_DECLARATION(t):
    ''' DECLARATION : VARIABLE_DECLARATION
                    | function_definition
                    | function_declaration
                    | variable_definition
                    | templates
                    '''
    t[0]=t[1]
    # print t[1],'sahil'
    #print t[0]

def p_templates(t):
    ''' templates : VARIABLE_TYPE IDENTIFIER LEFTPAR temp_params_type RIGHTPAR LEFTPAR temp_params_list RIGHTPAR  statement  
    '''
    t[0] = (t[1] , t[4] , t[7])   
def p_temp_param_type(t):
    ''' temp_params_type : temp_params_type COMMA IDENTIFIER
                    | IDENTIFIER
                    '''

    # global parametersymboltable
    if(len(t) == 4):
        t[0] = t[1] + [t[3]]
        # parametersymboltable.insert(t[3]['IDENTIFIER'],{'TYPE':t[3]['TYPE'],'ARRAY':t[3]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':0,'STATIC':0})
    else:
        t[0] =  [t[1]]
        # parametersymboltable.insert(t[1]['IDENTIFIER'],{'TYPE':t[1]['TYPE'],'ARRAY':t[1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1': 0,'STATIC':0})

def p_temp_params_list(t):
    ''' temp_params_list : temp_params_list COMMA IDENTIFIER IDENTIFIER
                    | IDENTIFIER IDENTIFIER
    '''

    # global parametersymboltable
    if(len(t) == 5):
        t[0] = t[1] + [t[3]]
        # parametersymboltable.insert(t[3]['IDENTIFIER'],{'TYPE':t[3]['TYPE'],'ARRAY':t[3]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':0,'STATIC':0})
    else:
        t[0] =  [t[1]]
        # parametersymboltable.insert(t[1]['IDENTIFIER'],{'TYPE':t[1]['TYPE'],'ARRAY':t[1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1': 0,'STATIC':0})

#----------------------------------------------------------------

def p_function_definitions(t):
    ''' function_definition : VARIABLE_TYPE IDENTIFIER LEFTPAR params RIGHTPAR SEMICOLON
                            | IDENTIFIER LEFTPAR params RIGHTPAR SEMICOLON
                            
                            '''
    t[0] = (t[1],t[2],t[4])


def p_params(t):
    ''' params : param_list
                |
                '''
    #print t[1]
    if(len(t)==2):
        t[0] = t[1]
    else:
        t[0] = []
    
def p_param_list (t):
    ''' param_list : param_list COMMA param_type_node
                    | param_type_node
                    '''

    # global parametersymboltable
    if(len(t) == 4):
        t[0] = t[1] + [t[3]]
        # parametersymboltable.insert(t[3]['IDENTIFIER'],{'TYPE':t[3]['TYPE'],'ARRAY':t[3]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':0,'STATIC':0})
    else:
        t[0] =  [t[1]]
        # parametersymboltable.insert(t[1]['IDENTIFIER'],{'TYPE':t[1]['TYPE'],'ARRAY':t[1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1': 0,'STATIC':0})
    
def p_param_type_node (t):
    ''' param_type_node : VARIABLE_TYPE IDENTIFIER
                        | VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER
                        | REF VARIABLE_TYPE IDENTIFIER
                        | REF VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER 
                        | IMMUTABLE VARIABLE_TYPE IDENTIFIER
                        | IMMUTABLE VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER 
                        
                        '''
    t[0] = (t[2], t[1])
    


    if (len(t) == 2):
        t[0] = t[1]
    else:
        t[0] = t[1]
# ---------------------------------------------------------------------------------------------

def p_function_declaration(t):
    ''' function_declaration : VARIABLE_TYPE IDENTIFIER LEFTPAR params RIGHTPAR statement 
                            | IDENTIFIER LEFTPAR params RIGHTPAR statement
                            | PURE VARIABLE_TYPE IDENTIFIER LEFTPAR params RIGHTPAR statement   
                            | VARIABLE_TYPE IDENTIFIER LEFTPAR params RIGHTPAR NOTHROW statement  
                            | REF VARIABLE_TYPE IDENTIFIER LEFTPAR params RIGHTPAR statement  
                            | AUTO IDENTIFIER LEFTPAR params RIGHTPAR statement   
                            | VARIABLE_TYPE IDENTIFIER LEFTPAR VARIABLE_TYPE IDENTIFIER COMMA DOT DOT DOT RIGHTPAR statement   
                            '''
    t[0] = (t[5])
    print (t[6])
    # print 'function declaration'

def p_statement(t):
    ''' statement : expression_stmt
                    | compound_stmt
                    | decision_stmt
                    | iteration_stmt
                    | RETURN_STATEMENT
                    | BREAK_STATEMENT
                    '''
    t[0] = {'NODE_TYPE':'STATEMENT','CHILD':t[1]}
    # print 'statement', t[0]

def p_expression_stmt(t):
    ''' expression_stmt : EXPRESSION SEMICOLON
                        
                        '''
    if(len(t) == 2):
        t[0] = {'NODE_TYPE':'expression_stmt', 'EXPRESSION':''}
    else:
        t[0] = {'NODE_TYPE':'expression_stmt', 'EXPRESSION':t[1]}
    # print 'expression ' , t[0]    

def p_compound_stmt(t):
    ''' compound_stmt : LEFTBRACE local_declarations statement_list RIGHTBRACE
                        '''
    t[0] = {'NODE_TYPE':'compound_stmt','STATEMENTS': t[3],'LOCAL_DECL': t[2]}

def p_local_declarations(t):
    ''' local_declarations : local_declarations scoped_var_declaration
                            |
                            '''
    if( len(t) == 3 ):
        t[0] = t[1] + [t[2]]
        #t[0] = t[1] + t[2]
    else:
        t[0] = []

          
def p_scoped_var_declaration(t):
    '''scoped_var_declaration : scoped_type_specifier LISTOF_VAR_DECLARATIONS SEMICOLON
                               '''
    t[0] = t[1]     
    # t[0]={'NODE_TYPE':'scoped_var_declaration','STATIC':t[1]['STATIC'],'VAR_TYPE':t[1]['TYPE'], 'VAR_LIST': t[2]}

    # table = 'LOCAL'
    # initialise = ''
    # if(t[1]['TYPE'] == 'float'):
    #     table = 'GLOBAL'
    #     initialise = {'TYPE': 'float', 'NODE_TYPE': 'expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'simple_expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'and_expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'unary_rel_expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'rel_expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'sum_expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'term', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'unary_expression', 'OP': '', 'EXPRESSION': {'SUBTYPE': 'immutable', 'NODE_TYPE': 'factor', 'EXPRESSION': {'SUBTYPE': 'Constant', 'NODE_TYPE': 'immutable', 'TYPE': 'float', 'VALUE': '0.0'}, 'TYPE': 'float'}, 'factor': 1}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OPS': ''}
    # for x in t[2]:
    #     if (currentSymbolTable.insert(x['ID'],{'TYPE':t[1]['TYPE'],'STATIC':t[1]['STATIC'],'ARRAY': x['ARRAY'],'INDEX1':x['INDEX1'],'INDEX2':x['INDEX2'],'SCOPETYPE':table}) == False):
    #         print x['ID'],': Variable already declared '
    #         sys.exit()
    #     else:
    #         x['SCOPETYPE'] = 'LOCAL'
    #         check = currentSymbolTable.lookupCurrentTable(x['ID'])
    #         #print check
    #         x['offset'] = check['offset']
    #         x['TABLE'] = check['TABLE']
    #         x['TYPE'] = t[1]['TYPE']
    #         x['STATIC'] = t[1]['STATIC']
    #         if (x['INITIALISED'] == ''):
    #             x['INITIALISED'] = initialise
            #print x['offset']
def p_scoped_type_specifier(t):
    ''' scoped_type_specifier : STATIC VARIABLE_TYPE
                                | VARIABLE_TYPE
                                '''
  
def p_statement_list(t):
    ''' statement_list : statement_list statement
                        |
                        '''
    if ( len(t) == 3):
        t[0] = t[1] + [t[2]]
    else :
        t[0] = ['']

def p_decision_stmt (t):
    '''decision_stmt : IF LEFTPAR SIMPLE_EXPRESSION RIGHTPAR statement
                        | IF LEFTPAR SIMPLE_EXPRESSION RIGHTPAR statement ELSE statement
                        '''

    if( len(t) == 6):
        t[0] = {'NODE_TYPE':'IF', 'CONDITION': t[3], 'ifProgram': t[5], 'elseProgram':''}
        #print t[0]
    else:
        t[0] = {'NODE_TYPE':'IF_ELSE', 'CONDITION': t[3], 'ifProgram': t[5], 'elseProgram': t[7]}
        #print t[0]
        
def p_iteration_stmt (t):
    '''iteration_stmt : WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR statement
                        | FOR LEFTPAR EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHTPAR   statement
                        | DO statement WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR SEMICOLON 
                        '''
    if( len(t) == 6):
        t[0] = {'NODE_TYPE':'WHILE', 'CONDITION': t[3], 'partProgram':t[5]}

    elif ( len(t) == 10):
        t[0] = {'NODE_TYPE':'FOR', 'CONDITION': t[5], 'INITIALISE': t[3], 'UPDATE': t[7], 'partProgram': t[9]}

    else:
        t[0] = {'NODE_TYPE':'DO', 'CONDITION': t[5],'partProgram': t[2]}


#---------------------------------------------------------------

def p_variable_definition(t):
    ''' variable_definition : ENUM ENUM_VARIABLE_TYPE LEFTBRACE LISTOF_VAR_DECLARATIONS RIGHTBRACE SEMICOLON
                            | ENUM COLON VARIABLE_TYPE LEFTBRACE LISTOF_VAR_DECLARATIONS RIGHTBRACE 
                            | ENUM LEFTBRACE LISTOF_VAR_DECLARATIONS RIGHTBRACE
                        '''
    # if(len(t)==2):
    #     t[0]=t[1]
    # else: 
    t[0]=t[4]     
    #print t[0]        
def p_ENUM_VARIABLE_TYPE(t):
    ''' ENUM_VARIABLE_TYPE : IDENTIFIER
                        '''
    # if(len(t)==2):
    #     t[0]=t[1]
    # else: 
    t[0]=t[1]     
    #print t[0]        

def p_VARIABLE_DECLARATION(t):
    '''VARIABLE_DECLARATION : VARIABLE_TYPE LISTOF_VAR_DECLARATIONS SEMICOLON
                        '''
    # if(len(t)==2):
    #     t[0]=t[1]
    # else: 
    t[0]=t[2]     
    #print t[0]        

def p_LISTOF_VAR_DECLARATIONS(t):
    '''LISTOF_VAR_DECLARATIONS : LISTOF_VAR_DECLARATIONS COMMA VAR_INITIALIZE
                    | VAR_INITIALIZE
                    '''

    if( len(t) == 4):
        t[0] = t[1] + [t[3]]
    else:
        #print 'sahil'
        #print t[1]
        t[0] = [t[1]]
    #print t[0]    

def p_VAR_INITIALIZE(t):
    '''VAR_INITIALIZE : VAR_DECLARATION_ID
                            |  VAR_DECLARATION_ID EQUALS EXPRESSION 
                            '''
    
    if( len(t) == 2):
        t[0] = t[1]
        
    elif ( len(t) == 4):
        t[0] = (t[1],t[3])
#    print t[0]

def p_VAR_DECLARATION_ID(t):
    ''' VAR_DECLARATION_ID : IDENTIFIER
                    | IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET
                    | IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET LEFTBRACKET INT_CONSTANT RIGHTBRACKET
                    | LEFTBRACKET INT_CONSTANT RIGHTBRACKET IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET   
                    | LEFTBRACKET RIGHTBRACKET IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET
                    | LEFTBRACKET INT_CONSTANT RIGHTBRACKET LEFTBRACKET INT_CONSTANT RIGHTBRACKET IDENTIFIER
                    | LEFTBRACKET VARIABLE_TYPE RIGHTBRACKET IDENTIFIER 
                    '''         #int[string] array1;
#    print 'sahil'
    if(len(t) == 2 ):
        t[0] = (t[1])
    elif(len(t) == 5):
        t[0] = (t[1],t[3])
    else:
        t[0] = (t[1],t[3],t[6])


def p_VARIABLE_TYPE (t):
    ''' VARIABLE_TYPE : INT 
                      | FLOAT
                      | CHAR
                      | BOOL
                      | LONG                      
                      | DOUBLE
                      | VOID
                      | STRING
                      | ENUM
                      '''
    t[0] = t[1]
    #print t[0]


def p_RETURN_STATEMENT(t):
    '''RETURN_STATEMENT : RETURN EXPRESSION SEMICOLON
                    | RETURN SEMICOLON
                    '''
    if(len(t) == 3):
        t[0] = ('RETURN')
    else:
        t[0] = ('RETURN',t[2])

def p_BREAK_STATEMENT(t):
    ''' BREAK_STATEMENT : BREAK SEMICOLON
                    '''
    t[0]=('BREAK')



def p_EXPRESSION (t):
    ''' EXPRESSION : DIFF_ID EQUALS EXPRESSION
                    | DIFF_ID PLUSPLUS
                    | DIFF_ID MINUSMINUS
                    | DIFF_ID PLUS_EQUAL EXPRESSION
                    | DIFF_ID MINUS_EQUAL EXPRESSION
                    | SIMPLE_EXPRESSION
                    | DIFF_ID NOR_EQUAL EXPRESSION
                    '''
    if(len(t)==4):
         t[0] = (t[2],t[1],t[3])   

    elif(len(t)==3):
        t[0] = (t[2],t[1])

    else:
        t[0] = t[1]

def p_SIMPLE_EXPRESSION (t):
    ''' SIMPLE_EXPRESSION : ANDOP_EXPRESSION
                            | SIMPLE_EXPRESSION OR ANDOP_EXPRESSION
                            '''
    if(len(t)==4):
        t[0] = (t[2][0],t[1],t[3])

    else:
        t[0] = t[1]
    #print t[0]    


def p_ANDOP_EXPRESSION (t):
    ''' ANDOP_EXPRESSION : ANDOP_EXPRESSION AND UNARY_RELATION_EXPRESSION
                        | UNARY_RELATION_EXPRESSION
                        '''
    if(len(t)==4):
        t[0] = (t[2][0],t[1],t[3])
    else:
        t[0] = t[1]
    #print t[0]    


def p_UNARY_RELATION_EXPRESSION(t):
    '''UNARY_RELATION_EXPRESSION : NOT UNARY_RELATION_EXPRESSION
                            | RELATIONAL_EXPRESSION
                            '''
    if(len(t) == 3):
        t[0] = t[2]
    else:
        t[0] = t[1]


def p_RELATIONAL_EXPRESSION (t):
    ''' RELATIONAL_EXPRESSION : SUM_EXPRESSION LESSER SUM_EXPRESSION
                        | SUM_EXPRESSION GREATER SUM_EXPRESSION
                        | SUM_EXPRESSION LESSER_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION GREATER_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION NOT_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION EQUAL_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION
                        '''
    if(len(t)==4):
        t[0] = (t[2][0],t[1],t[3])
    else:
        t[0] = t[1]


def p_SUM_EXPRESSION(t):
    ''' SUM_EXPRESSION : SUM_EXPRESSION PLUS term
                        | SUM_EXPRESSION MINUS term
                        | SUM_EXPRESSION BITWISENOR term 
                        | term
                        '''
    if(len(t) == 4):
        t[0] = (t[2][0],t[1],t[3])
    else:
        t[0] = t[1]
    #print t[0]    

def p_term (t):
    ''' term : term STAR UNARY_EXPRESSION
                | term DIVIDE UNARY_EXPRESSION
                | term MOD UNARY_EXPRESSION
                | UNARY_EXPRESSION
                '''
    if(len(t) == 4):
        t[0] = (t[2][0],t[1],t[3])
    else:
        t[0] = t[1]    


def p_UNARY_EXPRESSION(t):
    ''' UNARY_EXPRESSION : UNARY_OPERATOR UNARY_EXPRESSION
                        | factor
                        '''
    if(len(t) == 3):
        t[0] = (t[1][0],t[2])
    else:
        t[0] = t[1]

def p_UNARY_OPERATOR(t):
    '''UNARY_OPERATOR : MINUS
                | STAR
                '''
    t[0] = t[1][0]
    #print t[0]
    
def p_factor(t):
    ''' factor : DIFF_ID
                | STRUCT_EXPR
                '''
    t[0] = t[1]

def p_DIFF_ID(t):
    ''' DIFF_ID : IDENTIFIER
                | IDENTIFIER LEFTBRACKET EXPRESSION RIGHTBRACKET
                | IDENTIFIER LEFTBRACKET EXPRESSION RIGHTBRACKET LEFTBRACKET EXPRESSION RIGHTBRACKET
                | IDENTIFIER LEFTBRACKET INT_CONSTANT DOT DOT INT_CONSTANT RIGHTBRACKET
                | IDENTIFIER LEFTBRACKET INT_CONSTANT DOT DOT IDENTIFIER DOT IDENTIFIER RIGHTBRACKET                 
                |  IDENTIFIER DOT IDENTIFIER
                '''
    # print 'sahil'            
    if(len(t) == 2):
        t[0] = t[1]

    elif (len(t) == 5 or len(t) == 4 ):
        t[0] = (t[1],t[3])
    else:
        t[0]=(t[1],t[3],t[6])
    #print t[0]    

def p_STRUCT_EXPR(t):
    ''' STRUCT_EXPR : LEFTPAR EXPRESSION RIGHTPAR
                    | CONSTANT
                    | functionCall
                    | LEFTBRACKET LIST_OF_CONSTANTS RIGHTBRACKET
                    
                    '''
    if(len(t) == 4):
        t[0] = t[2]
    else:
        t[0] = t[1]

def p_functionCall (t):
    ''' functionCall : IDENTIFIER LEFTPAR args RIGHTPAR
            '''
    t[0] = {'NODE_TYPE':'call', 'IDENTIFIER':t[1], 'ARGS':t[3], 'TYPE':''}
    # global FUNCTION_PROTOTYPE_DECLARATION
    # flag = 0
    # if(t[1] != 'printf' and t[1] != 'scanf'):
    #     for func in FUNCTION_PROTOTYPE_DECLARATION :
    #             if(t[1] in func['NAME']):
    #                 flag=1
    #                 t[0]['TYPE'] = func['OUTPUT']
    #                 break
    #     if(flag == 0):
    #         print t[1],"Function is Undeclared"
    #         sys.exit()
    #     else :
    #         if(not(len(t[3]) == len(func['INPUT']))):
    #             print t[3]
    #             print func
    #             print "NUMBER OF ARGUMENTS OF FUNCTION DO NOT MATCH WITH THE GIVEN NUMBER OF ARGUMENTS"
    #             sys.exit()
    #         count = 0
    #         for x in func['INPUT']:
    #             if(t[3][count]['TYPE'] != x['TYPE']):
    #                 print "ARGUMENT TYPES DO NOT MATCH for function", func['NAME']
    #                 sys.exit()

def p_args(t):
    ''' args : args_list
            |
            '''
    if(len(t) == 2):
        t[0] = t[1]
    else:
        t[0] = []
    # print t[0]    
    #print t[0]
    
        
def p_args_list(t):
    ''' args_list : args_list COMMA EXPRESSION
                    | EXPRESSION
                    '''
    if(len(t) == 4):
        t[0] = t[1] + [t[3]]
    else:
        t[0] = [t[1]]
    # print t[0]    

def p_LIST_OF_CONSTANTS(t):
    ''' LIST_OF_CONSTANTS : STRING_CONSTANT COLON SIMPLE_EXPRESSION COMMA LIST_OF_CONSTANTS
                            | STRING_CONSTANT COLON SIMPLE_EXPRESSION
                    '''
    t[0] = t[1]   

def p_CONSTANT(t):
    ''' CONSTANT : INT_CONST
                    | FLOAT_CONST
                    | CHAR_CONST
                    | STR_CONST
                    '''
    t[0] = t[1]               

def p_INT_CONST(t):
    ''' INT_CONST : INT_CONSTANT
                '''
    t[0] = t[1]           

def p_FLOAT_CONST (t):
    ''' FLOAT_CONST : FLOAT_CONSTANT
                '''
    t[0] = t[1]

def p_STR_CONST (t):
    ''' STR_CONST : STRING_CONSTANT
                '''
    t[0] = t[1]
 
def p_CHAR_CONST (t):
    ''' CHAR_CONST : CHAR_CONSTANT
                '''
    t[0]=t[1]

def p_error(t):
    print "Parse Time Error!! at token",t.type," ", t.value," ", t.lineno


import logging
logging.basicConfig(
    level=logging.INFO,
    filename="parselog.txt"
)

parser = yacc.yacc()
data ='void print( immutable int[] array){int[string] days = ["MONDAY" : 0 , "TUE" : 1]; double[3][3] matrix; p[0..2] =3; a = b~ c ; a = b ~ c[0..0]; }'
print parser.parse(data, debug=logging.getLogger())
