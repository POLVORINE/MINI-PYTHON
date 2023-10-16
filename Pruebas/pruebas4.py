import re

# Pattern to match integer declarations like "int x = 50"
entero = r'\b(\w+)\s+(\w+)\s*=\s*(-?\d+)'

# Pattern to match expressions like "float result = 3.14"
expresion = r'\b(\w+)\s+(\w+)\s*=\s*([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)'

# Initialize lists to store matching results
integer_matches = []
expression_matches = []

# Sample lines containing variable declarations
lines = ["int x = 50", "float result = 3.14", "int y = -123", "float pi = 3.14159"]

for line in lines:
    if re.match(entero, line):
        integer_matches.append(("entero", line))
    elif re.match(expresion, line):
        expression_matches.append(("expresion", line))

# Print matches for integers
print("Integer Matches:")
for match_type, line in integer_matches:
    print(match_type, "-", line)

# Print matches for expressions
print("\nExpression Matches:")
for match_type, line in expression_matches:
    print(match_type, "-", line)
