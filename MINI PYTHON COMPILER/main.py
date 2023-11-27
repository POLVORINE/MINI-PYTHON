# Librerias
from tkinter import filedialog
import ply.lex as lex
import ply.yacc as yacc
import customtkinter as ctk
import re

correcto = True
# palabas reservadas
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

t_NUM = r'(\d*\.\d+)|(\d+\.\d*)|\d+'
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
    if correcto:
        semantico.delete("1.0", "end")
        mensaje = "Programa semanticamente correcto\n"
        semantico.insert("1.0", mensaje)
    else:
        mensaje = "Programa semanticamente incorrecto\n"
        mensaje += "errores encontrados en :\n "
        semantico.insert("1.0", mensaje)


def botonIntermedio():
    intermedio.delete("1.0", "end")
    # SECCIONES
    secdata = "section.data" + "\n"
    globalmain = "global main " + "\n"
    main = "main:" + "\n"
    # ENSAMBLADOR ES EL STRING QUE GENERAMOS
    # TIPOS DE DECLARACIONES Y INSTRUCCIONES
    # GUARDAMOS LINEAS DE CODIGO
    entero = r'\b(\w+)\s+(\w+)\s*=\s*(-?\d+)\b'
    cadena = r'\b(\w+)\s+(\w+)\s*=\s*\'([^\']*)\'|\"([^\"]*)\"'
    imprimir = r'print\s*\(\s*([\'"][^\'"]+[\'"])\s*\)'
    imprimirvariables = r'print\s*\(\s*([a-zA-Z_]\w*)\s*\)'
    expresion = r'\b(\w+)\s+(\w+)\s*=\s*([\w.+\-*/]+)'
    ensamblador = ""
    programa = codigofuente.get("1.0", "end-1c")
    # DIVIDIR EL CODIGO EN LINEAS
    lines = programa.split('\n')
    # POR EJEMPLO AQUI CONCATENAMOS LA LINEA DEL SECTION DATA
    ensamblador += secdata
    contador = 1
    # genera la section.data y se genera lineas de codigo
    for line in lines:
        # se encontro una DECLARACION  int
        if re.match(entero, line):
            match = re.match(entero, line)
            var_id = match.group(2)
            v1 = var_id
            var_value = int(match.group(3))
            v2 = var_value
            ensamblador += str(contador)
            dint = f" {v1} dw  {v2}\n"
            ensamblador += dint
            contador = contador + 1
        # se encontro una expresion
        elif re.match(expresion, line):
            match = re.match(expresion, line)
            variable = match.group(2)
            v1 = variable
            ensamblador += str(contador)
            dexpresion = f" {v1} dd 0;\n"
            ensamblador += dexpresion

        # se encontro una cadena
        elif re.match(cadena, line):
            match = re.match(cadena, line)
            var_value = str(match.group(3))
            v1 = contador
            v2 = var_value
            ensamblador += str(contador)
            deprint = f"text{v1} db {v2},0\n"
            ensamblador += deprint
            contador = contador + 1

        # se encontro la instruccion imprimir
        elif re.match(imprimir, line):
            match = re.match(imprimir, line)
            texto = match.group(1)
            v1 = contador
            v2 = texto
            ensamblador += str(contador)
            deprint = f"text{v1} db {v2},0\n"
            ensamblador += deprint
            contador = contador + 1

        elif re.match(imprimirvariables, line):
            print('')
    # encontramos operadores y operandos
    operadores = re.compile(r'[+\-*/]')
    operandos = re.compile(r'\b(\w+|\d+)\b')
    # creamos donde guardarlos
    operadores_encontrados = []
    operandos_encontrados = []
    ensamblador += "\n"
    ensamblador += globalmain
    ensamblador += "\n"
    ensamblador += main
    ensamblador += "\n"
    for line in lines:
        # solo para evitar errores
        if re.match(entero, line):
            print()
        # impresion
        elif re.match(imprimir, line):
            ensamblador += ";imprimir un mensaje" + "\n"
            v1 = 'mensajero'
            v2 = 'longitud'
            ensamblador += str(contador)
            contador = contador + 1
            linea = ' mov eax, 4' + "\n"
            ensamblador += linea
            ensamblador += str(contador)
            contador = contador + 1
            linea = ' mov ebx, 1' + "\n"
            ensamblador += str(contador)
            contador = contador + 1
            ensamblador += linea
            linea = f' movecx, {v1}' + "\n"
            ensamblador += str(contador)
            contador = contador + 1
            ensamblador += linea
            linea = f' movedx, {v2}' + "\n"
            ensamblador += str(contador)
            contador = contador + 1
            ensamblador += linea
            linea = ' int 0x80' + "\n"
            ensamblador += str(contador)
            contador = contador + 1
            ensamblador += linea
        # analisis y impresion de  expresiones
        elif re.match(expresion, line):
            ensamblador += ";analizar una expresion" + "\n"
            match = re.match(expresion, line)
            if match:
                expresion_completa = match.group(3)
                operadores_encontrados = operadores.findall(expresion_completa)
                operandos_encontrados = operandos.findall(expresion_completa)
            for op in operadores_encontrados:
                if op == '+':
                    t1 = operandos_encontrados[-1] + operandos_encontrados[-2]
                    v1 = 'ax'
                    v2 = operandos_encontrados.pop(-2)
                    mov = f" mov {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += mov
                    v1 = 'ax'
                    v2 = operandos_encontrados.pop(-1)
                    add = f" add {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += add
                    v1 = 't1'
                    v2 = 'ax'
                    mov = f" mov {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += mov
                    operandos_encontrados.append(t1)
                elif op == '-':
                    t1 = operandos_encontrados[-1] - operandos_encontrados[-2]
                    v1 = 'ax'
                    v2 = operandos_encontrados.pop(-2)
                    mov = f" mov {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += mov
                    v1 = 'ax'
                    v2 = operandos_encontrados.pop(-1)
                    sub = f" sub {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += sub
                    v1 = 't1'
                    v2 = 'ax'
                    mov = f" mov {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += mov
                    operandos_encontrados.append(t1)
                elif op == '*':
                    t1 = operandos_encontrados[-1] * operandos_encontrados[-2]
                    v1 = 'ax'
                    v2 = operandos_encontrados.pop(-2)
                    mov = f" mov {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += mov
                    v1 = 'ax'
                    v2 = operandos_encontrados.pop(-1)
                    mul = f" mul {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += mul
                    v1 = 't1'
                    v2 = 'ax'
                    mov = f" mov {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += mov
                    operandos_encontrados.append(t1)
                elif op == '/':
                    t1 = operandos_encontrados[-1] / operandos_encontrados[-2]
                    v1 = 'ax'
                    v2 = operandos_encontrados.pop(-2)
                    mov = f" mov {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += mov
                    v1 = 'ax'
                    v2 = operandos_encontrados.pop(-1)
                    div = f" div {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += div
                    v1 = 't1'
                    v2 = 'ax'
                    mov = f" mov {v1} {v2}\n"
                    ensamblador += str(contador)
                    contador = contador + 1
                    ensamblador += mov
                    operandos_encontrados.append(t1)

        elif re.match(imprimirvariables, line):
            ensamblador += ";imprimir una variable" + "\n"
            v1 = 'nombre expresion'
            v2 = 'valor final de la expresion'
            ensamblador += str(contador)
            contador = contador + 1
            linea = ' mov eax, 4' + "\n"
            ensamblador += linea
            ensamblador += str(contador)
            contador = contador + 1
            linea = ' mov ebx, 1' + "\n"
            ensamblador += str(contador)
            contador = contador + 1
            ensamblador += linea
            linea = f' movecx, {v1}' + "\n"
            ensamblador += str(contador)
            contador = contador + 1
            ensamblador += linea
            linea = f' movedx, {v2}' + "\n"
            ensamblador += str(contador)
            contador = contador + 1
            ensamblador += linea
            linea = ' int 0x80' + "\n"
            ensamblador += str(contador)
            contador = contador + 1
            ensamblador += linea

    print(ensamblador)
    intermedio.insert('1.0', ensamblador)


def botonrun():
    botonscanner()
    botonparser()
    botonIntermedio()


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
fuenteG = ("Helvetica", 32)
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
screen_width = 1280
screen_height = 720
# llenar la pantalla
ventana.geometry(f"{screen_width}x{screen_height}")
# Configurar la geometría DEL GRID principal
ventana.grid_rowconfigure(0, weight=1)
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_rowconfigure(2, weight=20)
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
boton_codinter = ctk.CTkButton(ventana, fg_color=color_gris, text='traducir a ensamblador', command=botonIntermedio)
boton_codinter.grid(row=0, column=6, sticky='nsew')
boton_codinter.grid_propagate(False)
################################################################
boton_semantico = ctk.CTkButton(ventana, fg_color=color_morado, text='errores semanticos', command=botonsemantico)
boton_semantico.grid(row=3, column=1, sticky='nsew')
boton_semantico.grid_propagate(False)
boton_parser = ctk.CTkButton(ventana, fg_color=color_rojo, text='errores sintacticos', command=botonparser)
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
