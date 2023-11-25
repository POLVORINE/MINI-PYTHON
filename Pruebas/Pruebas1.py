import re

expresion = r'\b(\w+)\s+(\w+)\s*=\s*([\w.+\-*/]+)'
operadores = re.compile(r'[+\-*/]')
operandos = re.compile(r'\b(\w+|\d+)\b')

expresion_texto = "5+5"
match = re.search(expresion, expresion_texto)

if match:
    nombre_variable = match.group(1)
    expresion_completa = match.group(3)

    # Encuentra operadores en la expresión completa
    operadores_encontrados = operadores.findall(expresion_completa)

    # Encuentra operandos en la expresión completa
    operandos_encontrados = operandos.findall(expresion_completa)

    print(f"Nombre de la variable: {nombre_variable}")
    print(f"Operadores encontrados: {operadores_encontrados}")
    print(f"Operandos encontrados: {operandos_encontrados}")
else:
    print("No se encontró una expresión válida.")
