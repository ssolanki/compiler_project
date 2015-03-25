import os,sys
import time
import dlex
import ply.yacc as yacc
tokens = dlex.tokens

def p_startProgram(t):
    ''' Program : LIST_OF_DECLARATIONS
                '''

    t[0] = {'TYPE':'startProgram','CHILD':t[1]}                
#    t[0] = t[1]
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
                    | FUNCTION_DEF
                    | FUNCTION_DECL
                    | VARIABLE_DEF
                    | TEMPLATES
                    '''
    t[0]=t[1]
    # print t[1],'sahil'
    #print t[0]

def p_TEMPLATES(t):
    ''' TEMPLATES : VARIABLE_TYPE IDENTIFIER LEFTPAR TEMP_PARAMETERS_TYPE RIGHTPAR LEFTPAR LIST_OF_TEMP_PARAMETERS RIGHTPAR  STATEMENT
    '''
    t[0] = (t[1] , t[4] , t[7])   
def p_TEMP_PARAMETERS_TYPE(t):
    ''' TEMP_PARAMETERS_TYPE : TEMP_PARAMETERS_TYPE COMMA IDENTIFIER
                    | IDENTIFIER
                    '''

    # global parametersymboltable
    if(len(t) == 4):
        t[0] = t[1] + [t[3]]
        # parametersymboltable.insert(t[3]['IDENTIFIER'],{'TYPE':t[3]['TYPE'],'ARRAY':t[3]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':0,'STATIC':0})
    else:
        t[0] =  [t[1]]
        # parametersymboltable.insert(t[1]['IDENTIFIER'],{'TYPE':t[1]['TYPE'],'ARRAY':t[1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1': 0,'STATIC':0})

def p_LIST_OF_TEMP_PARAMETERS(t):
    ''' LIST_OF_TEMP_PARAMETERS : LIST_OF_TEMP_PARAMETERS COMMA IDENTIFIER IDENTIFIER
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

def p_FUNCTION_DEF(t):
    ''' FUNCTION_DEF : VARIABLE_TYPE IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR SEMICOLON
                            | IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR SEMICOLON
                            
                            '''
    # t[0] = (t[1],t[2],t[4])
    global FUNCTION_PROTOTYPE_DECLARATION
    global functions
    global parametersymboltable
    #sys.call()
    if(len(t) == 7 ):
        t[0] = {'NODE_TYPE':'function_defination', 'OUTPUT':t[1]['TYPE'], 'INPUT': t[4], 'IDENTIFIER': t[2],'partProgram': ''}
        currentfunction = {'Function Detail':t[0],'symboltable':parametersymboltable}
        functions = functions + [currentfunction]
        CURRENT_DECLARATION = [{"NAME":t[2],"INPUT":t[4],"OUTPUT":t[1]['TYPE']}]
        FUNCTION_PROTOTYPE_DECLARATION = FUNCTION_PROTOTYPE_DECLARATION + CURRENT_DECLARATION
        parametersymboltable = SymbolTable(-1)
    elif(len(t) == 6 ):
        t[0] = {'NODE_TYPE':'function_defination', 'OUTPUT':'VOID', 'INPUT': t[3], 'IDENTIFIER': t[1],'partProgram': ''}
        currentfunction = {'Function Detail':t[0],'symboltable':parametersymboltable}
        functions = functions + [currentfunction]
        CURRENT_DECLARATION = [{"NAME":t[1],"INPUT":t[3],"OUTPUT":'VOID'}]
        FUNCTION_PROTOTYPE_DECLARATION = FUNCTION_PROTOTYPE_DECLARATION + CURRENT_DECLARATION
        parametersymboltable = SymbolTable(-1)
    print t[0]    


def p_PARAMETERS(t):
    ''' PARAMETERS : LIST_OF_PARAMETERS
                |
                '''
    #print t[1]
    if(len(t)==2):
        t[0] = t[1]
    else:
        t[0] = []
    
def p_LIST_OF_PARAMETERS (t):
    ''' LIST_OF_PARAMETERS : LIST_OF_PARAMETERS COMMA PARAMETER_TYPE
                    | PARAMETER_TYPE
                    '''

    global parametersymboltable
    if(len(t) == 4):
        t[0] = t[1] + [t[3]]
        parametersymboltable.insert(t[3]['IDENTIFIER'],{'TYPE':t[3]['TYPE'],'ARRAY':t[3]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':0,'STATIC':0})
    else:
        t[0] =  [t[1]]
        parametersymboltable.insert(t[1]['IDENTIFIER'],{'TYPE':t[1]['TYPE'],'ARRAY':t[1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1': 0,'STATIC':0})
    
def p_PARAMETER_TYPE (t):
    ''' PARAMETER_TYPE : VARIABLE_TYPE IDENTIFIER
                        | VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER
                        | REF VARIABLE_TYPE IDENTIFIER
                        | REF VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER 
                        | IMMUTABLE VARIABLE_TYPE IDENTIFIER
                        | IMMUTABLE VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER 
                        
                        '''
    t[0] = {'NODE_TYPE': 'param_type_node', 'TYPE': t[1]['TYPE'], 'ARRAY': t[2]['ARRAY'],'IDENTIFIER': t[2]['IDENTIFIER']}

    # t[0] = (t[2], t[1])
    # if (len(t) == 2):
    #     t[0] = t[1]
    # else:
    #     t[0] = t[1]

# ---------------------------------------------------------------------------------------------

def p_FUNCTION_DECL(t):
    ''' FUNCTION_DECL : VARIABLE_TYPE IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR STATEMENT 
                            | IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR STATEMENT
                            | PURE VARIABLE_TYPE IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR STATEMENT  
                            | VARIABLE_TYPE IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR NOTHROW STATEMENT  
                            | REF VARIABLE_TYPE IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR STATEMENT 
                            | AUTO IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR STATEMENT   
                            | VARIABLE_TYPE IDENTIFIER LEFTPAR VARIABLE_TYPE IDENTIFIER COMMA DOT DOT DOT RIGHTPAR STATEMENT  
                            '''

        global FUNCTION_PROTOTYPE_DECLARATION
    global functions
    global parametersymboltable
    #sys.call()
    if(len(t) == 7 ):
        t[0] = {'NODE_TYPE':'function_declaration', 'OUTPUT':t[1]['TYPE'], 'INPUT': t[4], 'IDENTIFIER': t[2],'partProgram': t[6]}
        flag = 0
        for func in FUNCTION_PROTOTYPE_DECLARATION :
                #print t[2]
                if(t[2] in func['NAME'] or t[2] == 'main'):
                    flag=1
                    func['partProgram'] = t[6]
                    break
        if(flag != 1):
            print "function definition missing for ",t[2]
            currentfunction = {'Function Detail':t[0],'symboltable':parametersymboltable}
            functions = functions + [currentfunction]
            CURRENT_DECLARATION = [{"NAME":t[2],"INPUT":t[4],"OUTPUT":t[1]['TYPE']}]
            FUNCTION_PROTOTYPE_DECLARATION = FUNCTION_PROTOTYPE_DECLARATION + CURRENT_DECLARATION
            
    elif(len(t) == 6 ):
        t[0] = {'NODE_TYPE':'function_declaration', 'OUTPUT':'VOID', 'INPUT': t[3], 'IDENTIFIER': t[1],'partProgram': t[5]}
        flag = 0
        for func in FUNCTION_PROTOTYPE_DECLARATION :
                if(t[1] in func['NAME'] or t[1] == 'main'):
                    flag=1
                    func['partProgram'] = t[5]
                    break
        if(flag != 1):
            print "function definition missing for ",t[2]
            currentfunction = {'Function Detail':t[0],'symboltable':parametersymboltable}
            functions = functions + [currentfunction]
            CURRENT_DECLARATION = [{"NAME":t[1],"INPUT":t[3],"OUTPUT":'VOID'}]
            FUNCTION_PROTOTYPE_DECLARATION = FUNCTION_PROTOTYPE_DECLARATION + CURRENT_DECLARATION
            parametersymboltable = SymbolTable(-1)
    print t[0]       

    # t[0] = (t[5])
    # print (t[6])
    # print 'function declaration'

def p_STATEMENT(t):
    ''' STATEMENT : EXPRESSION_STATEMENT
                    | COMPLEX_STATEMENT
                    | DECISION_STATEMENT
                    | LOOP_STATEMENT
                    | RETURN_STATEMENT
                    | BREAK_STATEMENT
                    '''
    t[0] = {'NODE_TYPE':'STATEMENT','CHILD':t[1]}
    # print 'statement', t[0]

def p_EXPRESSION_STATEMENT(t):
    ''' EXPRESSION_STATEMENT : EXPRESSION SEMICOLON
                        
                        '''
    if(len(t) == 2):
        t[0] = {'NODE_TYPE':'expression_stmt', 'EXPRESSION':''}
    else:
        t[0] = {'NODE_TYPE':'expression_stmt', 'EXPRESSION':t[1]}
    # print 'expression ' , t[0]    

def p_COMPLEX_STATEMENT(t):
    ''' COMPLEX_STATEMENT : LEFTBRACE PROG_LOCAL_DECLS LIST_OF_STATEMENTS RIGHTBRACE
                        '''
    t[0] = {'NODE_TYPE':'compound_stmt','STATEMENTS': t[3],'LOCAL_DECL': t[2]}

def p_PROG_LOCAL_DECLS(t):
    ''' PROG_LOCAL_DECLS : PROG_LOCAL_DECLS  SCOPED_VARIABLE_DECL
                            |
                            '''
    if( len(t) == 3 ):
        t[0] = t[1] + [t[2]]
        #t[0] = t[1] + t[2]
    else:
        t[0] = []

          
def p_SCOPED_VARIABLE_DECL(t):
    ''' SCOPED_VARIABLE_DECL : SCOPED_VARIABLE_TYPE LISTOF_VAR_DECLARATIONS SEMICOLON
                               '''
    t[0] = t[1]     
    t[0]={'NODE_TYPE':'scoped_var_declaration','STATIC':t[1]['STATIC'],'VAR_TYPE':t[1]['TYPE'], 'VAR_LIST': t[2]}

    table = 'LOCAL'
    initialise = ''
    if(t[1]['TYPE'] == 'float'):
        table = 'GLOBAL'
        initialise = {'TYPE': 'float', 'NODE_TYPE': 'expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'simple_expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'and_expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'unary_rel_expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'rel_expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'sum_expression', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'term', 'EXPRESSION': {'TYPE': 'float', 'NODE_TYPE': 'unary_expression', 'OP': '', 'EXPRESSION': {'SUBTYPE': 'immutable', 'NODE_TYPE': 'factor', 'EXPRESSION': {'SUBTYPE': 'Constant', 'NODE_TYPE': 'immutable', 'TYPE': 'float', 'VALUE': '0.0'}, 'TYPE': 'float'}, 'factor': 1}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OPS': ''}
    for x in t[2]:
        if (currentSymbolTable.insert(x['ID'],{'TYPE':t[1]['TYPE'],'STATIC':t[1]['STATIC'],'ARRAY': x['ARRAY'],'INDEX1':x['INDEX1'],'INDEX2':x['INDEX2'],'SCOPETYPE':table}) == False):
            print x['ID'],': Variable already declared '
            sys.exit()
        else:
            x['SCOPETYPE'] = 'LOCAL'
            check = currentSymbolTable.lookupCurrentTable(x['ID'])
            #print check
            x['offset'] = check['offset']
            x['TABLE'] = check['TABLE']
            x['TYPE'] = t[1]['TYPE']
            x['STATIC'] = t[1]['STATIC']
            if (x['INITIALISED'] == ''):
                x['INITIALISED'] = initialise
            print x['offset']

# STATIC NOT HERE

def p_SCOPED_VARIABLE_TYPE(t):
    ''' SCOPED_VARIABLE_TYPE : STATIC VARIABLE_TYPE
                                | VARIABLE_TYPE
                                '''
    if(len(t) == 3):
        t[0] = {'NODE_TYPE' : 'scoped_type_specifier', 'STATIC':1, 'TYPE': t[2]['TYPE'] }
    else :
        t[0] = {'NODE_TYPE' : 'scoped_type_specifier', 'STATIC':0, 'TYPE': t[1]['TYPE'] }
    print t[0]
  
def p_LIST_OF_STATEMENTS(t):
    ''' LIST_OF_STATEMENTS : LIST_OF_STATEMENTS STATEMENT
                        |
                        '''
    if ( len(t) == 3):
        t[0] = t[1] + [t[2]]
    else :
        t[0] = ['']

def p_DECISION_STATEMENT (t):
    '''DECISION_STATEMENT : IF LEFTPAR SIMPLE_EXPRESSION RIGHTPAR STATEMENT
                        | IF LEFTPAR SIMPLE_EXPRESSION RIGHTPAR STATEMENT ELSE STATEMENT
                        '''

    if( len(t) == 6):
        t[0] = {'NODE_TYPE':'IF', 'CONDITION': t[3], 'ifProgram': t[5], 'elseProgram':''}
        #print t[0]
    else:
        t[0] = {'NODE_TYPE':'IF_ELSE', 'CONDITION': t[3], 'ifProgram': t[5], 'elseProgram': t[7]}
        #print t[0]
        
def p_LOOP_STATEMENT(t):
    '''LOOP_STATEMENT : WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR STATEMENT
                        | FOR LEFTPAR EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHTPAR  STATEMENT
                        | DO STATEMENT WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR SEMICOLON 
                        '''
    if( len(t) == 6):
        t[0] = {'NODE_TYPE':'WHILE', 'CONDITION': t[3], 'partProgram':t[5]}

    elif ( len(t) == 10):
        t[0] = {'NODE_TYPE':'FOR', 'CONDITION': t[5], 'INITIALISE': t[3], 'UPDATE': t[7], 'partProgram': t[9]}

    else:
        t[0] = {'NODE_TYPE':'DO', 'CONDITION': t[5],'partProgram': t[2]}


#---------------------------------------------------------------

def p_VARIABLE_DEF(t):
    ''' VARIABLE_DEF : ENUM ENUM_VARIABLE_TYPE LEFTBRACE LISTOF_VAR_DECLARATIONS RIGHTBRACE SEMICOLON
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

    t[0]={'TYPE':'VARIABLE_DECL','VAR_TYPE':t[1]['TYPE'], 'VAR_LIST': t[2]}
    for x in t[2]:
        if (currentSymbolTable.insert(x['ID'],{'TYPE':t[1]['TYPE'],'STATIC':0,'ARRAY': x['ARRAY'],'INDEX1':x['INDEX1'],'INDEX2':x['INDEX2'],'SCOPETYPE':'GLOBAL'}) == False):
            print x['ID'],': Variable already declared '
            sys.exit()
        else:
            x['SCOPETYPE'] = 'GLOBAL'
            check = currentSymbolTable.lookupCurrentTable(x['ID'])
            #print check
            x['TYPE'] = t[1]['TYPE']
            x['offset'] = check['offset']
            x['STATIC'] = 0
            #print x['offset']
    print t[0]                                
    # # if(len(t)==2):
    # #     t[0]=t[1]
    # # else: 
    # t[0]=t[2]     
    # #print t[0]        

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
    
#     if( len(t) == 2):
#         t[0] = t[1]
        
#     elif ( len(t) == 4):
#         t[0] = (t[1],t[3])
# #    print t[0]
    if( len(t) == 2):
        t[0] = {'NODE_TYPE':'var_initialise', 'ID': t[1]['IDENTIFIER'], 'ARRAY':t[1]['ARRAY'],'INDEX1':t[1]['INDEX1'],'INDEX2':t[1]['INDEX2'], 'INITIALISED':''}
    elif ( len(t) == 4):
        t[0] = {'NODE_TYPE':'var_initialise', 'ID': t[1]['IDENTIFIER'], 'ARRAY':t[1]['ARRAY'],'INDEX1':t[1]['INDEX1'],'INDEX2':t[1]['INDEX2'], 'INITIALISED':t[3]}
    print t[0]

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
    # if(len(t) == 2 ):
    #     t[0] = (t[1])
    # elif(len(t) == 5):
    #     t[0] = (t[1],t[3])
    # else:
    #     t[0] = (t[1],t[3],t[6])
    if(len(t) == 2 ):
        t[0] = {'NODE_TYPE' : 'var_decl_id', 'ARRAY':0, 'IDENTIFIER' : t[1], 'INDEX1': '','INDEX2':''}
        #print t[1]
    elif(len(t) == 5):
        t[0] = {'NODE_TYPE': 'var_decl_id','ARRAY':1, 'IDENTIFIER' : t[1], 'INDEX1': t[3],'INDEX2':''}
    else:
        t[0] = {'NODE_TYPE': 'var_decl_id','ARRAY':2, 'IDENTIFIER' : t[1], 'INDEX1': t[3],'INDEX2':t[6]}
    print t[0]    


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
    # t[0] = t[1]
    #print t[0]
    t[0] = {'NODE_TYPE': 'type_specifier', 'TYPE': t[1]}
    #print t[1]
    print t[0]


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
                    | LEFTBRACKET LIST_OF_CONSTANTS RIGHTBRACKET
                    | CONSTANT
                    | FUNCTION_INSTANCE                    
                    '''
    if(len(t) == 4):
        t[0] = t[2]
    else:
        t[0] = t[1]

def p_FUNCTION_INSTANCE (t):
    ''' FUNCTION_INSTANCE : IDENTIFIER LEFTPAR FUNC_ARGUMENTS RIGHTPAR
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

def p_FUNC_ARGUMENTS(t):
    ''' FUNC_ARGUMENTS : LIST_OF_FUNCTION_ARGUMENTS
            |
            '''
    if(len(t) == 2):
        t[0] = t[1]
    else:
        t[0] = []
    # print t[0]    
    #print t[0]
    
        
def p_LIST_OF_FUNCTION_ARGUMENTS(t):
    ''' LIST_OF_FUNCTION_ARGUMENTS : LIST_OF_FUNCTION_ARGUMENTS COMMA EXPRESSION
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
