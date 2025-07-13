# Import
from instrucoes import interpretar

# CPU em si
class CPU:
    def __init__(self):
        # Registradores
        self.registers = {
            'AX': 0,
            'BX': 0,
            'CX': 0,
            'DX': 0,
            'SP': 0xFFFE,
            'IP': 0,
        }

        self.flags = {
            'ZF': 0,
            'CF': 0,
            'SF': 0,
            'OF': 0,
        }

        
        self.memory = [0] * 65536
        self.flags = dict.fromkeys(self.flags, 0)
        self.programa = []

    def reset(self):
        for i in self.registers:
            self.registers[i] = 0
        self.registers['SP'] = 0xFFFE
        self.memory = [0] * 65536
        self.programa = []

    def carregar_programa(self, texto):
        self.programa = []
        for linha in texto.splitlines():
            linha_limpa = linha.strip()
            if linha_limpa:
                self.programa.append(linha_limpa)

    def executar(self):
        while self.registers['IP'] < len(self.programa):
            instrucao = self.programa[self.registers['IP']]
            interpretar(self, instrucao)
              