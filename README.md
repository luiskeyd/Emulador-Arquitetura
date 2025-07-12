# Emulador Assembly 8086

Este projeto é um emulador da arquitetura Intel 8086 de 16 bits, com interface gráfica em Python usando a biblioteca customtkinter. Permite executar e depurar programas em uma linguagem Assembly simplificada, com visualização dos registradores.

## Funcionalidades

* Interface gráfica com entrada de código, botões de controle e área de saída
* Modo Debug com execução linha a linha
* Exibição dos registradores AX, BX, CX, DX, SP e IP
* Instruções básicas: MOV, ADD, SUB, PUSH, POP, INT
* Simulação de memória RAM com 64 KB

## Estrutura do Projeto

* `main.py` - Interface gráfica
* `emulador.py` - Classe CPU (registradores e memória)
* `instrucoes.py` - Execução das instruções
* `debug.py` - Modo de depuração

## Como Executar

### Requisitos

* Python 3.10+
* customtkinter

Instalação:

```bash
pip install customtkinter
```

Execução:

```bash
python main.py
```

## Exemplo de Código

```asm
MOV AX, 5
MOV BX, 3
ADD AX, BX
SUB AX, 2
PUSH AX
POP CX
INT 0
```

Saída esperada:

```
AX = 6
BX = 3
CX = 6
DX = 0
SP = 65534
IP = 5
```

## Instruções Suportadas

* MOV reg, reg / MOV reg, valor
* ADD reg, reg / ADD reg, valor
* SUB reg, reg / SUB reg, valor
* PUSH reg
* POP reg
* INT 0 (encerra a execução)

## Debug

* Botão "Debug" abre nova janela
* Botão "Próxima Instrução" executa linha por linha
* Linha atual é destacada
* Registradores atualizados em tempo real

## Autores

* Edmar Miqueias Carvalho Vieira
* Glezier Montalvane de Farias Ferreira
* Luis Eduardo do Rosario Fonseca
