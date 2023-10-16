import re


def analyze_expression(expression):
    # Find operators and operands within the expression
    operators_and_operands = re.findall(r'[\w.+\-*/]+', expression)

    # Create a dictionary to store the analysis results
    analysis_result = {
        "Expression": expression,
        "Operators": [],
        "Operands": []
    }

    # Classify each item as an operator or operand
    for item in operators_and_operands:
        if re.match(r'[\+\-\*/]', item):
            analysis_result["Operators"].append(item)
        else:
            analysis_result["Operands"].append(item)

    return analysis_result


# Test the function with an example expression
expression = "x + y * 5 - z"
result = analyze_expression(expression)

print("Expression:", result["Expression"])
print("Operators:", result["Operators"])
print("Operands:", result["Operands"])
