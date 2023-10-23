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
# SALTOS

# SECCIONES
secdata= "section.data" + "\n"

# TIPOS DE DECLARACIONES Y INSTRUCCIONES
entero = r'\b(\w+)\s+(\w+)\s*=\s*(-?\d+)\b'
cadena = r'\b(\w+)\s+(\w+)\s*=\s*\'([^\']*)\'|\"([^\"]*)\"'
imprimir = r'print\s*\(\s*([\w.+\-*/]+|\'[^\']*\'|"[^"]*"\s*)\)'
expresion = r'\b(\w+)\s+(\w+)\s*=\s*([\w.+\-*/]+)'
# GUARDAMOS LINEAS DE CODIGO
lineasdecodigo = []
# LA TAGLA DE SIMBOLOS
symbol_table = []
# un contador
contador = 1
# CODIGO FUENTE
programa = """
inicio prueba
print ('Suma de dos numeros')
int x=50
int y=100
int suma = x+y
fin
"""
# DIVIDIR EL CODIGO EN LINEAS
lines = programa.split('\n')
# ENSAMBLADOR ES EL STRING QUE GENERAMOS
ensamblador = ""
# POR EJEMPLO AQUI CONCATENAMOS LA LINEA DEL SECTION DATA
ensamblador += "section.data" + "\n"
# genera la section.data y se genera lineas de codigo
for line in lines:
    # se encontro una variable int
    if re.match(entero, line):
        match = re.match(entero, line)
        var_type = match.group(1)
        var_id = match.group(2)
        var_value = int(match.group(3))
        variable_dict = {"TYPE": var_type, "ID": var_id, "VALOR": var_value}
        ensamblador += f"{variable_dict['ID']} dw {variable_dict['VALOR']}   ;" + "\n"
        symbol_table.append(variable_dict)
        lineasdecodigo.append(("entero", line))
    # se encontro una expresion
    elif re.match(expresion, line):
        match = re.match(expresion, line)
        variable = match.group(2)
        ensamblador += variable + " dw " + " 0 " + "\n"
        lineasdecodigo.append(("expresion", line))
    # se encontro una cadena
    elif re.match(cadena, line):
        match = re.match(cadena, line)
        var_type = match.group(1)
        var_id = match.group(2)
        var_value = str(match.group(3))
        variable_dict = {"TYPE": var_type, "ID": var_id, "VALOR": var_value}
        symbol_table.append(variable_dict)
        lineasdecodigo.append(("cadena", line))
    # se encontro la instruccion imprimir
    elif re.match(imprimir, line):
        texto = "mensaje "
        ensamblador += add
        texto = "db "
        ensamblador += texto
        cont = str(contador)
        match = re.match(imprimir, line)
        cadena = match.group(1)
        ensamblador += cadena + ",0" + "\n"
        contador += 1
        lineasdecodigo.append(("imprimir", line))
# imprimimos cada linea encontrada
for pattern, match in lineasdecodigo:
    print(f"linea: {pattern}, Match: {match}")
# imprimimos la tabla de simbolos
for variable_dict in symbol_table:
    print(variable_dict)
# section.data
ensamblador += "\n"
ensamblador += "section.text" + "\n"
ensamblador += "global_main" + "\n"
ensamblador += "\n"
# el main
ensamblador += "_main:" + "\n"
# encontramos operadores y operandos
operator_pattern = re.compile(r'[+\-*/]')
operand_pattern = re.compile(r'\b(\w+|\d+)\b')
# creamos donde guardarlos
operadores_encontrados = []
operandos_encontrados = []
for line in lines:
    # solo para evitar errores
    if re.match(entero, line):
        print()
    # impresion
    elif re.match(imprimir, line):
        ensamblador += ";imprimir un mensaje" + "\n"
        ensamblador += "mov eax, 4; syscall: write" + "\n"
        ensamblador += "mov ebx, 1; descriptor de archivo(stdout)" + "\n"
        ensamblador += "mov ecx, message" + "\n"
        ensamblador += "mov edx, 19; longitud del mensaje" + "\n"
        ensamblador += "int 0x80" + "\n"
    # analisis y impresion de  expresiones
    elif re.match(expresion, line):
        ensamblador += ";resolver una expresion" + "\n"
        v1 = "ax"
        v2 = "bx"
        usar_v1 = True
        match = re.match(expresion, line)
        # nombre y expresion
        nombre = match.group(2)
        exp = match.group(3)
        # buscamos todas los operadores y operandos en la expresion
        operators = operator_pattern.findall(exp)
        operands = operand_pattern.findall(exp)
        # evita que se use ax y bx si ya no esta usado
        for operand in operands:
            if usar_v1:
                v = v1
            else:
                v = v2
            ensamblador += " mov " + " " + v + " " + operand + "\n"
            operandos_encontrados.append(operand)
        for operator in operators:
            if operator == "+":
                ensamblador += "add " + " " + v1 + " " + v2 + "\n"
                ensamblador += "mov " + nombre + " " + v1 + "\n"
            elif operator == "-":
                ensamblador += "sub"
            elif operator == "*":
                ensamblador += "mul"
            elif operator == "/":
                ensamblador += "div"
            operadores_encontrados.append(operator)

        # Imprimir los operadores y operandos encontrados
        print(exp)

print("Operadores encontrados:", operadores_encontrados)
print("Operandos encontrados:", operandos_encontrados)

print(ensamblador)
