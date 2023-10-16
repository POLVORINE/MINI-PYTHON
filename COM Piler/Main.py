# LIBRERIAS
from tkinter import filedialog
import ply.lex as lex
import ply.yacc as yacc
import customtkinter as ctk
import re

# Lista de palabras reservadas
reserved = {
    'inicio': 'INICIO',
    'fin': 'FIN',
    'if': 'IF',
    'while': 'WHILE',
    'print': 'PRINT',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',

}
# Definición de tokens
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
# DIRECTIVAS
directivas_table = []
symbol_table = []


# REGLAS MAS ESPECIFICAS
#       IDENTIFICADORES
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
    sintaxerror.insert("0.0", 'Programa sintacticamente correcto')


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
    ASIGNACION : INT ID IGUAL EXPRESION
                | STRING ID IGUAL CADENA
                | FLOAT ID IGUAL EXPRESION
    """


def p_EXPRESION(p):
    """
    EXPRESION : NUM
                       | ID
                       | OPERACION
    """


def p_OPERACION(p):
    """
    OPERACION :  EXPRESION OPARIT EXPRESION
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
    PRINTINSTR : PRINT APERTUPAR CADENA CIERREPAR
                | PRINT APERTUPAR EXPRESION   CIERREPAR
    """


def p_error(p):
    token_str = str(p.value)
    if p is not None:
        sintaxerror.insert("0.0", "Error de sintaxis en la entrada :" + token_str)
    else:
        sintaxerror.insert("0.0", 'Error sintaxis por token no reconocido' + token_str)


# Constructor del lexer
lexer = lex.lex()

# Constructor del Parser
parser = yacc.yacc()


def botonscanner():  # scanner
    # programa ejemplo
    tablatokens.delete("1.0", "end")
    textoprocesado = "Token Type\tToken Value\n"
    progejemplo = codigofuente.get("1.0", "end-1c")
    lexer.input(progejemplo)  # mandamos lo que esta en el cuadro de texto para el lexer
    for token in lexer:  # por cada token que encuentre en el programa ejemplo
        token_type = token.type
        token_value = token.value
        formatted_token = f"{token_type}\t{token_value}\n"
        textoprocesado += formatted_token
    # imprime a la izquierda lo que encontro
    tablatokens.insert('1.0', textoprocesado)


def botonparser():
    sintaxerror.delete("1.0", "end")
    progejemplo = codigofuente.get("1.0", "end-1c")
    parser.parse(progejemplo)


def botonsemantico():
    global symbol_table
    semantico.delete("1.0", "end")
    symbol_table.clear()
    progejemplo = codigofuente.get("1.0", "end-1c")
    patrondeclaraciones = r'\b(\w+)\s+(\w+)\s*=\s*([\'"]?[\w.]+[\'"]?)'
    patronexpresiones = r'\b(\w+)\s+(\w+)\s*=\s*([0-9]+|[\w.+\-*/]+)'
    variable_declarations = re.findall(patrondeclaraciones, progejemplo)
    variable_expresion = re.findall(patronexpresiones, progejemplo)
    for declaration in variable_declarations:
        TYPE, ID, VALOR = declaration
        a = {"TYPE": TYPE, "ID": ID, "VALOR": VALOR}
        symbol_table.append(a)
    for declaration in variable_expresion:
        TYPE, ID, EXPRESION = declaration
        a = {"TYPE": TYPE, "ID": ID, "EXPRESION": EXPRESION}
        symbol_table.append(a)

    imprimir = '\n'.join([str(a) for a in symbol_table])
    semantico.insert('1.0', imprimir)


def botontraducir():
    botonsemantico()
    global symbol_table
    intermedio.delete("1.0", "end")
    ensamblador = ""
    line1 = "section.data"
    ensamblador += line1 + "\n"
    for a in symbol_table:
        if a["TYPE"] == 'int':
            i = f"{a['ID']} dw {a['VALOR']}   ;"
            ensamblador += i + "\n"
        if a["TYPE"] == 'float':
            f = f"{a['ID']} dd {a['VALOR']}   ;"
            ensamblador += f + "\n"
        if a["TYPE"] == 'string':
            s = f"{a['ID']} db {a['VALOR']}  ;"
            ensamblador += s + "\n"
    line1 = "section.text"
    ensamblador += line1 + "\n"
    line1 = "global main "
    ensamblador += line1 + "\n"
    line1 = "main"
    ensamblador += line1 + "\n"

    intermedio.insert('1.0', ensamblador)


def botonrun():
    botonscanner()
    botonparser()
    botontraducir()


def botonsalir():
    ventana.quit()


def botonopenfile():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                text_content = file.read()
                codigofuente.delete(1.0, ctk.END)  # Clear existing content
                codigofuente.insert(ctk.END, text_content)  # Insert file content
        except Exception as e:
            codigofuente.delete(1.0, ctk.END)
            codigofuente.insert(ctk.END, f"Error reading file: {str(e)}")


def botonsavefile():
    # Get the content from the textbox
    content = codigofuente.get("1.0", "end-1c")

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if file_path:
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Saved as: {file_path}")


# DE AQUI PARA ABAJO ES GRAFICACION
# personalizacion
#   TAMAÑO Y TIPO DE FUENTE DE LA APLICACION
fuente = ("Helvetica", 16)
radio = 10
grosor = 10
nomcomp = "COM PILER"
nomgramatica = "MICRO PYTHON"
#   COLORES DE LA INTERFAZ
color_morado = "#4d3f62"
color_gris = "#40434f"
color_gris3 = "#282a36"
color_gris2 = "#3a3d4c"
color_rojo = "#FE4A49"
# Crear una ventana
ventana = ctk.CTk()
ventana.title("COM PAILER")
# tamaño de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()
# llenar la pantalla
ventana.geometry(f"{screen_width}x{screen_height}")
# Configurar la geometría DEL GRID principal
ventana.grid_rowconfigure(0, weight=1)
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_rowconfigure(2, weight=30)
ventana.grid_rowconfigure(3, weight=1)
ventana.grid_rowconfigure(4, weight=1)
ventana.grid_rowconfigure(5, weight=1)
################################################################
ventana.grid_columnconfigure(0, weight=3)
ventana.grid_columnconfigure(1, weight=10)
ventana.grid_columnconfigure(2, weight=10)
ventana.grid_columnconfigure(3, weight=10)
ventana.grid_columnconfigure(4, weight=10)
ventana.grid_columnconfigure(5, weight=10)
ventana.grid_columnconfigure(6, weight=10)
ventana.grid_columnconfigure(7, weight=3)
# OBJETOS DE LA INTERFAZ
titulo = ctk.CTkLabel(ventana, text=nomcomp, bg_color=color_morado)
titulo.grid(row=0, columnspan=2, sticky='nsew')
titulo.grid_propagate(False)
boton_open = ctk.CTkButton(ventana, fg_color=color_gris, text='open file', command=botonopenfile)
boton_open.grid(row=0, column=2, sticky='nsew')
boton_open.grid_propagate(False)
boton_save = ctk.CTkButton(ventana, fg_color=color_gris2, text='save file', command=botonsavefile)
boton_save.grid(row=0, column=3, sticky='nsew')
boton_save.grid_propagate(False)
boton_run = ctk.CTkButton(ventana, fg_color=color_gris, text='run program', command=botonrun)
boton_run.grid(row=0, column=4, sticky='nsew')
boton_run.grid_propagate(False)
boton_scanner = ctk.CTkButton(ventana, fg_color=color_gris2, text='scanner', command=botonscanner)
boton_scanner.grid(row=0, column=5, sticky='nsew')
boton_scanner.grid_propagate(False)
boton_codinter = ctk.CTkButton(ventana, fg_color=color_gris, text='traducir', command=botontraducir)
boton_codinter.grid(row=0, column=6, sticky='nsew')
boton_codinter.grid_propagate(False)
################################################################
boton_semantico = ctk.CTkButton(ventana, fg_color=color_morado, text='tabla de simbolos', command=botonsemantico)
boton_semantico.grid(row=3, column=1, sticky='nsew')
boton_semantico.grid_propagate(False)
boton_parser = ctk.CTkButton(ventana, fg_color=color_rojo, text='parser', command=botonparser)
boton_parser.grid(row=3, column=4, sticky='nsew')
boton_parser.grid_propagate(False)
################################################################
relleno = ctk.CTkLabel(ventana, bg_color=color_morado, text='')
relleno.grid(row=0, column=7, sticky='nsew')
relleno.grid_propagate(False)
################################################################
extrainfo = ctk.CTkLabel(ventana, text="", bg_color=color_morado)
extrainfo.grid(row=5, columnspan=8, sticky='nsew')
extrainfo.grid_propagate(False)
derecha = ctk.CTkLabel(ventana, text="", bg_color=color_gris3)
derecha.grid(row=1, column=0, rowspan=4, sticky='nsew')
derecha.grid_propagate(False)
izquierda = ctk.CTkLabel(ventana, text="", bg_color=color_gris3)
izquierda.grid(row=1, column=7, rowspan=4, sticky='nsew')
izquierda.grid_propagate(False)
################################################################
nombredelprograma = ctk.CTkLabel(ventana, text="CODIGO", bg_color=color_gris3)
nombredelprograma.grid(row=1, column=1, columnspan=4, sticky='nsew')
nombredelprograma.grid_propagate(False)
codigofuente = ctk.CTkTextbox(ventana, fg_color=color_gris2, font=fuente)
codigofuente.grid(row=2, column=1, columnspan=4, sticky='nsew')
codigofuente.grid_propagate(False)
########################################################################
label10 = ctk.CTkLabel(ventana, text="LISTA DE TOKENS", bg_color=color_morado)
label10.grid(row=1, column=5, sticky='nsew')
tablatokens = ctk.CTkTextbox(ventana, fg_color=color_gris, font=fuente)
tablatokens.grid(row=2, column=5, sticky='nsew')
tablatokens.grid_propagate(False)
########################################################################
label12 = ctk.CTkLabel(ventana, text="CODIGO INTERMEDIO", bg_color=color_rojo)
label12.grid(row=1, column=6, sticky='nsew')
intermedio = ctk.CTkTextbox(ventana, fg_color=color_gris2, font=fuente)
intermedio.grid(row=2, column=6, sticky='nsew')
intermedio.grid_propagate(False)
##########################
sintaxerror = ctk.CTkTextbox(ventana, fg_color=color_gris, font=fuente)
sintaxerror.grid(row=4, column=4, columnspan=3, sticky='nsew')
sintaxerror.grid_propagate(False)
semantico = ctk.CTkTextbox(ventana, fg_color=color_gris2, font=fuente)
semantico.grid(row=4, column=1, columnspan=3, sticky='nsew')
semantico.grid_propagate(False)
# Iniciar  la aplicación/inferfaz
ventana.mainloop()
