# Mostrar registradores ao final do programa
def mostrar_registradores(cpu):
    linhas = []
    for k, v in cpu.registers.items():
        linhas.append(f"{k} = {v}")
    resultado = "\n".join(linhas)
    return resultado

# Interpretação do código
def interpretar(cpu, linha):
    partes = linha.split() # Divide a instrução em um vetor
    instrucao = partes[0].upper() # Pega a instrução

    # Divide a instrução em dois argumentos pra manipulação posterior
    if instrucao not in ("PUSH", "POP", "INT"):
        dst, src = map(lambda x: x.strip(",").upper(), partes[1:])
        if dst=="SP" or src=="SP":
            raise ReferenceError("SP não pode ser manipulado")
    
    #Instrução MOV
    if instrucao == "MOV":
        if len(partes) != 3:
            raise SyntaxError(f"{instrucao} requer exatos dois argumentos!")
        if dst in cpu.registers:
            if src in cpu.registers:
                if dst not in ("IP", "SP") and src not in ("IP", "SP"):
                    cpu.registers[dst] = cpu.registers[src]
            elif src.isnumeric():
                cpu.registers[dst] = int(src)
            else:
                raise ValueError("Valor inválido")
        else:
            raise SyntaxError("Registrador inválido")  

    # Instrução ADD
    elif instrucao == "ADD":
        if len(partes) != 3:
            raise SyntaxError(f"{instrucao} requer exatos dois argumentos!")
        if dst in cpu.registers:
            if src in cpu.registers:
                if dst not in ("IP", "SP") and src not in ("IP", "SP"):
                    cpu.registers[dst] += cpu.registers[src]
            elif src.isnumeric():
                cpu.registers[dst] += int(src)
            else:
                raise ValueError("Valor inválido")
        else:
            raise SyntaxError("Registrador inválido") 

    # Instrução SUB
    elif instrucao == "SUB":
        if len(partes) != 3:
            raise SyntaxError(f"{instrucao} requer exatos dois argumentos!")
        if dst in cpu.registers:
            if src in cpu.registers:
                if dst not in ("IP", "SP") and src not in ("IP", "SP"):
                    cpu.registers[dst] -= cpu.registers[src]
            elif src.isnumeric():
                cpu.registers[dst] -= int(src)
            else:
                raise ValueError("Valor inválido")
        else:
            raise SyntaxError("Registrador inválido") 
            
    # Instrução INT
    elif instrucao == "INT":
        if len(partes) != 2:
            raise SyntaxError(f"{instrucao} requer um argumento!")
        codigo = partes[1]
        if codigo == "0":
            raise StopIteration("Execução finalizada com INT 0")
        else:
            raise SyntaxError(f"INT {codigo}: função não definida")
    
    # Instrução PUSH
    elif instrucao == "PUSH":
        reg = partes[1].upper()
        if reg in cpu.registers:
            cpu.registers['SP'] -= 2
            addr = cpu.registers['SP']
            valor = cpu.registers[reg]
            cpu.memory[addr] = valor & 0xFF
            cpu.memory[addr + 1] = (valor >> 8) & 0xFF

    # Instrução POP
    elif instrucao == "POP":
        reg = partes[1].upper()
        if reg in cpu.registers:
            addr = cpu.registers['SP']
            low = cpu.memory[addr]
            high = cpu.memory[addr + 1]
            cpu.registers[reg] = (high << 8) | low
            cpu.registers['SP'] += 2
    
    # Instrução inválida
    else:
        raise SyntaxError("Erro de sintaxe")