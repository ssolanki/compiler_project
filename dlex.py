# -----------------------------------------------------------------------------------
#   CS335: Compiler Design (Dec 2014 - May 2015)                                     
#   Assignment 1                                                                     
#                                                                                    
#   Authors: Abhay Kumar(11008), Sahil Solanki(11624), Swaroop Singh Deval(11756)    
#   Group Number: G28                                                                
#   File: dlex.py                                                                    
# -----------------------------------------------------------------------------------

import sys
import ply.lex as lex
reserved =( 
  # Reserved words
    'ABSTRACT', 'ALIAS', 'ALIGN', 'ASM', 'ASSERT', 'AUTO', 'BODY', 'BOOL', 'BREAK', 'BYTE',
     'CASE', 'CAST', 'CATCH', 'CDOUBLE', 'CENT', 'CFLOAT', 'CHAR', 'CLASS', 'CONST', 'CONTINUE',
      'CREAL', 'DCHAR', 'DEBUG', 'DEFAULT', 'DELEGATE', 'DELETE', 'DEPRECATED', 'DO', 'DOUBLE', 'ELSE',
       'ENUM', 'EXPORT', 'EXTERN', 'FALSE', 'FINAL', 'FINALLY', 'FLOAT', 'FOR', 'FOREACH', 'FOREACH_REVERSE', 
       'FUNCTION', 'GOTO', 'IDOUBLE', 'IF', 'IFLOAT', 'IMMUTABLE', 'IMPORT', 'IN', 'INOUT', 'INT', 'INTERFACE', 
       'INVARIANT', 'IREAL', 'IS', 'LAZY', 'LONG', 'MACRO', 'MIXIN', 'MODULE', 'NEW', 'NOTHROW', 'NULL', 'OUT',
        'OVERRIDE', 'PACKAGE', 'PRAGMA', 'PRIVATE', 'PROTECTED', 'PUBLIC', 'PURE', 'REAL', 'REF', 'RETURN', 'SCOPE',
         'SHARED', 'STRING', 'SHORT', 'STATIC', 'STRUCT', 'SUPER', 'SWITCH', 'SYNCHRONIZED', 'TEMPLATE', 'THIS', 'THROW',
          'TRUE', 'TRY', 'TYPEDEF', 'TYPEID', 'TYPEOF', 'UBYTE', 'UCENT', 'UINT', 'ULONG', 'UNION', 'UNITTEST', 
          'USHORT', 'VERSION', 'VOID', 'VOLATILE', 'WCHAR', 'WHILE', 'WITH', '__FILE__', '__MODULE__', '__LINE__',
           '__FUNCTION__', '__PRETTY_FUNCTION__', '__GSHARED', '__TRAITS', '__VECTOR', '__PARAMETERS'
           )         
tokens = reserved + (
  #Literals 
   'IDENTIFIER', 'CHAR_CONSTANT', 'FLOAT_CONSTANT','INT_CONSTANT', 'STRING_CONSTANT',

  #Arithmetic Operators in this order: + - * / % ++ --      
        'PLUS', 'MINUS', 'STAR', 'DIVIDE', 'MOD', 'PLUSPLUS','MINUSMINUS',
  #Relational Operators : == != > < >= <=
        'EQUAL_EQUAL','NOT_EQUAL','GREATER','LESSER','GREATER_EQUAL','LESSER_EQUAL',
  #Logical Operators : && || !
        'AND','OR','NOT',
  #Bitwise Operators: & | ^  ~ << >>
        'BITWISEAND', 'BITWISEOR', 'BITWISEXOR' ,'BITWISENOR', 'LEFTSHIFT', 'RIGHTSHIFT',
  #Assignment Operators : = += -= *= /= %= <<= >>= &= ^= |= ,~=,     

       'EQUALS', 'PLUS_EQUAL','MINUS_EQUAL','MULT_EQUAL','DIV_EQUAL',
        'MOD_EQUAL', 'LSHIFT_EQUAL','RSHIFT_EQUAL','AND_EQUAL','XOR_EQUAL',
        'OR_EQUAL', 'NOR_EQUAL',
  #Other Operators:  ; , . : { } ( ) [ ] ? &
      'SEMICOLON', 'COMMA','DOT', 'COLON', 'LEFTPAR',
       'RIGHTPAR', 'LEFTBRACKET','RIGHTBRACKET', 'LEFTBRACE',
       'RIGHTBRACE','CONDITIONOP'  , 'ADDRESS_AND'      
       )

reserved_map = { }
for r in reserved:
    reserved_map[r.lower()] = r

 #----------------------------------#

def t_LEFTBRACE(t):
  r'{'
  t.value = [t.value,'LEFTBRACE']
  return t

def t_RIGHTBRACE(t):
  r'}'
  t.value = [t.value,'RIGHTBRACE']
  return t

def t_MOD(t):
  r'%'
  t.value = [t.value,'MOD']
  return t

def  t_PLUSPLUS(t):
  r'\+\+'
  t.value = [t.value,'PLUSPLUS']
  return t

def t_MINUSMINUS(t):
  r'\-\-'
  t.value = [t.value,'MINUSMINUS']
  return t


def t_PLUS_EQUAL(t):
  r'\+\='
  t.type = reserved_map.get(t.value,"PLUS_EQUAL")
  return t

def t_MINUS_EQUAL(t):
  r'\-\='
  t.type = reserved_map.get(t.value,"MINUS_EQUAL")
  return t

def t_MULT_EQUAL(t):
  r'\*\='
  t.type = reserved_map.get(t.value,"MULT_EQUAL")
  return t

def t_DIV_EQUAL(t):
  r'/='
  t.type = reserved_map.get(t.value,"DIV_EQUAL")
  return t

def t_MOD_EQUAL(t):
  r'\%\='
  t.type = reserved_map.get(t.value,"MOD_EQUAL")
  return t

def t_LSHIFT_EQUAL(t):
  r'\<\<\='
  t.type = reserved_map.get(t.value,"LSHIFT_EQUAL")
  return t

def t_RSHIFT_EQUAL(t):
  r'\>\>\='
  t.type = reserved_map.get(t.value,"RSHIFT_EQUAL")
  return t


#--------------------------------------------#

def t_EQUAL_EQUAL(t):
  r'=='
  t.value = [t.value,'EQUAL_EQUAL']
  return t

def t_NOT_EQUAL(t):
  r'!='
  t.value = [t.value,'NOT_EQUAL']
  return t


def t_GREATER_EQUAL(t):
  r'\>='
  t.value = [t.value,'GREATER_EQUAL']
  return t
  
def t_LESSER_EQUAL(t):
  r'\<='
  t.value = [t.value,'LESSER_EQUAL']
  return t
def t_LESSER(t):
  r'\<'
  t.value = [t.value,'LESSER']
  return t
def t_GREATER(t):
  r'\>'
  t.value = [t.value,'GREATER']
  return t


# ..........................................................#
def t_BITWISE_AND(t):
  r'(?<=([A-Za-z0-9_]))&'
  t.value = [t.value,'BITWISE_AND']
  return t


def t_OR(t):
  r'\|\|'
  t.value = [t.value,'OR']
  return t


def t_BITWISEOR(t):
  r'\|'
  t.value = [t.value,'BITWISEOR']
  return t

def t_BITWISEXOR(t):
  r'\^'
  t.value = [t.value,'BITWISEXOR']
  return t

def t_BITWISENOR(t):
  r'~'
  t.value = [t.value,'BITWISENOR']
  return t

def t_LSHIFT(t):
  r'\<\<'
  t.value = [t.value,'LSHIFT']
  return t

def t_RSHIFT(t):
  r'\>\>'
  t.value = [t.value,'RSHIFT']
  return t

  #Logical Operator Rules : && || !

def t_AND(t):
  r'&&'
  t.value = [t.value,'AND']
  return t

def t_NOT(t):
  r'!'
  t.value = [t.value,'NOT']
  return t


def t_SEMICOLON(t):
  r';'
  t.value = [t.value,'SEMICOLON']
  return t

def t_COMMA(t):
  r','
  t.value = [t.value,'COMMA']
  return t

def t_DOT(t):
  r'\.'
  t.value = [t.value,'DOT']
  return t

def t_COLON(t):
  r':'
  t.value = [t.value,'COLON']
  return t



def t_LEFTPAR(t):
  r'\('
  t.value = [t.value,'LEFTPAR']
  return t

def t_RIGHTPAR(t):
  r'\)'
  t.value = [t.value,'RIGHTPAR']
  return t

def t_LEFTBRACKET(t):
  r'\['
  t.value = [t.value,'LEFTBRACKET']
  return t

def t_RIGHTBRACKET(t):
  r'\]'
  t.value = [t.value,'RIGHTBRACKET']
  return t

def t_CONDITIONOP(t):
  r'\?'
  t.value = [t.value,'CONDITIONOP']
  return t

def t_AND_EQUAL(t):
  r'\&\='
  t.type = reserved_map.get(t.value,"AND_EQUAL")
  return t

def t_XOR_EQUAL(t):
  r'\^\='
  t.type = reserved_map.get(t.value,"XOR_EQUAL")
  return t

def t_OR_EQUAL(t):
  r'\|\='
  t.type = reserved_map.get(t.value,"OR_EQUAL")
  return t

def t_NOR_EQUAL(t):
  r'\~\='
  t.type = reserved_map.get(t.value,"NOR_EQUAL")
  return t

#Literals 

def t_IDENTIFIER(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value,"IDENTIFIER")
    return t

def t_FLOAT_CONSTANT(t):
  r'(([0-9]*)([.]*)([0-9]+)([e]|[E])([-]?)([0-9]+))|(([0-9]*)([\.])([0-9]+))'
  t.value = [t.value,'FLOAT_CONSTANT']
  return t  

def t_INT_CONSTANT(t):
  r'(\d+([uU]|[lL]|[uU][lL]|[lL][uU])?)|(0b([0-1]+?))|(0([0-7]+?))'
  t.value = [t.value,'INT_CONSTANT']
  return t


def t_STRING_CONSTANT(t):
  r'\"([^\\\n]|(\\.))*?\"'
  t.value = [t.value,'STRING_CONSTANT']
  return t

def t_CHAR_CONSTANT(t):
  r'(L)?\'([^\\\n]|(\\.))*?\''
  t.value = [t.value,'CHAR_CONSTANT']
  return t

def t_ADDRESS_AND(t):
  r'&'
  t.value = [t.value,'ADDRESS_AND']
  return t



# correctly working now
def t_comment(t):
    r'((/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)|(/\+([^+]|[\r\n]|(\++([^+/]|[\r\n])))*\++/) )'
    t.lineno += t.value.count('\n')
    if(t.value.count('\n')):
      global temp
      temp = 0
    global lnumber
    global output
    for i in range(t.value.count('\n')):
      print output[lnumber]
      lnumber += 1


def t_EQUALS(t):
  r'='
  t.value = [t.value,'EQUALS']
  return t
def t_PLUS(t):
  r'\+'
  t.value = [t.value,'PLUS']
  return t

def t_MINUS(t):
  r'\-'
  t.value = [t.value,'MINUS']
  return t

def t_STAR(t):
  r'\*'
  t.value = [t.value,'STAR']
  return t

def t_DIVIDE(t):
  r'\/'
  t.value = [t.value,'DIVIDE']
  return t

def t_error(t):
    print " %s not defined:" % repr(t.value[0])
    t.lexer.skip(1)

t_ignore = " \t"

def t_newline(t):
  r'\n'
  global lnumber
  global temp
  print output[lnumber]
  lnumber += 1
  temp = 0



import sys
# Build the lexer
lexer = lex.lex()
# lexer.input('return (4*9-0+5)')
# while True:
#       tok = lexer.token()
#       # print tok
#       if not tok: break      # No more input
#       print tok.type

# lnumber = 0
# output = []
# temp = 0

# with open(sys.argv[1], "r") as ins:
#     data = "";
#     for line in ins:
#       data += (line)
#     output = data.split('\n')
#     # print len(output)
#     for j in range(len(output)):
#       for i in range(50-len(output[j])):
#         output[j] = output[j] + ' '

#     lexer.input(data)
#     while True:
#       tok = lexer.token()
#       # print tok
#       if not tok: break      # No more input
#       if temp == 0:
#         output[lnumber] = output[lnumber] + '\\\\'
#         temp = 1
#       output[lnumber] = output[lnumber] + ' ' + tok.type
#     print output[lnumber] #at EOF