# LIBRERIAS
from tkinter import filedialog

import ply.lex as lex
import ply.yacc as yacc
import customtkinter as ctk

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
    sintaxerror.insert("0.0",'Programa sintacticamente correcto')


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
        sintaxerror.insert("0.0","Error de sintaxis en la entrada :" + token_str)
    else:
        print("Error de sintaxis en la entrada:", p, "Token no reconocido")
        sintaxerror.insert("0.0",'Error sintaxis por token no reconocido')


# Constructor del lexer
lexer = lex.lex()

# Constructor del Parser
parser = yacc.yacc()


# Función que se ejecuta cuando se presiona el boton Scanner
def botonscanner():  # scanner
    # programa ejemplo
    tablatokens.delete("1.0", "end")
    textoprocesado = "Token Type\tToken Value\n"
    progejemplo = cuadrodetexto.get("1.0", "end-1c")
    print(progejemplo)
    lexer.input(progejemplo)  # mandamos lo que esta en el cuadro de texto para el lexer
    for token in lexer:  # por cada token que encuentre en el programa ejemplo
        token_type = token.type
        token_value = token.value
        formatted_token = f"{token_type}\t{token_value}\n"
        textoprocesado += formatted_token
    # imprime a la izquierda lo que encontro
    print(textoprocesado)
    tablatokens.insert('1.0', textoprocesado)


# Función que se ejecuta cuando se presiona el boton parser
def botonparser():
    sintaxerror.delete("1.0", "end")
    progejemplo = cuadrodetexto.get("1.0", "end-1c")
    parser.parse(progejemplo)


def botonrun():
    botonscanner()
    botonparser()


def botonopenfile():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                text_content = file.read()
                cuadrodetexto.delete(1.0, ctk.END)  # Clear existing content
                cuadrodetexto.insert(ctk.END, text_content)  # Insert file content
        except Exception as e:
            cuadrodetexto.delete(1.0, ctk.END)
            cuadrodetexto.insert(ctk.END, f"Error reading file: {str(e)}")


def botonsavefile():
    # Get the content from the textbox
    content = cuadrodetexto.get("1.0", "end-1c")

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if file_path:
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Saved as: {file_path}")


# DE AQUI PARA ABAJO ES GRAFICACION
# personalizacion
ctk.set_appearance_mode("dark")  # apariencia
ctk.set_default_color_theme("dark-blue")  # tema
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
color_verde = "#7FB800"
color_blanco = "#ECE5F0"
color_AZUL = "#799496"
color_dorado = "#C2A83E"
color_rojo = "#FE4A49"
# Crear una ventana
ventana = ctk.CTk()
ventana.title("COM PAILER")
# Get the screen width and height
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()
# Set the window dimensions to fill the screen
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
boton_open = ctk.CTkButton(ventana, fg_color=color_AZUL, text='open file', command=botonopenfile)
boton_open.grid(row=0, column=2, sticky='nsew')
boton_open.grid_propagate(False)
boton_save = ctk.CTkButton(ventana, fg_color=color_rojo, text='save file', command=botonsavefile)
boton_save.grid(row=0, column=3, sticky='nsew')
boton_save.grid_propagate(False)
boton_run = ctk.CTkButton(ventana, fg_color=color_verde, text='run program', command=botonrun)
boton_run.grid(row=0, column=4, sticky='nsew')
boton_run.grid_propagate(False)
boton_scanner = ctk.CTkButton(ventana, fg_color=color_dorado, text='scanner', command=botonscanner)
boton_scanner.grid(row=0, column=5, sticky='nsew')
boton_scanner.grid_propagate(False)
boton_parser = ctk.CTkButton(ventana, fg_color=color_AZUL, text='parser', command=botonparser)
boton_parser.grid(row=0, column=6, sticky='nsew')
boton_parser.grid_propagate(False)
relleno = ctk.CTkLabel(ventana, bg_color=color_morado, text='')
relleno.grid(row=0, column=7, sticky='nsew')
relleno.grid_propagate(False)
################################################################
extrainfo = ctk.CTkLabel(ventana, text="", bg_color=color_morado)
extrainfo.grid(row=5, columnspan=8, sticky='nsew')
extrainfo.grid_propagate(False)
derecha = ctk.CTkLabel(ventana, text="", bg_color=color_gris)
derecha.grid(row=1, column=0, rowspan=4, sticky='nsew')
derecha.grid_propagate(False)
izquierda = ctk.CTkLabel(ventana, text="", bg_color=color_gris)
izquierda.grid(row=1, column=7, rowspan=4, sticky='nsew')
izquierda.grid_propagate(False)
################################################################
nombredelprograma = ctk.CTkLabel(ventana, text="TABVIEW", bg_color=color_gris3)
nombredelprograma.grid(row=1, column=1, columnspan=4, sticky='nsew')
nombredelprograma.grid_propagate(False)
cuadrodetexto = ctk.CTkTextbox(ventana, fg_color=color_gris2, font=fuente)
cuadrodetexto.grid(row=2, column=1, columnspan=4, sticky='nsew')
cuadrodetexto.grid_propagate(False)
########################################################################
separacion = ctk.CTkLabel(ventana, text="SEPARACION", bg_color=color_gris3)
separacion.grid(row=3, column=1, columnspan=6, sticky='nsew')
################################################################
label8 = ctk.CTkLabel(ventana, text="FUNCION1", bg_color=color_gris3)
label8.grid(row=4, column=1, columnspan=3, sticky='nsew')
label9 = ctk.CTkLabel(ventana, text="FUNCION2", bg_color=color_verde)
label9.grid(row=4, column=4, columnspan=3, sticky='nsew')
################################################################
label10 = ctk.CTkLabel(ventana, text="TOKENLIST", bg_color=color_morado)
label10.grid(row=1, column=5, sticky='nsew')
tablatokens = ctk.CTkTextbox(ventana, bg_color=color_gris3, font=fuente)
tablatokens.grid(row=2, column=5, sticky='nsew')
tablatokens.grid_propagate(False)
label12 = ctk.CTkLabel(ventana, text="SINTAX", bg_color=color_rojo)
label12.grid(row=1, column=6, sticky='nsew')
sintaxerror = ctk.CTkTextbox(ventana, bg_color=color_gris2, font=fuente)
sintaxerror.grid(row=2, column=6, sticky='nsew')
sintaxerror.grid_propagate(False)
# Iniciar  la aplicación/inferfaz
ventana.mainloop()
