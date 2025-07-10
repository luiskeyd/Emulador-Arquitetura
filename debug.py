import customtkinter as ctk
from emulador import CPU

cpu = CPU()
janela_debug = None
debug_ip = 0
texto_debug_saida = None
texto_debug_codigo = None
texto_codigo = None

def set_texto_codigo_ref(text_widget):
    global texto_codigo
    texto_codigo = text_widget

def abrir_debug(codigo_str):
    global janela_debug, debug_ip, texto_debug_saida, texto_debug_codigo

    if janela_debug is not None and janela_debug.winfo_exists():
        janela_debug.lift()
        return

    cpu.reset()
    cpu.carregar_programa(codigo_str)
    debug_ip = 0

    if texto_codigo:
        texto_codigo.tag_remove("linha_atual", "1.0", "end")
        try:
            texto_codigo.tag_config("linha_atual", background="yellow")
        except:
            pass

    janela_debug = ctk.CTkToplevel()
    janela_debug.title("Modo Debug")
    janela_debug.geometry("800x500")

    # Força foco e traz para frente
    janela_debug.lift()
    janela_debug.focus_force()
    janela_debug.attributes('-topmost', True)
    janela_debug.after(10, lambda: janela_debug.attributes('-topmost', False))

    container = ctk.CTkFrame(janela_debug)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Código e registradores lado a lado
    texto_debug_codigo = ctk.CTkTextbox(container, width=400)
    texto_debug_codigo.pack(side="left", fill="both", expand=True, padx=(0, 5))

    texto_debug_saida = ctk.CTkTextbox(container, width=200)
    texto_debug_saida.pack(side="left", fill="both", expand=False)

    button_next = ctk.CTkButton(janela_debug, text="Próxima Instrução", command=executar_proxima_instrucao)
    button_next.pack(pady=10)

    # Inserir o código completo com tags por linha
    texto_debug_codigo.delete("1.0", "end")
    for linha in cpu.programa:
        texto_debug_codigo.insert("end", linha + "\n")

    texto_debug_codigo.tag_config("linha_atual", background="yellow")
    executar_proxima_instrucao()

def executar_proxima_instrucao():
    global debug_ip

    texto_debug_saida.delete("1.0", "end")
    texto_debug_codigo.tag_remove("linha_atual", "1.0", "end")

    try:
        if debug_ip < len(cpu.programa):
            linha = cpu.programa[debug_ip]

            linha_inicio = f"{debug_ip + 1}.0"
            linha_fim = f"{debug_ip + 1}.end"
            texto_debug_codigo.tag_add("linha_atual", linha_inicio, linha_fim)

            cpu.executar_instrucoes(linha)
            cpu.registers['IP'] = debug_ip
            debug_ip += 1

            mostrar_registradores_debug()
        else:
            texto_debug_saida.insert("end", "Fim da execução (EOF)")
            texto_debug_codigo.tag_remove("linha_atual", "1.0", "end")

    except StopIteration as fim:
        mostrar_registradores_debug()
        texto_debug_saida.insert("end", f"\n{fim}")
        texto_debug_codigo.tag_remove("linha_atual", "1.0", "end")

    except Exception as e:
        mostrar_registradores_debug()
        texto_debug_saida.insert("end", f"\nErro: {e}")
        texto_debug_codigo.tag_remove("linha_atual", "1.0", "end")

def mostrar_registradores_debug():
    linhas = [f"{k} = {v}" for k, v in cpu.registers.items()]
    resultado = "\n".join(linhas)
    texto_debug_saida.insert("1.0", resultado)