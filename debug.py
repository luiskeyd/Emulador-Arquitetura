import customtkinter as ctk
from emulador import CPU

# Classe do debug
class Debugger:
    #
    def __init__(self, texto_codigo_widget):
        self.cpu = CPU()
        self.janela_debug = None
        self.debug_ip = 0
        self.texto_debug_saida = None
        self.texto_debug_codigo = None
        self.texto_codigo = texto_codigo_widget

    def abrir_debug(self, codigo_str):
        if self.janela_debug and self.janela_debug.winfo_exists():
            self.janela_debug.focus()
            self.janela_debug.lift()
            return

        self.cpu.reset()
        self.cpu.carregar_programa(codigo_str)
        self.debug_ip = 0

        if self.texto_codigo:
            self.texto_codigo.tag_remove("linha_atual", "1.0", "end")
            try:
                self.texto_codigo.tag_config("linha_atual", background="yellow", foreground="black")
            except:
                pass

        self.janela_debug = ctk.CTkToplevel()
        self.janela_debug.title("Modo Debug")
        self.janela_debug.geometry("800x500")

        self.janela_debug.focus_force()
        self.janela_debug.attributes('-topmost', True)
        self.janela_debug.after(10, lambda: self.janela_debug.attributes('-topmost', False))

        container = ctk.CTkFrame(self.janela_debug)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.texto_debug_codigo = ctk.CTkTextbox(container, width=400)
        self.texto_debug_codigo.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.texto_debug_saida = ctk.CTkTextbox(container, width=200)
        self.texto_debug_saida.pack(side="left", fill="both", expand=False)

        button_next = ctk.CTkButton(self.janela_debug, text="Próxima Instrução", command=self.executar_proxima_instrucao)
        button_next.pack(pady=10)

        self.texto_debug_codigo.delete("1.0", "end")
        for linha in self.cpu.programa:
            self.texto_debug_codigo.insert("end", linha + "\n")

        self.texto_debug_codigo.tag_config("linha_atual", background="yellow", foreground="black")
        self.executar_proxima_instrucao()

    def executar_proxima_instrucao(self):
        self.texto_debug_saida.delete("1.0", "end")
        self.texto_debug_codigo.tag_remove("linha_atual", "1.0", "end")

        try:
            if self.debug_ip < len(self.cpu.programa):
                linha = self.cpu.programa[self.debug_ip]

                linha_inicio = f"{self.debug_ip + 1}.0"
                linha_fim = f"{self.debug_ip + 1}.end"
                self.texto_debug_codigo.tag_add("linha_atual", linha_inicio, linha_fim)

                self.cpu.executar_instrucoes(linha)
                self.cpu.registers['IP'] = self.debug_ip
                self.debug_ip += 1

                self.mostrar_registradores_debug()
            else:
                self.texto_debug_saida.insert("end", "Fim da execução (EOF)")
                self.texto_debug_codigo.tag_remove("linha_atual", "1.0", "end")

        except StopIteration as fim:
            self.mostrar_registradores_debug()
            self.texto_debug_saida.insert("end", f"\n{fim}")
            self.texto_debug_codigo.tag_remove("linha_atual", "1.0", "end")

        except Exception as e:
            self.mostrar_registradores_debug()
            self.texto_debug_saida.insert("end", f"\nErro: {e}")
            self.texto_debug_codigo.tag_remove("linha_atual", "1.0", "end")

    def mostrar_registradores_debug(self):
        linhas = []
        for k, v in self.cpu.registers.items():
            linhas.append(f"{k} = {v}")
        resultado = "\n".join(linhas)
        self.texto_debug_saida.delete("1.0", "end")
        self.texto_debug_saida.insert("1.0", resultado)



