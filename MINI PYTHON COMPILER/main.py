# Librerias
from tkinter import filedialog

import customtkinter as ctk
import ply.lex as lex
import ply.yacc as yacc
import re

# palabas reservadas
reserved = {
    'inicio': 'INICIO',
    'fin': 'FIN',
    'if': 'IF',
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
    erroresSintacticos.insert("0.0", 'Programa sintacticamente correcto')


def p_ListaInstrucciones(p):
    """
    ListaInstrucciones  : INSTRUCCION
                        | ListaInstrucciones INSTRUCCION
    """


def p_INSTRUCCION(p):
    """
    INSTRUCCION : ASIGNACION
                | IFINSTR
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
    OPERACION :  ID OPARIT ID
              | ID OPARIT   NUM
              | NUM OPARIT   NUM
              | NUM OPARIT   ID


    """


def p_IFINSTR(p):
    """
    IFINSTR : IF  CONDICION  INICIO ListaInstrucciones FIN
    """


def p_CONDICION(p):
    """
    CONDICION :  APERTUPAR EXPRESION OPRELAC EXPRESION CIERREPAR
    """


def p_PRINTINSTR(p):
    """
    PRINTINSTR  : PRINT APERTUPAR CADENA CIERREPAR
                | PRINT APERTUPAR EXPRESION   CIERREPAR
    """


def p_error(p):
    token_str = str(p.value)
    if p is not None:
        erroresSintacticos.insert("0.0", "Error de sintaxis en la entrada :" + token_str)
    else:
        erroresSintacticos.insert("0.0", 'Error sintaxis por token no reconocido' + token_str)


# Constructor del lexer
lexer = lex.lex()

# Constructor del Parser
parser = yacc.yacc()



def botonNuevoArchivo():
    codigoFuente.delete(1.0, ctk.END)


def botonAbrirArchivo():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                text_content = file.read()
                codigoFuente.delete(1.0, ctk.END)  # Clear existing content
                codigoFuente.insert(ctk.END, text_content)  # Insert file content
        except Exception as e:
            codigoFuente.delete(1.0, ctk.END)
            codigoFuente.insert(ctk.END, f"Error reading file: {str(e)}")


def botonSalvarArchivo():
    # Get the content from the textbox
    content = codigoFuente.get("1.0", "end-1c")

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if file_path:
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Saved as: {file_path}")


def botonscanner():  # scanner
    # programa ejemplo
    tablaTokens.delete("1.0", "end")
    textoprocesado = "Token Type\tToken Value\n"
    progejemplo = codigoFuente.get("1.0", "end-1c")
    lexer.input(progejemplo)  # mandamos lo que esta en el cuadro de texto para el lexer
    for token in lexer:  # por cada token que encuentre en el programa ejemplo
        token_type = token.type
        token_value = token.value
        formatted_token = f"{token_type}\t{token_value}\n"
        textoprocesado += formatted_token
    # imprime a la izquierda lo que encontro
    tablaTokens.insert('1.0', textoprocesado)


def botonparser():
    erroresSintacticos.delete("1.0", "end")
    progejemplo = codigoFuente.get("1.0", "end-1c")
    parser.parse(progejemplo)


def botonsemantico():
    error = " "
    correcto = True
    erroresSemanticos.delete("1.0", "end-1c")
    entero = r'\b(\w+)\s+(\w+)\s*=\s*(-?\d+)\b'
    cadena = r'\b(\w+)\s+(\w+)\s*=\s*\'([^\']*)\'|\"([^\"]*)\"'
    # verifica que las variables declaradas como enteras lo sean y las variables declaradas como string lo sean
    programa = codigoFuente.get("1.0", "end-1c")
    # DIVIDIR EL CODIGO EN LINEAS
    lines = programa.split('\n')
    for line in lines:
        # se encontro una DECLARACION  int
        if re.match(entero, line):
            match = re.match(entero, line)
            var_id = match.group(2)
            v1 = var_id
            var_value = int(match.group(3))
            v2 = var_value
            if isinstance(v2, int):
                print(" ")
                correcto = True
            else:
                correcto = False
                error="La variable"+v1
                error += " no es un entero\n"
        elif re.match(cadena, line):
            match = re.match(cadena, line)
            var_value = str(match.group(3))
            v2 = var_value
            if isinstance(v2, str):
                print(" ")
                correcto = True
            else:
                correcto = False
                error="La variable"+v2
                error += " no es un string\n"

    if correcto:
        erroresSemanticos.delete("1.0", "end")
        mensaje = "Programa semanticamente correcto\n"
        erroresSemanticos.insert("1.0", mensaje)
    else:
        mensaje = "Programa semanticamente incorrecto\n"
        mensaje += "errores encontrados en :\n "
        erroresSemanticos.insert("1.0", error)


def botonIntermedio():
    codigoIntermedio.delete("1.0", "end")
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
    programa = codigoFuente.get("1.0", "end-1c")
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
    codigoIntermedio.insert('1.0', ensamblador)


def botonCodigoObjeto():
    codigoObjeto.delete("1.0", "end")
    Ensamblador = codigoIntermedio.get("1.0", "end-1c")
    codigo = " "

    registrosTraduccion = {
        'eax': '000', 'ebx': '001', 'ecx': '010', 'edx': '011',
        'esi': '110', 'edi': '111', 'ax': '000', 'bx': '001',
        'cx': '010', 'dx': '011', 'si': '110', 'di': '111',
        'al': '000', 'bl': '001', 'cl': '010', 'dl': '011',
    }
    # MOV registro valor immediato
    # como se compone un mov
    mov_regex = re.compile(r'^\s*mov\s+([a-zA-Z0-9]+)\s*,\s*(\d+)\s*$')
    # ANALIZA EL MOV
    match = mov_regex.match(Ensamblador)
    if match:
        registroDestino = match.group(1).lower()
        valorInmediato = int(match.group(2))

        # chekea si existe el registro
        if registroDestino in registrosTraduccion:
            # Convertir valor inmmediato a binario
            immediate_binary = bin(valorInmediato & 0xFFFF)[2:].zfill(16)

            # acomodar para la printeada
            opcode = '1011'  # MOV opcode
            reg_binary = registrosTraduccion[registroDestino]
            binary_representation = f'{opcode}{reg_binary}{immediate_binary}'
            codigo += binary_representation + "\n"
            codigoObjeto.insert('1.0', codigo)


def botonCorrerPrograma():
    botonscanner()
    botonparser()
    botonIntermedio()
    botonCodigoObjeto()


# DE AQUI PARA ABAJO ES GRAFICACION
#   personalizacion
#       TAMAÑO Y TIPO DE FUENTE DE LA APLICACION
fuente = ("Helvetica", 16)
fuentetexto = ("Helvetica", 16)
nomcomp = "COMPILER"
nomgramatica = "MINI PYTHON"
#       COLORES DE LA INTERFAZ
colorTitulo = "#4d3f62"
colorBotones = "#40434f"
colorFondoTexto = "#282a36"
color_Contraste = "#3a3d4c"
colorEncabezados = "#4B8F8C"
# Crear una ventana
ventana = ctk.CTk()
ventana.title(nomcomp)
# tamaño de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()
# llenar la pantalla
ventana.geometry(f"{screen_width}x{screen_height}")
# Configurar la geometría DEL GRID
ventana.grid_rowconfigure(0, weight=1)
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_rowconfigure(2, weight=2)
ventana.grid_rowconfigure(3, weight=1)
ventana.grid_rowconfigure(4, weight=1)
ventana.grid_rowconfigure(5, weight=1)
ventana.grid_rowconfigure(6, weight=1)
ventana.grid_rowconfigure(7, weight=1)
################################################################
ventana.grid_columnconfigure(0, weight=3)
ventana.grid_columnconfigure(1, weight=10)
ventana.grid_columnconfigure(2, weight=10)
ventana.grid_columnconfigure(3, weight=3)
ventana.grid_columnconfigure(4, weight=10)
ventana.grid_columnconfigure(5, weight=10)
ventana.grid_columnconfigure(6, weight=3)
ventana.grid_columnconfigure(7, weight=10)
ventana.grid_columnconfigure(8, weight=10)
ventana.grid_columnconfigure(9, weight=3)
# OBJETOS DE LA INTERFAZ
# ROW 0
titulo = ctk.CTkLabel(ventana, text=nomcomp, bg_color=colorTitulo, font=fuente)
titulo.grid(row=0, columnspan=2, sticky='nsew')
titulo.grid_propagate(False)
botonNuevo = ctk.CTkButton(ventana, fg_color=colorBotones, text='Nuevo archivo', font=fuente, command=botonNuevoArchivo)
botonNuevo.grid(row=0, column=2, sticky='nsew')
botonNuevo.grid_propagate(False)
espacio1 = ctk.CTkLabel(ventana, text=" ", bg_color=colorTitulo)
espacio1.grid(row=0, column=3, sticky='nsew')
espacio1.grid_propagate(False)
botonAbrir = ctk.CTkButton(ventana, fg_color=colorBotones, text='Abrir archivo', border_color="black", font=fuente,
                           command=botonAbrirArchivo)
botonAbrir.grid(row=0, column=4, sticky='nsew')
botonAbrir.grid_propagate(False)
botonSalvar = ctk.CTkButton(ventana, fg_color=color_Contraste, text='Salvar archivo', font=fuente,
                            command=botonSalvarArchivo)
botonSalvar.grid(row=0, column=5, sticky='nsew')
botonSalvar.grid_propagate(False)
espacio2 = ctk.CTkLabel(ventana, text=" ", bg_color=colorTitulo)
espacio2.grid(row=0, column=6, sticky='nsew')
espacio2.grid_propagate(False)
botonCorrer = ctk.CTkButton(ventana, fg_color=color_Contraste, text='Correr programa', font=fuente,
                            command=botonCorrerPrograma)
botonCorrer.grid(row=0, column=7, columnspan=2, sticky='nsew')
botonCorrer.grid_propagate(False)
espacio3 = ctk.CTkLabel(ventana, text=" ", bg_color=colorTitulo)
espacio3.grid(row=0, column=9, sticky='nsew')
espacio3.grid_propagate(False)
# ROW 1
LabelCF = ctk.CTkLabel(ventana, text="Codigo Fuente ", bg_color=colorEncabezados, font=fuente)
LabelCF.grid(row=1, column=1, columnspan=2, sticky='nsew')
LabelCF.grid_propagate(False)
LabelCI = ctk.CTkLabel(ventana, text="Codigo Intermedio ", bg_color=colorEncabezados, font=fuente)
LabelCI.grid(row=1, column=4, sticky='nsew')
LabelCI.grid_propagate(False)
botonCI = ctk.CTkButton(ventana, fg_color=colorBotones, text=' Generar ', font=fuente, command=botonIntermedio)
botonCI.grid(row=1, column=5, sticky='nsew')
botonCI.grid_propagate(False)
LabelCO = ctk.CTkLabel(ventana, text="Codigo Objeto ", bg_color=colorEncabezados, font=fuente)
LabelCO.grid(row=1, column=7, sticky='nsew')
LabelCO.grid_propagate(False)
botonCO = ctk.CTkButton(ventana, fg_color=colorBotones, text=' Generar ', font=fuente, command=botonCodigoObjeto)
botonCO.grid(row=1, column=8, sticky='nsew')
botonCO.grid_propagate(False)
# ROW 2
codigoFuente = ctk.CTkTextbox(ventana, fg_color=colorFondoTexto, font=fuentetexto)
codigoFuente.grid(row=2, column=1, columnspan=2, sticky='nsew', rowspan=3)
codigoFuente.grid_propagate(True)
codigoIntermedio = ctk.CTkTextbox(ventana, fg_color=colorFondoTexto, font=fuentetexto)
codigoIntermedio.grid(row=2, column=4, columnspan=2, sticky='nsew', rowspan=3)
codigoIntermedio.grid_propagate(True)
codigoObjeto = ctk.CTkTextbox(ventana, fg_color=colorFondoTexto, font=fuentetexto)
codigoObjeto.grid(row=2, column=7, columnspan=2, sticky='nsew', rowspan=3)
codigoObjeto.grid_propagate(True)
# ROW 3
LabelTT = ctk.CTkLabel(ventana, text="Tabla De Tokens ", bg_color=colorEncabezados, font=fuente)
LabelTT.grid(row=6, column=1, sticky='nsew')
LabelTT.grid_propagate(False)
botonTT = ctk.CTkButton(ventana, fg_color=colorBotones, text=' Generar ', font=fuente)
botonTT.grid(row=6, column=2, sticky='nsew')
botonTT.grid_propagate(False)
LabelESEM = ctk.CTkLabel(ventana, text="Errores semanticos ", bg_color=colorEncabezados, font=fuente)
LabelESEM.grid(row=6, column=4, sticky='nsew')
LabelESEM.grid_propagate(False)
botonESEM = ctk.CTkButton(ventana, fg_color=colorBotones, text=' Mostrat ', font=fuente)
botonESEM.grid(row=6, column=5, sticky='nsew')
botonESEM.grid_propagate(False)
LabelESIN = ctk.CTkLabel(ventana, text="Errores Sintacticos ", bg_color=colorEncabezados, font=fuente)
LabelESIN.grid(row=6, column=7, sticky='nsew')
LabelESIN.grid_propagate(False)
botonESIN = ctk.CTkButton(ventana, fg_color=colorBotones, text=' Mostrar ', font=fuente)
botonESIN.grid(row=6, column=8, sticky='nsew')
botonESIN.grid_propagate(False)
# ROW 4
tablaTokens = ctk.CTkTextbox(ventana, fg_color=colorFondoTexto, font=fuentetexto)
tablaTokens.grid(row=7, column=1, columnspan=2, rowspan=1, sticky='nsew')
tablaTokens.grid_propagate(False)
erroresSemanticos = ctk.CTkTextbox(ventana, fg_color=colorFondoTexto, font=fuentetexto)
erroresSemanticos.grid(row=7, column=4, columnspan=2, rowspan=1, sticky='nsew')
erroresSemanticos.grid_propagate(False)
erroresSintacticos = ctk.CTkTextbox(ventana, fg_color=colorFondoTexto, font=fuentetexto)
erroresSintacticos.grid(row=7, column=7, columnspan=2, rowspan=1, sticky='nsew')
erroresSintacticos.grid_propagate(False)
# row 7
extraInfo = ctk.CTkLabel(ventana, text=" ", bg_color=colorTitulo, font=fuente)
extraInfo.grid(row=8, columnspan=10, sticky='nsew')
extraInfo.grid_propagate(False)
# Iniciar  la aplicación/inferfaz
ventana.mainloop()
