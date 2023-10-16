import re

# Pattern to match expressions like "int suma = x+y+5"
declaracion = r'\b(\w+)\s+(\w+)\s*=\s*([\w.+\-*/]+)'

# Initialize an empty list to store expression information dictionaries
expression_info_list = []

# Sample lines containing expressions
lines = ["int suma = x+y+5", "float result = a*b-c/d"]

for line in lines:
    match = re.match(declaracion, line)
    if match:
        # Extract the components
        var_type = match.group(1)
        var_id = match.group(2)
        expression = match.group(3)

        # Create a dictionary to store operator and operand information
        expression_dict = {"TYPE": var_type, "ID": var_id, "EXPRESSION": expression}

        # Find operators and operands within the expression
        operators_and_operands = re.findall(r'[\w.+\-*/]+', expression)

        # Add operators and operands to the dictionary
        expression_dict["OPERATORS_AND_OPERANDS"] = operators_and_operands

        # Append the dictionary to the list
        expression_info_list.append(expression_dict)

# Print each operand and operator in order for each expression
for expression_dict in expression_info_list:
    print("Variable Type:", expression_dict["TYPE"])
    print("Variable ID:", expression_dict["ID"])
    print("Expression:", expression_dict["EXPRESSION"])

    # Print each operand and operator on separate lines
    for item in re.findall(r'[\w.+\-*/]+', expression_dict["EXPRESSION"]):
        print(item)

    print()
