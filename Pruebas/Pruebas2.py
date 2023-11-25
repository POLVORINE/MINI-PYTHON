import re
# PLANTILLAS
v1 = 1
v2 = 2
# MOVER
mov = f"mov {v1} {v2}\n"
# OPERACIONES ARITMETICAS
add = f"add {v1} {v2}\n"
sub = f"sub {v1} {v2}\n"
mul = f"mul {v1} {v2}\n"
div = f"div {v1} {v2}\n"
# GUARDAR
sto = f"sto {v1} {v2}\n"
# declaraciones
dint = f"{v1} dw  {v2}\n"
dfloat = f"{v1} dd  {v2}\n"
dstring = f"{v1} dw  {v2}\n"
dexpresion = f"{v1} dd 0;\n"
deprint = f"text {v1} db {v2},0\n"
# SECCIONES
secdata = "section.data" + "\n"
sectext = "section.main" + "\n"
globalmain = "global main " + "\n"
main = "main:" + "\n"
# ENSAMBLADOR ES EL STRING QUE GENERAMOS
ensamblador = ""
# TIPOS DE DECLARACIONES Y INSTRUCCIONES
entero = r'\b(\w+)\s+(\w+)\s*=\s*(-?\d+)\b'
cadena = r'\b(\w+)\s+(\w+)\s*=\s*\'([^\']*)\'|\"([^\"]*)\"'
imprimir = r'print\s*\(\s*([\'"][^\'"]+[\'"])\s*\)'
imprimirvariables = r'print\s*\(\s*([a-zA-Z_]\w*)\s*\)'
expresion = r'\b(\w+)\s+(\w+)\s*=\s*([\w.+\-*/]+)'
# GUARDAMOS LINEAS DE CODIGO
lineasdecodigo = []
# LA TAGLA DE SIMBOLOS
symbol_table = []
# contador
contador = 1
# CODIGO FUENTE
programa = """
inicio prueba
int x=50
int y=100
int suma = x+y+5
print ('Suma de dos numeros')
print (suma)
fin
"""
# DIVIDIR EL CODIGO EN LINEAS
lines = programa.split('\n')
# POR EJEMPLO AQUI CONCATENAMOS LA LINEA DEL SECTION DATA
ensamblador += secdata
# genera la section.data y se genera lineas de codigo
for line in lines:
    # se encontro una variable int
    if re.match(entero, line):
        match = re.match(entero, line)
        var_type = match.group(1)
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
ensamblador += globalmain
ensamblador += main
for line in lines:
    # solo para evitar errores
    if re.match(entero, line):
        print()
    # impresion
    elif re.match(imprimir, line):
        ensamblador += ";imprimir un mensaje" + "\n"
    # analisis y impresion de  expresiones
    elif re.match(expresion, line):
        ensamblador += ";analizar una expresion" + "\n"
        match = re.match(expresion, line)
        if match:
            nombre_variable = match.group(1)
            expresion_completa = match.group(3)
            operadores_encontrados = operadores.findall(expresion_completa)
            operandos_encontrados = operandos.findall(expresion_completa)
            print(f"Operadores encontrados: {operadores_encontrados}")
            print(f"Operandos encontrados: {operandos_encontrados}")
        for op in operadores_encontrados:
            if op == '+':
                t1 = operandos_encontrados[-1] + operandos_encontrados[-2]
                v1 = 'ax'
                v2 = operandos_encontrados.pop(-2)
                mov = f"mov {v1} {v2}\n"
                ensamblador += mov
                v1 = 'ax'
                v2 = operandos_encontrados.pop(-1)
                add = f"add {v1} {v2}\n"
                ensamblador += add
                v1 = 't1'
                v2 = 'ax'
                mov = f"mov {v1} {v2}\n"
                ensamblador += mov
                operandos_encontrados.append(t1)
            elif op == '-':
                t1 = operandos_encontrados[-1] - operandos_encontrados[-2]
                v1 = 'ax'
                v2 = operandos_encontrados.pop(-2)
                mov = f"mov {v1} {v2}\n"
                ensamblador += mov
                v1 = 'ax'
                v2 = operandos_encontrados.pop(-1)
                sub = f"sub {v1} {v2}\n"
                ensamblador += sub
                v1 = 't1'
                v2 = 'ax'
                mov = f"mov {v1} {v2}\n"
                ensamblador += mov
                operandos_encontrados.append(t1)
            elif op == '*':
                t1 = operandos_encontrados[-1] * operandos_encontrados[-2]
                v1 = 'ax'
                v2 = operandos_encontrados.pop(-2)
                mov = f"mov {v1} {v2}\n"
                ensamblador += mov
                v1 = 'ax'
                v2 = operandos_encontrados.pop(-1)
                mul = f"mul {v1} {v2}\n"
                ensamblador += mul
                v1 = 't1'
                v2 = 'ax'
                mov = f"mov {v1} {v2}\n"
                ensamblador += mov
                operandos_encontrados.append(t1)
            elif op == '/':
                t1 = operandos_encontrados[-1] / operandos_encontrados[-2]
                v1 = 'ax'
                v2 = operandos_encontrados.pop(-2)
                mov = f"mov {v1} {v2}\n"
                ensamblador += mov
                v1 = 'ax'
                v2 = operandos_encontrados.pop(-1)
                div = f"div {v1} {v2}\n"
                ensamblador += div
                v1 = 't1'
                v2 = 'ax'
                mov = f"mov {v1} {v2}\n"
                ensamblador += mov
                operandos_encontrados.append(t1)

    elif re.match(imprimirvariables, line):
        ensamblador += ";imprimir una variable" + "\n"

print(ensamblador)
