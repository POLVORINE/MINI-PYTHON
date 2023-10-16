# Lista de palabras reservadas
reserved = {
    'inicio': 'INICIO',
    'fin': 'FIN',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT',
    'read': 'READ',
}
# Definición de tokens
tokens = [
             'ID',
             'NUM',
             'CADENA',
             'OPARIT',
             'OPRELAC',
             'SIMBOLOS',
             'IGUAL',
             'APERTUPAR',
             'CIERREPAR',
             'AUMENTO',
             'DECREMENTO'
         ] + list(reserved.values())

# Definición de la gramática
t_NUM = r'([0-9]*)[0-9]'
t_CADENA = r"'([^']*)'"
t_OPARIT = r'[+\-*/]'
t_OPRELAC = r'<|>|==|<=|>=|!='
t_SIMBOLOS = r'[,;]'
t_IGUAL = r'\='
t_APERTUPAR = r'\('
t_CIERREPAR = r'\)'


# REGLAS MAS ESPECIFICAS
#       IDENTIFICADORES
def t_ID(t):
    r"""[a-zA-Z_][a-zA-Z0-9_]*"""
    t.type = reserved.get(t.value, 'ID')
    return t


#       AUMENTO
def t_AUMENTO(t):
    r"""\+\+"""
    return t


#       DRECREMENTO
def t_DECREMENTO(t):
    r"""\-\-"""
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
    print("Programa sintacticamente correcto")
    label2.config(text='Programa sintacticamente correcto')


def p_ListaInstrucciones(p):
    """
    ListaInstrucciones : INSTRUCCION
                      | ListaInstrucciones INSTRUCCION
    """


def p_INSTRUCCION(p):
    """
    INSTRUCCION : ASIGNACION
                | IFINSTR
                | WHILEINSTR
                | PRINTINSTR
    """


def p_ASIGNACION(p):
    """
    ASIGNACION : ID IGUAL EXPRESION
    """


def p_EXPRESION(p):
    """
    EXPRESION : NUM
                       | ID
                       | CADENA
    """


def p_IFINSTR(p):
    """
    IFINSTR : IF  CONDICION  APERTUPAR ListaInstrucciones CIERREPAR
    """


def p_CONDICION(p):
    """
    CONDICION :  APERTUPAR EXPRESION OPRELAC EXPRESION CIERREPAR
    """


def p_WHILEINSTR(p):
    """
    WHILEINSTR : WHILE CONDICION APERTUPAR ListaInstrucciones CIERREPAR
    """


def p_PRINTINSTR(p):
    """
    PRINTINSTR : PRINT APERTUPAR EXPRESION CIERREPAR
    """


def p_error(p):
    token_str = str(p.value)
    if p is not None:
        print("Error de sintaxis en la entrada:", p)
        label2.config(text="Error de sintaxis en la entrada :" + token_str)
    else:
        print("Error de sintaxis en la entrada:", p, "Token no reconocido")
        label2.config(text='Error sintaxis por token no reconocido')


