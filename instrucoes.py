# Mostrar registradores ao final do programa
def mostrar_registradores(cpu):
    linhas = []
    linhas.append("--- REGISTERS ---\n")
    for k, v in cpu.registers.items():
        linhas.append(f"{k} = {v}")
    linhas.append("\n--- FLAGS ---\n")
    for k, v in cpu.flags.items():
        linhas.append(f"{k} = {v}")
    resultado = "\n".join(linhas)
    return resultado

def atualiza_flags(cpu, a, b, resultado, operacao = "sub"):

    # ZF (Zero Flag): ativa se o resultado for zero
    if resultado == 0:
        cpu.flags["ZF"] = 1
    else:
        cpu.flags["ZF"] = 0

    # SF (Sign Flag): ativa se o resultado for negativo
    if resultado < 0:
        cpu.flags["SF"] = 1
    else:
        cpu.flags["SF"] = 0

    # CF (Carry Flag): em ADD, ativa se passou de 65535 (estouro); em SUB, se deu negativo no unsigned
    if operacao == "add":
        if resultado > 0xFFFF:
            cpu.flags["CF"] = 1
        else:
            cpu.flags["CF"] = 0
    elif operacao == "sub":
        if a < b:
            cpu.flags["CF"] = 1
        else:
            cpu.flags["CF"] = 0

    # OF (Overflow Flag): em ADD/SUB com números com sinal, ativa se o sinal ficou errado
    if operacao == "add":
        if (a >= 0 and b >= 0 and resultado < 0) or (a < 0 and b < 0 and resultado >= 0):
            cpu.flags["OF"] = 1
        else:
            cpu.flags["OF"] = 0
    elif operacao == "sub":
        if (a >= 0 and b < 0 and resultado < 0) or (a < 0 and b >= 0 and resultado >= 0):
            cpu.flags["OF"] = 1
        else:
            cpu.flags["OF"] = 0


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
        if dst in cpu.registers and dst not in("IP", "SP"):
            if src in cpu.registers and src not in ("IP", "SP"):
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
        if dst in cpu.registers and  dst not in ("IP", "SP"):
            a = cpu.registers[dst]
            if src in cpu.registers and src not in ("IP", "SP"):
                cpu.registers[dst] += cpu.registers[src]
                b = cpu.registers[src]

            elif src.isnumeric():
                cpu.registers[dst] += int(src)
                b = int(src)
            
            else:
                raise ValueError("Valor inválido")
            resultado = a + b
            atualiza_flags(cpu, a, b, resultado, operacao="add")
        else:
            raise SyntaxError("Registrador inválido") 

    # Instrução SUB
    elif instrucao == "SUB":
        if len(partes) != 3:
            raise SyntaxError(f"{instrucao} requer exatos dois argumentos!")
        if dst in cpu.registers and dst not in ("IP", "SP"):
            a = cpu.registers[dst]
            if src in cpu.registers and src not in ("IP", "SP"):
                cpu.registers[dst] -= cpu.registers[src]
                b = cpu.registers[src]
            elif src.isnumeric():
                cpu.registers[dst] -= int(src)
                b = int(src)
            else:
                raise ValueError("Valor inválido")
            resultado = a - b
            atualiza_flags(cpu, a ,b, resultado, operacao="sub")
        else:
            raise SyntaxError("Registrador inválido") 
        
    elif instrucao == "CMP":
        if len(partes) != 3:
            raise SyntaxError(f"{instrucao} requer exatos dois argumentos!")
        if dst in cpu.registers and dst not in("IP", "SP"):
            a = cpu.registers[dst]
            if src in cpu.registers and src not in ("IP", "SP"):
                b = cpu.registers[src]
            elif src.isnumeric():
                b = int(src)
            else:
                raise ValueError("Valor errado!")
            resultado = a-b
            atualiza_flags(cpu, a, b, resultado, operacao="sub")
        else:
            raise SyntaxError("Registrador Inválido!")
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