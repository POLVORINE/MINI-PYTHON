# Librerias
import ply.lex as lex
import ply.yacc as yacc

# palabas reservadas
reserved = {
    'inicio': 'INICIO',
    'fin': 'FIN',
    'if': 'IF',
    'while': 'WHILE',
    'print': 'PRINT',
    'read': 'READ',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
}

# definion de tokens
tokens = [
             'ID',
             'NUM',
             'CADENA',
             'OPARIT',
             'OPRELAC',
             'IGUAL',
             'APERTUPAR',
             'CIERREPAR',
         ] + list(reserved.values())

# Definición de la gramática

t_NUM = r'([0-9]*)[0-9]'
t_CADENA = r"'([^']*)'"
t_OPARIT = r'[+\-*/]'
t_OPRELAC = r'<|>|==|<=|>=|!='
t_IGUAL = r'\='
t_APERTUPAR = r'\('
t_CIERREPAR = r'\)'


def t_ID(t):
    r"""[a-zA-Z_][a-zA-Z0-9_]*"""
    t.type = reserved.get(t.value, 'ID')
    return t


# Ignorar espacios en blanco y saltos de línea

t_ignore = ' \t\n'


# Función para manejar errores léxicos

def t_error(t):
    # print("Caracter no válido: '%s'" % t.value[0])
    t.lexer.skip(1)


# Reglas gramaticales

def p_programa(p):
    """Programa : INICIO ID ListaInstrucciones FIN"""
    print('Programa sintacticamente correcto')
    # sintaxerror.insert("0.0", 'Programa sintacticamente correcto')


def p_ListaInstrucciones(p):
    """
    ListaInstrucciones  : INSTRUCCION
                        | ListaInstrucciones
    """


def p_INSTRUCCION(p):
    """
    INSTRUCCION : ASIGNACION
                | IFINSTR
                | WHILEINSTR
                | PRINTINSTR
                | READINSTR
    """


def p_ASIGNACION(p):
    """
    ASIGNACION : INT ID IGUAL EXPRESION
                | STRING ID IGUAL CADENA
                | FLOAT ID IGUAL EXPRESION
    """


def p_EXPRESION(p):
    """
    EXPRESION   : NUM
                | ID
                | OPERACION
    """


def p_OPERACION(p):
    """
    OPERACION :  EXPRESION OPARIT EXPRESION
    """


def p_IFINSTR(p):
    """
    IFINSTR : IF  CONDICION  INICIO ListaInstrucciones FIN
    """


def p_CONDICION(p):
    """
    CONDICION :  APERTUPAR EXPRESION OPRELAC EXPRESION CIERREPAR
    """


def p_WHILEINSTR(p):
    """
    WHILEINSTR : WHILE CONDICION INICIO ListaInstrucciones FIN
    """


def p_PRINTINSTR(p):
    """
    PRINTINSTR  : PRINT APERTUPAR CADENA CIERREPAR
                | PRINT APERTUPAR EXPRESION   CIERREPAR
    """


def p_error(p):
    token_str = str(p.value)
    if p is not None:
        print('Error sintaxis por token no reconocido en la entrada :' + token_str)
        # sintaxerror.insert("0.0", "Error de sintaxis en la entrada :" + token_str)
    else:
        print('Error sintaxis por token no reconocido en la entrada :' + token_str)
        # sintaxerror.insert("0.0", 'Error sintaxis por token no reconocido' + token_str)


# Constructor del lexer
lexer = lex.lex()

# Constructor del Parser
parser = yacc.yacc()

