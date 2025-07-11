
def interpretar(cpu, linha):
    partes = linha.split()
    if not partes:
        return

    instrucao = partes[0].upper()
        
    if instrucao == "MOV":
        if len(partes) != 3:
            raise SyntaxError(f"{instrucao} requer exatos dois argumentos!")
        dst, src = map(lambda x: x.strip(',').upper(), partes[1:])
        if dst in cpu.registers:
          if src in cpu.registers:
            if dst not in ("IP", "SP") and src not in ("IP", "SP"):
                cpu.registers[dst] = cpu.registers[src]
            else:
                raise SyntaxError("Registrador inválido")
          elif src.isdigit():
            cpu.registers[dst] = int(src)
        else:
            raise SyntaxError("registrador nao existe, animal")

    elif instrucao == "ADD":
        if len(partes) != 3:
            raise SyntaxError(f"{instrucao} requer exatos dois argumentos!")
        dst, src = map(lambda x: x.strip(",").upper(), partes[1:])
        if dst in cpu.registers:
            if src in cpu.registers:
                if dst not in ("IP", "SP") and src not in ("IP", "SP"):
                    cpu.registers[dst] += cpu.registers[src]
                else:
                    raise SyntaxError("Registrador inválido")
            elif src.isdigit():
                cpu.registers[dst] += int(src)
        else:
            raise SyntaxError

    elif instrucao == "SUB":
        if len(partes) != 3:
            raise SyntaxError(f"{instrucao} requer exatos dois argumentos!")
        dst, src = map(lambda x: x.strip(",").upper(), partes[1:])
        if dst in cpu.registers:
            if src in cpu.registers:
                if dst not in ("IP", "SP") and src not in ("IP", "SP"):
                    cpu.registers[dst] -= cpu.registers[src]
                else:
                    raise SyntaxError("Registrador inválido")
            elif src.isdigit():
                cpu.registers[dst] -= int(src)
        else:
            raise SyntaxError
            

    elif instrucao == "INT":
        if len(partes) != 2:
            raise SyntaxError(f"{instrucao} requer um argumento!")
        codigo = partes[1]
        if codigo == "0":
            raise StopIteration("Execução finalizada com INT 0")
        else:
            raise StopIteration(f"INT {codigo}: função não definida")
    
    else:
        raise SyntaxError("CASA DO CARALHO")
