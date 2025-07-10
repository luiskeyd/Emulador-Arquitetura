class CPU:
  def __init__(self):
    # registradores de 16 bits
    self.registers = {
      'AX': 0,
      'BX': 0,
      'CX': 0,
      'DX': 0,
      'SP': 0XFFFE,
      'IP': 0,
      'CS': 0,
    }

    self.flags = {
      'ZF': 0,
      'CF': 0,
      'SF': 0,
      'OF': 0,
    }

    # memória 64kb
    self.memory = [0] * 65536

    # programa carregado (linhas)
    self.program =  []

  def reset(self):
    for r in self.registers:
      self.registers[r] = 0
    self.registers['SP'] = 0xFFFE
    self.program = []
    self.flags = dict.fromkeys(self.flags, 0)
    self.memory = [0] * 65536

  def carregar_programa(self, texto):
    self.programa = []
    for linha in texto.splitlines():
      linha_limpa = linha.strip()
      if linha_limpa:
        self.programa.append(linha_limpa)

  def executar(self):
    while self.registers['IP'] < len(self.program):
      instrucao = self.program[self.regs['IP']]
      self.executar_instrucao(instrucao)
      self.registers['IP'] += 1

  def executor_instrucoes(self, linha):
    from instrucoes import interpretar
    interpretar(self, linha)