#flotante = r'\b(\w+)\s+(\w+)\s*=\s*([+-]?(\d+\.\d+|\.\d+|\d+\.)\d*([eE][+-]?\d+)?)\b'
# se encontro un flotante
    elif re.match(flotante, line):
        match = re.match(flotante, line)
        var_type = match.group(1)
        var_id = match.group(2)
        var_value = float(match.group(3))
        print(var_value, "aver")
        variable_dict = {"TYPE": var_type, "ID": var_id, "VALOR": var_value}
        symbol_table.append(variable_dict)
        lineasdecodigo.append(("flotante", line))