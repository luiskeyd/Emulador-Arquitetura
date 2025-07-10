
def interpretar(cpu, linha):
  partes = linha.split()
  if not partes:
    return
  
  instrucao = partes[0].upper()

  if instrucao == "MOV":
    dst, src = map(lambda x: x.strip(',').upper(), partes[1:])
    if src in cpu.registers:
      cpu.registers[dst] = cpu.registers[src]
    elif src.isdigit():
      cpu.registers[dst] = int(src)
  
  elif instrucao == "ADD":
    dst, src = map(lambda x: x.strip(",").upper(), partes[1:])
    if src in cpu.registers:
      cpu.registers[dst] += cpu.registers[src]
    elif src.isdigit():
      cpu.registers[dst] += int(src)

  elif instrucao == "SUB":
    dst, src = map(lambda x: x.strip(",").upper(), partes[1:])
    if src in cpu.registers:
      cpu.registers[dst] -= int(src)
    elif src.isdigit():
      cpu.registers[dst] -= int(src)

  elif instrucao == "INT":
    codigo = partes[1]
    if codigo == "0":
      raise StopIteration("Execução finalizada com INT 0")
  
def atualizar_flags(cpu, resultado):
  cpu.flags['ZF'] = int(resultado == 0)
  cpu.flags['SF'] = int(resultado < 0)