import re
def mov_to_binary(assembly_instruction):
    # Define a mapping of register names to their binary representation
    register_mapping = {'eax': '000', 'ebx': '001', 'ecx': '010', 'edx': '011', 'esi': '110', 'edi': '111'}

    # Regular expression to match the MOV instruction with immediate data
    mov_regex = re.compile(r'^\s*mov\s+([a-zA-Z0-9]+)\s*,\s*(\d+)\s*$')

    # Check if the instruction matches the MOV pattern
    match = mov_regex.match(assembly_instruction)
    if match:
        destination_register = match.group(1).lower()
        immediate_value = int(match.group(2))

        # Ensure the destination register is in the mapping
        if destination_register in register_mapping:
            # Convert immediate value to 16-bit binary representation
            immediate_binary = bin(immediate_value & 0xFFFF)[2:].zfill(16)

            # Construct the binary representation
            opcode = '1011'  # MOV opcode
            reg_binary = register_mapping[destination_register]
            binary_representation = f'{opcode}{reg_binary}{immediate_binary}'

            return binary_representation
        else:
            print(f"Error: Unknown destination register {destination_register}")
    else:
        print("Error: Not a valid MOV instruction")

# Example usage:
assembly_instruction = 'mov eax, 255'
binary_representation = mov_to_binary(assembly_instruction)
print(f"Binary representation: {binary_representation}")

# Similar usage can be done for SUB, MUL, and DIV instructions
