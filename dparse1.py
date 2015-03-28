import os,sys
import time
import dlex
import ply.yacc as yacc
tokens = dlex.tokens
from SymbolTable import *

global FUNCTION_PROTOTYPES
FUNCTION_PROTOTYPES = [{'FUNC_NAME':' ','INPUT':'',"OUTPUT":''}]
global currentSymbolTable
currentSymbolTable = SymbolTable(-1)
global parametersymboltable
parametersymboltable = SymbolTable(-1)
global DefinedFunctions
DefinedFunctions = []
tableNumber = 1;

def p_startProgram(p):
    ''' Program : LIST_OF_DECLARATIONS
                '''

    p[0] = {'NODE_TYPE':'startProgram','CHILD':p[1]}                
#    p[0] = p[1]
    #

def p_LIST_OF_DECLARATIONS(p):
    '''LIST_OF_DECLARATIONS : LIST_OF_DECLARATIONS DECLARATION
                        | DECLARATION
                        '''                        
    if( len([p]) == 3):
        p[0]=p[1]+[p[2]]
    else:
        p[0] = p[1]
        # 

    #
# RIGHT NOW ONLY VAR_DECLARATION WORKING SO WE ARE USING ONLY THIS RULE
def p_DECLARATION(p):
    ''' DECLARATION : VARIABLE_DECLARATION
                    | FUNCTION_DEF
                    | FUNCTION_DECL
                    | VARIABLE_DEF
                    | TEMPLATES
                    '''
    p[0]=p[1]
    # print p[1],'sahil'
    #

def p_TEMPLATES(p):
    ''' TEMPLATES : VARIABLE_TYPE IDENTIFIER LEFTPAR TEMP_PARAMETERS_TYPE RIGHTPAR LEFTPAR LIST_OF_TEMP_PARAMETERS RIGHTPAR  STATEMENT
    '''
    p[0] = (p[1] , p[4] , p[7])

def p_TEMP_PARAMETERS_TYPE(p):
    ''' TEMP_PARAMETERS_TYPE : TEMP_PARAMETERS_TYPE COMMA IDENTIFIER
                    | IDENTIFIER
                    '''

    # global parametersymboltable
    if(len(p) == 4):
        p[0] = p[1] + [p[3]]
        # parametersymboltable.insert(p[3]['IDENTIFIER'],{'DATA_TYPE':p[3]['DATA_TYPE'],'ARRAY':p[3]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':0,'STATIC':0})
    else:
        p[0] =  [p[1]]
        # parametersymboltable.insert(p[1]['IDENTIFIER'],{'DATA_TYPE':p[1]['DATA_TYPE'],'ARRAY':p[1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1': 0,'STATIC':0})

def p_LIST_OF_TEMP_PARAMETERS(p):
    ''' LIST_OF_TEMP_PARAMETERS : LIST_OF_TEMP_PARAMETERS COMMA IDENTIFIER IDENTIFIER
                    | IDENTIFIER IDENTIFIER
    '''

    # global parametersymboltable
    if(len(p) == 5):
        p[0] = p[1] + [p[3]]
        # parametersymboltable.insert(p[3]['IDENTIFIER'],{'DATA_TYPE':p[3]['DATA_TYPE'],'ARRAY':p[3]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1':0,'STATIC':0})
    else:
        p[0] =  [p[1]]
        # parametersymboltable.insert(p[1]['IDENTIFIER'],{'DATA_TYPE':p[1]['DATA_TYPE'],'ARRAY':p[1]['ARRAY'],'SCOPETYPE':'PARAMETER','INDEX1': 0,'STATIC':0})

#----------------------------------------------------------------

def p_FUNCTION_DEF(p):
    ''' FUNCTION_DEF : IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR SEMICOLON
                        | VARIABLE_TYPE IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR SEMICOLON
                        '''

    # p[0] = (p[1],p[2],p[4])
    global parametersymboltable
    global DefinedFunctions
    global FUNCTION_PROTOTYPES
    # global m
##############################################
#   type--> op_type , input --> parameters ,     partProgram - > FUNCTION_PROGRAM   Name-> func_name
#   order not changed
##########################################################
    if(len(p) == 6 ):

        p[0] = {'NODE_TYPE':'FUNCTION_DEF', 'INPUT': t[3],'OUTPUT':'VOID' , 'IDENTIFIER': p[1],'PARAMETERS': p[3], 'FUNCTION_PROGRAM': ''}
        newfunction = {'FUNCTION INFORMATIONS: ':p[0],'symboltable':parametersymboltable}
#       add this def to our definedfunctions var
#        print newfunction
        DefinedFunctions = DefinedFunctions + [newfunction]
        CURRENT_DECLARATION = [{"FUNC_NAME":p[1],"INPUT":p[3],"OUTPUT":'VOID'}]
        FUNCTION_PROTOTYPES = FUNCTION_PROTOTYPES + CURRENT_DECLARATION
        parametersymboltable = SymbolTable(-1)
        
    else:
        p[0] = {'NODE_TYPE':'FUNCTION_DEF', 'INPUT': t[4], 'OUTPUT':p[1]['DATA_TYPE'],  'IDENTIFIER': p[2],'PARAMETERS': p[4], 'FUNCTION_PROGRAM': ''}
        newfunction = {'FUNCTION INFORMATIONS: ':p[0],'symboltable':parametersymboltable}
#       add this def to our definedfunctions var
#        print newfunction
        DefinedFunctions = DefinedFunctions + [newfunction]
        CURRENT_DECLARATION = [{"FUNC_NAME":p[2],"INPUT":p[4],"OUTPUT":p[1]['DATA_TYPE']}]
        FUNCTION_PROTOTYPES += CURRENT_DECLARATION
        parametersymboltable = SymbolTable(-1)
        


def p_FUNCTION_DECL(p):
    ''' FUNCTION_DECL : VARIABLE_TYPE IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR STATEMENT 
                            | IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR STATEMENT
                            | PURE VARIABLE_TYPE IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR STATEMENT  
                            | VARIABLE_TYPE IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR NOTHROW STATEMENT  
                            | REF VARIABLE_TYPE IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR STATEMENT 
                            | AUTO IDENTIFIER LEFTPAR PARAMETERS RIGHTPAR STATEMENT   
                            | VARIABLE_TYPE IDENTIFIER LEFTPAR VARIABLE_TYPE IDENTIFIER COMMA DOT DOT DOT RIGHTPAR STATEMENT  
                            '''

    global parametersymboltable
    global DefinedFunctions
    global FUNCTION_PROTOTYPES
######### RULE STILL REMAINING
    if(len(p) == 6 ):
        temp = 0        
        p[0] = {'NODE_TYPE':'FUNCTION_DECLARATION', 'INPUT': p[3] , 'OUTPUT':'VOID', 'IDENTIFIER': p[1],'FUNCTION_PROGRAM': p[5]}
        for f in FUNCTION_PROTOTYPES :
            # WHAT ABOUT MAIN()
                if(p[1] in f['FUNC_NAME']):
                    temp=1
                    f['FUNCTION_PROGRAM'] = p[5]
                    break
        if(temp == 0):
            print "No function defined like this : ", p[2]
            currentfunction = {'Function Detail':p[0],'symboltable':parametersymboltable}
            DefinedFunctions = DefinedFunctions + [currentfunction]
            CURRENT_DECLARATION = [{"FUNC_NAME":p[1],"INPUT":p[3],"OUTPUT":'VOID'}]
            FUNCTION_PROTOTYPES += CURRENT_DECLARATION
            parametersymboltable = SymbolTable(-1)

    elif(len(p) == 7 ):
        temp = 0
        p[0] = {'NODE_TYPE':'FUNCTION_DECLARATION',  'INPUT': p[4], 'OUTPUT':p[1]['DATA_TYPE'], 'IDENTIFIER': p[2],'FUNCTION_PROGRAM': p[6]}        
        for f in FUNCTION_PROTOTYPES :
                #print p[2]
                if(p[2] in f['FUNC_NAME']):
                    temp=1
                    f['FUNCTION_PROGRAM'] = p[6]
                    break
        if(temp == 0 ):
            print "No function defined like this :  ", p[2]
            newfunction = {'FUNCTION INFORMATIONS: ':p[0],'symboltable':parametersymboltable}
            DefinedFunctions = DefinedFunctions + [newfunction]
            CURRENT_DECLARATION = [{"FUNC_NAME":p[2],"INPUT":p[4],"OUTPUT":p[1]['DATA_TYPE']}]
            FUNCTION_PROTOTYPES += CURRENT_DECLARATION
                       

    # p[0] = (p[5])
    # print (p[6])
    # print 'function declaration'
def p_PARAMETERS(p):
    ''' PARAMETERS : LIST_OF_PARAMETERS
                |
                '''
    #print p[1]
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = []
    
def p_LIST_OF_PARAMETERS (p):
    ''' LIST_OF_PARAMETERS : LIST_OF_PARAMETERS COMMA PARAMETER_TYPE
                    | PARAMETER_TYPE
                    '''

    global parametersymboltable
    if(len(p) == 2):
        p[0] =  [p[1]]
        insertNode = {'DATA_TYPE':p[1]['DATA_TYPE'],'ARRAY_DIMENTION':p[1]['ARRAY_DIMENTION'],'SCOPE':'PARAM','VAL1': 0,'STATIC':0}
        parametersymboltable.insert(p[1]['IDENTIFIER'], insertNode)

    else:
        p[0] = p[1] + [p[3]]
        insertNode = {'DATA_TYPE':p[3]['DATA_TYPE'],'ARRAY_DIMENTION':p[3]['ARRAY_DIMENTION'],'SCOPE':'PARAM','VAL1':0,'STATIC':0}
        parametersymboltable.insert(p[3]['IDENTIFIER'], insertNode)
    
    #        print p[0]
    
def p_PARAMETER_TYPE (p):
    ''' PARAMETER_TYPE : VARIABLE_TYPE IDENTIFIER
                        | VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER
                        | REF VARIABLE_TYPE IDENTIFIER
                        | REF VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER 
                        | IMMUTABLE VARIABLE_TYPE IDENTIFIER
                        | IMMUTABLE VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER 
                        
                        '''
########## RULE STILL REMAINING
    if(len(p)==3):                        
        p[0] = {'NODE_TYPE': 'PARAMETER_TYPE', 'DATA_TYPE': p[1]['DATA_TYPE'] ,'IDENTIFIER': p[2] , 'ARRAY_DIMENTION': 0}
    elif(len(p)==5):
        p[0] = {'NODE_TYPE': 'PARAMETER_TYPE', 'DATA_TYPE': p[1]['DATA_TYPE'],'IDENTIFIER': p[4] , 'ARRAY_DIMENTION': 1 }
    
        
#    ------------------------------
    # p[0] = (p[2], p[1])
    # if (len(p) == 2):
    #     p[0] = p[1]
    # else:
    #     p[0] = p[1]

# ---------------------------------------------------------------------------------------------

def p_STATEMENT(p):
    ''' STATEMENT : EXPRESSION_STATEMENT
                    | COMPLEX_STATEMENT
                    | DECISION_STATEMENT
                    | LOOP_STATEMENT
                    | RETURN_STATEMENT
                    | BREAK_STATEMENT
                    '''
    p[0] = {'NODE_TYPE':'STATEMENT','CHILD':p[1]}
    # print 'statement', p[0]

def p_EXPRESSION_STATEMENT(p):
    ''' EXPRESSION_STATEMENT : EXPRESSION SEMICOLON
                        
                        '''
    p[0] = {'NODE_TYPE':'EXPRESSION_STATEMENT', 'EXPRESSION':p[1]}

    # print 'expression ' , p[0]    

def p_COMPLEX_STATEMENT(p):
    ''' COMPLEX_STATEMENT : LEFTBRACES PROG_LOCAL_DECLS LIST_OF_STATEMENTS RIGHTBRACES
                        '''
    p[0] = {'NODE_TYPE':'COMPLEX_STATEMENT','LOCAL_DECL': p[2],'STATEMENTS': p[3]}

def p_PROG_LOCAL_DECLS(p):
    ''' PROG_LOCAL_DECLS : PROG_LOCAL_DECLS  SCOPED_VARIABLE_DECL
                            |
                            '''
    if( len(p) == 3 ):
#        print p[2]
        p[0] = p[1] + [p[2]]

    else:
        p[0] = []

          
def p_SCOPED_VARIABLE_DECL(p):
    ''' SCOPED_VARIABLE_DECL : SCOPED_VARIABLE_TYPE LISTOF_VAR_DECLARATIONS SEMICOLON
                               '''
#    print t[0]
    # p[0] = p[1]     
    p[0]={'NODE_TYPE':'SCOPED_VARIABLE_DECL', 'VARIABLE_TYPE':p[1]['DATA_TYPE'], 'LIST_OF_VARIABLES': p[2],'STATIC':p[1]['STATIC']}

    initial_val = ''
    # if(p[1]['DATA_TYPE'] == 'float'):
    #     table = 'GLOBAL'
    #     initialise = {'DATA_TYPE': 'float', 'NODE_TYPE': 'expression', 'EXPRESSION': {'DATA_TYPE': 'float', 'NODE_TYPE': 'simple_expression', 'EXPRESSION': {'DATA_TYPE': 'float', 'NODE_TYPE': 'and_expression', 'EXPRESSION': {'DATA_TYPE': 'float', 'NODE_TYPE': 'unary_rel_expression', 'EXPRESSION': {'DATA_TYPE': 'float', 'NODE_TYPE': 'rel_expression', 'EXPRESSION': {'DATA_TYPE': 'float', 'NODE_TYPE': 'sum_expression', 'EXPRESSION': {'DATA_TYPE': 'float', 'NODE_TYPE': 'term', 'EXPRESSION': {'DATA_TYPE': 'float', 'NODE_TYPE': 'unary_expression', 'OP': '', 'EXPRESSION': {'SUBTYPE': 'immutable', 'NODE_TYPE': 'factor', 'EXPRESSION': {'SUBTYPE': 'Constant', 'NODE_TYPE': 'immutable', 'DATA_TYPE': 'float', 'VALUE': '0.0'}, 'DATA_TYPE': 'float'}, 'factor': 1}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OP': ''}, 'OPS': ''}
    for var in p[2]:
        if (currentSymbolTable.insert(var['IDENTIFIER'],{'DATA_TYPE':p[1]['DATA_TYPE'],'STATIC':p[1]['STATIC'],'ARRAY_DIMENTION': var['ARRAY_DIMENTION'],'VAL1':var['VAL1'],'VAL2':var['VAL2'],'SCOPE':'LOCAL'}) == False):
            print var['IDENTIFIER'],': Already Declared Before!! '
            sys.exit()
        else:
            var['DATA_TYPE'] = p[1]['DATA_TYPE']
            var['STATIC'] = p[1]['STATIC']
            var['SCOPE'] = 'LOCAL'
            var['offset'] = currentSymbolTable.lookupCurrentTable(var['IDENTIFIER'])['offset']
            var['TABLE'] = currentSymbolTable.lookupCurrentTable(var['IDENTIFIER'])['TABLE']
            if (var['INITIALISED'] == ''):
                var['INITIALISED'] = initial_val
            print var['offset']

# STATIC NOT HERE

def p_SCOPED_VARIABLE_TYPE(p):
    ''' SCOPED_VARIABLE_TYPE : STATIC VARIABLE_TYPE
                                | VARIABLE_TYPE
                                '''
    if(len(p) == 2):
        p[0] = {'NODE_TYPE' : 'SCOPED_VARIABLE_TYPE', 'DATA_TYPE': p[1]['DATA_TYPE'], 'STATIC':0 }
    else :
        p[0] = {'NODE_TYPE' : 'SCOPED_VARIABLE_TYPE', 'DATA_TYPE': p[2]['DATA_TYPE'] , 'STATIC':1 }        
    
  
def p_LIST_OF_STATEMENTS(p):
    ''' LIST_OF_STATEMENTS : LIST_OF_STATEMENTS STATEMENT
                        |
                        '''
    if ( len(p) == 3):
        p[0] = p[1] + [p[2]]
    else :
        p[0] = ['']

def p_DECISION_STATEMENT (p):
    '''DECISION_STATEMENT : IF LEFTPAR SIMPLE_EXPRESSION RIGHTPAR STATEMENT
                        | IF LEFTPAR SIMPLE_EXPRESSION RIGHTPAR STATEMENT ELSE STATEMENT
                        '''

    if( len(p) == 6):
        p[0] = {'NODE_TYPE':'IF', 'CONDITION_EXPR': p[3], 'IF_PROGRAM': p[5], 'ELSE_PROGRAM':''}
        # print p[0]
    else:
        p[0] = {'NODE_TYPE':'IF_ELSE', 'CONDITION_EXPR': p[3], 'IF_PROGRAM': p[5], 'ELSE_PROGRAM': p[7]}
        #
        
def p_LOOP_STATEMENT(p):
    '''LOOP_STATEMENT : FOR LEFTPAR EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHTPAR  STATEMENT
                        | WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR STATEMENT
                        | DO STATEMENT WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR SEMICOLON 
                        '''
    
    if ( len(p) == 10):
        p[0] = {'NODE_TYPE':'FOR', 'CONDITION_EXPR': p[5], 'INITIALISE': p[3], 'UPDATE': p[7], 'PARTIAL_PROGRAM': p[9]}
    elif( len(p) == 6):
        p[0] = {'NODE_TYPE':'WHILE', 'CONDITION_EXPR': p[3], 'PARTIAL_PROGRAM':p[5]}    
    else:
        p[0] = {'NODE_TYPE':'DO', 'CONDITION_EXPR': p[5],'PARTIAL_PROGRAM': p[2]}


#---------------------------------------------------------------

def p_VARIABLE_DEF(p):
    ''' VARIABLE_DEF : ENUM ENUM_VARIABLE_TYPE LEFTBRACES LISTOF_VAR_DECLARATIONS RIGHTBRACES SEMICOLON
                            | ENUM COLON VARIABLE_TYPE LEFTBRACES LISTOF_VAR_DECLARATIONS RIGHTBRACES 
                            | ENUM LEFTBRACES LISTOF_VAR_DECLARATIONS RIGHTBRACES
                        '''
###############################################
    # if(len(p)==2):
    #     p[0]=p[1]
    # else: 
    # p[0]=p[4]     
    #
    for var in p[2]:
        if (currentSymbolTable.insert(var['ID'],{'DATA_TYPE':p[1]['DATA_TYPE'],'STATIC':0,'ARRAY_DIMENTION': var['ARRAY_DIMENTION'],'VAL1':var['VAL1'],'VAL2':var['VAL2'],'SCOPETYPE':'GLOBAL'}) == False):
            print var['IDENTIFIER'],': Declared Already Before!! '
            sys.exit()
        else:
            var['SCOPETYPE'] = 'GLOBAL'
            check = currentSymbolTable.lookupCurrentTable(var['IDENTIFIER'])
            #print check
            var['DATA_TYPE'] = p[1]['DATA_TYPE']
            var['offset'] = check['offset']
            var['STATIC'] = 0

def p_ENUM_VARIABLE_TYPE(p):
    ''' ENUM_VARIABLE_TYPE : IDENTIFIER
                        '''
################################################
    # if(len(p)==2):
    #     p[0]=p[1]
    # else: 
    p[0]=p[1]     
    #        

def p_VARIABLE_DECLARATION(p):
    '''VARIABLE_DECLARATION : VARIABLE_TYPE LISTOF_VAR_DECLARATIONS SEMICOLON
                        '''

    p[0]={'DATA_TYPE':'VARIABLE_DECL','VARIABLE_TYPE':p[1]['DATA_TYPE'], 'LIST_OF_VARIABLES': p[2]}

    for var in p[2]:
        if (currentSymbolTable.insert(var['ID'],{'DATA_TYPE':p[1]['DATA_TYPE'],'ARRAY_DIMENTION': var['ARRAY_DIMENTION'],'VAL1':var['VAL1'],'VAL2':var['VAL2'],'SCOPE':'GLOBAL','STATIC':0}) == False):
            print var['IDENTIFIER'],': Declared Already Before!! '
            sys.exit()
        else:
            #print check
            var['DATA_TYPE'] = p[1]['DATA_TYPE']
            var['STATIC'] = 0
            var['SCOPE'] = 'GLOBAL'
            var['offset'] = currentSymbolTable.lookupCurrentTable(var['IDENTIFIER'])['offset']
                                    
    # # if(len(p)==2):
    # #     p[0]=p[1]
    # # else: 
    # p[0]=p[2]     
    # #        

def p_LISTOF_VAR_DECLARATIONS(p):
    '''LISTOF_VAR_DECLARATIONS : LISTOF_VAR_DECLARATIONS COMMA VAR_INITIALIZE
                    | VAR_INITIALIZE
                    '''

    if( len(p) == 4):
        p[0] = p[1] + [p[3]]
    else:
        #print 'sahil'
        #print p[1]
        p[0] = [p[1]]
    #    

def p_VAR_INITIALIZE(p):
    '''VAR_INITIALIZE : VAR_DECLARATION_ID
                            |  VAR_DECLARATION_ID EQUALS EXPRESSION 
                            '''
    
#     if( len(p) == 2):
#         p[0] = p[1]
        
#     elif ( len(p) == 4):
#         p[0] = (p[1],p[3])
# #    
    if( len(p) == 2):
        p[0] = {'NODE_TYPE':'VAR_INITIALIZE', 'IDENTIFIER': p[1]['IDENTIFIER'], 'ARRAY_DIMENTION':p[1]['ARRAY_DIMENTION'],'VAL1':p[1]['VAL1'],'VAL2':p[1]['VAL2'], 'INITIALISED':''}
    elif ( len(p) == 4):
        p[0] = {'NODE_TYPE':'VAR_INITIALIZE', 'IDENTIFIER': p[1]['IDENTIFIER'], 'ARRAY_DIMENTION':p[1]['ARRAY_DIMENTION'],'VAL1':p[1]['VAL1'],'VAL2':p[1]['VAL2'], 'INITIALISED':p[3]}
    

def p_VAR_DECLARATION_ID(p):
    ''' VAR_DECLARATION_ID : IDENTIFIER
                    | IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET
                    | IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET LEFTBRACKET INT_CONSTANT RIGHTBRACKET
                    | LEFTBRACKET INT_CONSTANT RIGHTBRACKET IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET   
                    | LEFTBRACKET RIGHTBRACKET IDENTIFIER LEFTBRACKET INT_CONSTANT RIGHTBRACKET
                    | LEFTBRACKET INT_CONSTANT RIGHTBRACKET LEFTBRACKET INT_CONSTANT RIGHTBRACKET IDENTIFIER
                    | LEFTBRACKET VARIABLE_TYPE RIGHTBRACKET IDENTIFIER 
                    '''         #inp[string] array1;
#    print 'sahil'
    # if(len(p) == 2 ):
    #     p[0] = (p[1])
    # elif(len(p) == 5):
    #     p[0] = (p[1],p[3])
    # else:
    #     p[0] = (p[1],p[3],p[6])
    if(len(p) == 2 ):
        p[0] = {'NODE_TYPE' : 'VAR_DECLARATION_ID', 'IDENTIFIER' : p[1],  'ARRAY_DIMENTION':0,'VAL1': '','VAL2':''}
        #print p[1]
    elif(len(p) == 5):
        p[0] = {'NODE_TYPE': 'VAR_DECLARATION_ID', 'IDENTIFIER' : p[1],'ARRAY_DIMENTION':1, 'VAL1': p[3],'VAL2':''}
    else:
        p[0] = {'NODE_TYPE': 'VAR_DECLARATION_ID', 'IDENTIFIER' : p[1], 'ARRAY_DIMENTION':2,'VAL1': p[3],'VAL2':p[6]}
        


def p_VARIABLE_TYPE (p):
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
    # p[0] = p[1]
    #
    p[0] = {'NODE_TYPE': 'VARIABLE_TYPE', 'DATA_TYPE': p[1]}
    #print p[1]
    


def p_RETURN_STATEMENT(p):
    '''RETURN_STATEMENT : RETURN EXPRESSION SEMICOLON
                    | RETURN SEMICOLON
                    '''
    # if(len(p) == 3):
    #     p[0] = ('RETURN')
    # else:
    #     p[0] = ('RETURN',p[2])
    if(len(p) == 2):
        p[0] = {'NODE_TYPE':'RETURN_STATEMENT', 'EXPRESSION':p[2], 'VALUE':'RETURN'}

    else:
        p[0] = {'NODE_TYPE':'RETURN_STATEMENT', 'EXPRESSION':'', 'VALUE':'RETURN'}

    #  

def p_BREAK_STATEMENT(p):
    ''' BREAK_STATEMENT : BREAK SEMICOLON
                    '''
    # p[0]=('BREAK')
    p[0] = {'NODE_TYPE':'BREAK_STATEMENT', 'VALUE':'BREAK'}
    

def p_EXPRESSION (p):
    ''' EXPRESSION : DATA_OBJECT EQUALS EXPRESSION
                    | DATA_OBJECT PLUSPLUS
                    | DATA_OBJECT MINUSMINUS
                    | DATA_OBJECT PLUS_EQUAL EXPRESSION
                    | DATA_OBJECT MINUS_EQUAL EXPRESSION
                    | DATA_OBJECT NOR_EQUAL EXPRESSION
                    | SIMPLE_EXPRESSION
                    '''
    # if(len(p)==4):
    #      p[0] = (p[2],p[1],p[3])   

    # elif(len(p)==3):
    #     p[0] = (p[2],p[1])

    # else:
    #     p[0] = p[1]
    if(len(p)==2):
        p[0]={'NODE_TYPE':'EXPRESSION','DATA_TYPE': p[1]['DATA_TYPE'] , 'EXPRESSION': p[1] ,'OPERATOR':''}
        
    elif(len(p)==3):
        p[0]= {'NODE_TYPE':'EXPRESSION','DATA_TYPE': p[1]['DATA_TYPE'] ,'LEFT_EXPR': p[1] ,'OPERATOR' : p[2][1]}

    else:
        if (p[1]['DATA_TYPE'] != p[3]['DATA_TYPE']):
            
            print "ERROR!!: '",p[2],"' can\'t operate between ", p[1]['DATA_TYPE'], " ,",  p[3]['DATA_TYPE']
            sys.exit()
        p[0]= {'NODE_TYPE':'EXPRESSION', 'DATA_TYPE' : p[1]['DATA_TYPE'],'LEFT_EXPR': p[1], 'OPERATOR' : p[2][1], 'RIGHT_EXPR':p[3]}



def p_SIMPLE_EXPRESSION (p):
    ''' SIMPLE_EXPRESSION : SIMPLE_EXPRESSION OR ANDOP_EXPRESSION
                            | ANDOP_EXPRESSION
                            
                            '''
    # if(len(p)==4):
    #     p[0] = (p[2][0],p[1],p[3])
  
    if(len(p)==2):
        p[0]={'NODE_TYPE':'SIMPLE_EXPRESSION','DATA_TYPE':p[1]['DATA_TYPE'],'OPERATOR':'','EXPRESSION':p[1]}

    # else:
    #     p[0] = p[1]
    # #  
    else:
        if(p[1]['DATA_TYPE'] != p[3]['DATA_TYPE']):
            print "ERROR!!: " , p[1]['DATA_TYPE'], " not same as ", p[3]['DATA_TYPE']
            sys.exit()
        p[0]={'NODE_TYPE':'SIMPLE_EXPRESSION', 'DATA_TYPE':p[1]['DATA_TYPE'],'OPERATOR':'or','LEFT_EXPR':p[1], 'RIGHT_EXPR':p[3]}

def p_ANDOP_EXPRESSION (p):
    ''' ANDOP_EXPRESSION : ANDOP_EXPRESSION AND UNARY_RELATION_EXPRESSION
                        | UNARY_RELATION_EXPRESSION
                        '''
    # if(len(p)==4):
    #     p[0] = (p[2][0],p[1],p[3])
    if(len(p)==2):
        p[0]={'NODE_TYPE':'ANDOP_EXPRESSION','DATA_TYPE':p[1]['DATA_TYPE'],'OPERATOR':'','EXPRESSION':p[1]}
                
    # else:
    #     p[0] = p[1]
    # #    
    else:
        if(p[1]['DATA_TYPE'] != p[3]['DATA_TYPE']):
            print "ERROR!!: " , p[1]['DATA_TYPE'], " not same as ", p[3]['DATA_TYPE'] , "  at NODE_TYPE: ANDOP_EXPRESSION"
            sys.exit()
        p[0]={'NODE_TYPE':'ANDOP_EXPRESSION', 'DATA_TYPE':p[1]['DATA_TYPE'],'OPERATOR':'and','LEFT_EXPR':p[1], 'RIGHT_EXPR':p[3]}



def p_UNARY_RELATION_EXPRESSION(p):
    '''UNARY_RELATION_EXPRESSION : NOT UNARY_RELATION_EXPRESSION
                            | RELATIONAL_EXPRESSION
                            '''
    # if(len(p) == 3):
    #     p[0] = p[2]
    # else:
    #     p[0] = p[1]
    if(len(p) == 3):
        p[0] = {'NODE_TYPE':'UNARY_RELATION_EXPRESSION', 'DATA_TYPE':p[2]['DATA_TYPE'],'OPERATOR':'not','EXPRESSION':p[2]}
    else:
        p[0] = {'NODE_TYPE':'UNARY_RELATION_EXPRESSION', 'DATA_TYPE':p[1]['DATA_TYPE'],'OPERATOR':'','EXPRESSION':p[1]}
        

def p_RELATIONAL_EXPRESSION (p):
    ''' RELATIONAL_EXPRESSION : SUM_EXPRESSION LESSER SUM_EXPRESSION
                        | SUM_EXPRESSION GREATER SUM_EXPRESSION
                        | SUM_EXPRESSION LESSER_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION GREATER_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION NOT_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION EQUAL_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION
                        '''
    # if(len(p)==4):
    #     p[0] = (p[2][0],p[1],p[3])
    # else:
    #     p[0] = p[1]

    if(len(p)==2):
        p[0]={'NODE_TYPE':'RELATIONAL_EXPRESSION','DATA_TYPE':p[1]['DATA_TYPE'],'OPERATOR':'','EXPRESSION':p[1]}
    else:
        if(p[1]['DATA_TYPE'] != p[3]['DATA_TYPE']):
            print "ERROR!!: " , p[1]['DATA_TYPE'], " is not same as ", p[3]['DATA_TYPE'], "  at NODE_TYPE: RELATIONAL_EXPRESSION"
            sys.exit()
        
        p[0]={'NODE_TYPE':'RELATIONAL_EXPRESSION', 'DATA_TYPE':'bool' ,'OPERATOR':p[3]['OPERATOR'],'LEFT_SUM_EXPR':p[1], 'RIGHT_SUM_EXPR':p[3]}
        


def p_SUM_EXPRESSION(p):
    ''' SUM_EXPRESSION : SUM_EXPRESSION PLUS term
                        | SUM_EXPRESSION MINUS term
                        | SUM_EXPRESSION BITWISENOR term 
                        | term
                        '''
    # if(len(p) == 4):
    #     p[0] = (p[2][0],p[1],p[3])
        
    if(len(p) == 2):
        p[0] = {'NODE_TYPE':'SUM_EXPRESSION','DATA_TYPE':p[1]['DATA_TYPE'], 'OPERATOR':'','EXPRESSION':p[1]}
    # else:
    #     p[0] = p[1]
    
    else:
        if(p[1]['DATA_TYPE'] != p[3]['DATA_TYPE']):
            print "ERROR!!:" , p[1]['DATA_TYPE'], " is not same as  ", p[3]['DATA_TYPE'] , " at NODE_TYPE: SUM_EXPRESSION"
            sys.exit()
        p[0] = {'NODE_TYPE':'SUM_EXPRESSION','DATA_TYPE':p[1]['DATA_TYPE'], 'LEFT_EXPR':p[1], 'OPERATOR':p[2][1]  ,'RIGHT_EXPR':p[3]}
        

def p_term (p):
    ''' term : term STAR UNARY_EXPRESSION
                | term DIVIDE UNARY_EXPRESSION
                | term MOD UNARY_EXPRESSION
                | UNARY_EXPRESSION
                '''
    # if(len(p) == 4):
    #     p[0] = (p[2][0],p[1],p[3])
    # else:
    #     p[0] = p[1]    
    if(len(p) == 2):
        p[0] = {'NODE_TYPE':'term', 'DATA_TYPE':p[1]['DATA_TYPE'],'OPERATOR':'','EXPRESSION':p[1]}
                
    else:
        if(p[1]['DATA_TYPE'] != p[3]['DATA_TYPE']):
            print "ERROR!!: " , p[1]['DATA_TYPE'], "is not same as ", p[3]['DATA_TYPE'], " at DATA_TYPE: term"
            sys.exit()
        p[0] = {'NODE_TYPE':'term', 'DATA_TYPE':p[1]['DATA_TYPE'] ,'LEFT_EXPR':p[1],'OPERATOR': p[2],'RIGHT_EXPR': p[3]}
        


def p_UNARY_EXPRESSION(p):
    ''' UNARY_EXPRESSION : UNARY_OPERATOR UNARY_EXPRESSION
                        | factor
                        '''
    # if(len(p) == 3):
    #     p[0] = (p[1][0],p[2])
    # else:
    #     p[0] = p[1]
    if(len(p) == 2):
        p[0] = {'NODE_TYPE':'UNARY_EXPRESSION','DATA_TYPE':p[1]['DATA_TYPE'],'factor':1,'OPERATOR':'','EXPRESSION':p[1]}

    else:
        p[0] = {'NODE_TYPE':'UNARY_EXPRESSION', 'DATA_TYPE':p[2]['DATA_TYPE'], 'factor':0,'OPERATOR':p[1]['OPERATOR'], 'EXPRESSION':p[2]}
        

def p_UNARY_OPERATOR(p):
    '''UNARY_OPERATOR : MINUS
                | STAR
                '''
    p[0] = p[1][0]
    #
    
def p_factor(p):
    ''' factor : DATA_OBJECT
                | STRUCT_EXPR
                '''
    # p[0] = p[1]
    p[0] = {'NODE_TYPE':'factor', 'DATA_TYPE': p[1]['DATA_TYPE'] , 'SUBTYPE':p[1]['NODE_TYPE'],'EXPRESSION':p[1]}
    

def p_DATA_OBJECT(p):
    ''' DATA_OBJECT : IDENTIFIER
                | IDENTIFIER LEFTBRACKET EXPRESSION RIGHTBRACKET
                | IDENTIFIER LEFTBRACKET EXPRESSION RIGHTBRACKET LEFTBRACKET EXPRESSION RIGHTBRACKET
                | IDENTIFIER LEFTBRACKET INT_CONSTANT DOT DOT INT_CONSTANT RIGHTBRACKET
                | IDENTIFIER LEFTBRACKET INT_CONSTANT DOT DOT IDENTIFIER DOT IDENTIFIER RIGHTBRACKET                 
                |  IDENTIFIER DOT IDENTIFIER
                '''
    # print 'sahil'            
    # if(len(p) == 2):
    #     p[0] = p[1]

    # elif (len(p) == 5 or len(p) == 4 ):
    #     p[0] = (p[1],p[3])
    # else:
    #     p[0]=(p[1],p[3],p[6])
    #    

    if(currentSymbolTable.lookup(p[1])== False):
        if(parametersymboltable.lookup(p[1]) == False):
            print "ERROR!!: in DATA_OBJECT ",  p[1] , " not declared: ",
            sys.exit()

    var_data_type = currentSymbolTable.lookup(p[1])['attributes']['DATA_TYPE']
    var_table = currentSymbolTable.lookup(p[1])['TABLE']
    var_offset = currentSymbolTable.lookup(p[1])['offset']
    var_scope = currentSymbolTable.lookup(p[1])['attributes']['SCOPE']    
    Is_static = currentSymbolTable.lookup(p[1])['attributes']['STATIC']
    var_index1 = currentSymbolTable.lookup(p[1])['attributes']['VAL1']
    var_index2 = currentSymbolTable.lookup(p[1])['attributes']['VAL2']
    if(len(p) == 2):
        p[0] = {'NODE_TYPE':'DATA_OBJECT','IDENTIFIER':p[1],'DATA_TYPE':var_data_type,'ARRAY_DIMENTION':0, 'OFFSET':var_offset,'SCOPE':var_scope,'TABLE':var_table,'STATIC':Is_static}

    elif (len(p) == 5):
        p[0] = {'NODE_TYPE':'DATA_OBJECT', 'IDENTIFIER':p[1], 'DATA_TYPE': var_data_type,'ARRAY_DIMENTION':1,'EXPRESSION':p[3], 'OFFSET':var_offset,'SCOPE':var_scope,'TABLE':var_table,'STATIC':Is_static}
    else:
        p[0] = {'NODE_TYPE':'DATA_OBJECT', 'IDENTIFIER':p[1],'VAL1':var_index1,'VAL2':var_index2, 'DATA_TYPE': var_data_type,'ARRAY_DIMENTION':2,'EXPRESSION1':p[3],'EXPRESSION2':p[6], 'OFFSET':var_offset,'SCOPE':var_scope,'TABLE':var_table,'STATIC':Is_static}
        

def p_STRUCT_EXPR(p):
    ''' STRUCT_EXPR : LEFTPAR EXPRESSION RIGHTPAR
                    | LEFTBRACKET LIST_OF_CONSTANTS RIGHTBRACKET
                    | CONSTANT
                    | FUNCTION_INSTANCE                    
                    '''
    # if(len(p) == 4):
    #     p[0] = p[2]
    # else:
    #     p[0] = p[1]
    ####################################################
    if(len(p) == 4):
        p[0] = {'NODE_TYPE':'STRUCT_EXPR', 'DATA_TYPE':p[2]['DATA_TYPE'] , 'SUBTYPE':'NESTED_EXPR','EXPRESSION':p[2], 'IS_NESTED':1}
    elif(p[1]['NODE_TYPE'] == 'FUNCTION_INSTANCE'):
        p[0] = {'NODE_TYPE':'STRUCT_EXPR', 'DATA_TYPE':p[1]['DATA_TYPE'], 'SUBTYPE':'FUNCTION_INSTANCE','IDENTIFIER':p[1]['IDENTIFIER'], 'ARGUMENTS':p[1]['ARGUMENTS']}
    else:
        p[0] = {'NODE_TYPE':'STRUCT_EXPR', 'DATA_TYPE':p[1]['DATA_TYPE'] , 'SUBTYPE':'CONSTANT','VALUE':p[1]['VALUE']}
        


def p_FUNCTION_INSTANCE (p):
    ''' FUNCTION_INSTANCE : IDENTIFIER LEFTPAR FUNC_ARGUMENTS RIGHTPAR
            '''
    p[0] = {'NODE_TYPE':'FUNCTION_INSTANCE', 'IDENTIFIER':p[1], 'ARGUMENTS':p[3], 'DATA_TYPE':''}
    global FUNCTION_PROTOTYPES
    temp = 0
    if(p[1] != 'writefln' and p[1] != 'readf' and  p[1] != 'write'  ):
        for f in FUNCTION_PROTOTYPES :
                if(p[1] in f['FUNC_NAME']):
                    temp=1
                    p[0]['DATA_TYPE'] = f['OUTPUT']
                    break
        if(temp == 0):
            print p[1],"Function not Declared!!"
            sys.exit()
        else :
            if(len(p[3]) != len(f['INPUT'])):
                print p[3]
                print f
                print "Different number of arguments for function ", f['NAME']
                sys.exit()
            tmp = 0
            for var in f['INPUT']:
                if(p[3][count]['DATA_TYPE'] != var['DATA_TYPE']):
                    print "Mismatch in Argument type for function ", f['NAME']
                    sys.exit()

def p_FUNC_ARGUMENTS(p):
    ''' FUNC_ARGUMENTS : LIST_OF_FUNCTION_ARGUMENTS
            |
            '''
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = []
    #     
    #
    
        
def p_LIST_OF_FUNCTION_ARGUMENTS(p):
    ''' LIST_OF_FUNCTION_ARGUMENTS : LIST_OF_FUNCTION_ARGUMENTS COMMA EXPRESSION
                    | EXPRESSION
                    '''
    if(len(p) == 4):
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]
    #     

def p_LIST_OF_CONSTANTS(p):
    ''' LIST_OF_CONSTANTS : STRING_CONSTANT COLON SIMPLE_EXPRESSION COMMA LIST_OF_CONSTANTS
                            | STRING_CONSTANT COLON SIMPLE_EXPRESSION
                    '''
    p[0] = p[1]   

def p_CONSTANT(p):
    ''' CONSTANT : INT_CONST
                    | FLOAT_CONST
                    | CHAR_CONST
                    | STR_CONST
                    '''
    # p[0] = p[1]               
    p[0] = {'NODE_TYPE':'CONSTANT','VALUE':p[1]['VALUE'], 'DATA_TYPE':p[1]['DATA_TYPE']}
    
def p_INT_CONST(p):
    ''' INT_CONST : INT_CONSTANT
                '''
    p[0] ={'NODE_TYPE':'INT_CONST','DATA_TYPE':'int','VALUE':p[1][0]}
    
    # p[0] = p[1]           

def p_FLOAT_CONST (p):
    ''' FLOAT_CONST : FLOAT_CONSTANT
                '''
    # p[0] = p[1]
    p[0] = {'NODE_TYPE':'FLOAT_CONST','DATA_TYPE':'float','VALUE':p[1][0]}

def p_STR_CONST (p):
    ''' STR_CONST : STRING_CONSTANT
                '''
    # p[0] = p[1]
    p[0] ={'NODE_TYPE':'STR_CONST','DATA_TYPE':'string','VALUE':p[1][0]}
    
def p_LEFTBRACES(p):
    ''' LEFTBRACES : LEFTBRACE
                    '''
    p[0] = p[1]
    #print "-----Making NewSymbolTable---------"
    global currentSymbolTable
    currentSymbolTable = SymbolTable(currentSymbolTable)
    print p[0]

def p_RIGHTBRACES(p):
    ''' RIGHTBRACES : RIGHTBRACE
                    '''
    p[0] = p[1]
    #print "--------EXITING CURRENT SYMBOL TABLE--------------"
    global currentSymbolTable
    print p[0]
    currentSymbolTable = currentSymbolTable.father

 
def p_CHAR_CONST (p):
    ''' CHAR_CONST : CHAR_CONSTANT
                '''
    # p[0]=p[1]
    p[0] ={'NODE_TYPE':'CHARCTER_CONST','DATA_TYPE':'char','VALUE':p[1]}
    
def p_error(p):
    print "Parse Time Error!! at token",t.type," ", t.value," ", t.lineno

import logging
logging.basicConfig(
    level=logging.INFO,
    filename="parselog.txt"
)

parser = yacc.yacc()
data =' int main (){   int i = 2+4 ; for(i=0 ; i<10 ; i++)   {      writefln("This loop will run forever.");  }    return 0; }'

print parser.parse(data, debug=logging.getLogger())

