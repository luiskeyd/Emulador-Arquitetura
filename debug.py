# Imports
import customtkinter as ctk
from emulador import CPU
from instrucoes import mostrar_registradores, interpretar

# Classe do debug
class Debugger:
    def __init__(self, codigo):
        self.cpu = CPU()
        self.janela_debug = None
        self.saida_debug = None
        self.texto_debug = None
        self.codigo = codigo

    # Limpar destaque
    def limpar_destaque(self):
        if self.codigo and self.codigo.winfo_exists():
            try:
                self.codigo.tag_remove("linha_atual", "1.0", "end")
            except:
                pass

        if self.texto_debug and self.texto_debug.winfo_exists():
            try:
                self.texto_debug.tag_remove("linha_atual", "1.0", "end")
            except:
                self.texto_debug = None

    # Fechar o debug
    def fechar_debug(self):
        if self.janela_debug:
            self.janela_debug.destroy()
            self.janela_debug = None
            self.texto_debug = None
            self.saida_debug = None

    def abrir_debug(self, codigo):
        if not codigo.strip():
            return

        # Impede abrir várias janelas
        if self.janela_debug and self.janela_debug.winfo_exists():
            self.janela_debug.focus()
            self.janela_debug.lift()
            return

        # Preparar CPU
        self.cpu.reset()
        self.cpu.carregar_programa(codigo)
        self.cpu.registers["IP"] = 0
        self.limpar_destaque()
        
        # Marcar linha atual
        try:
            self.codigo.tag_config("linha_atual", background="yellow", foreground="black")
        except:
            pass

        # Configurações da janela e seus itens
        self.janela_debug = ctk.CTkToplevel()
        self.janela_debug.protocol("WM_DELETE_WINDOW", self.fechar_debug)
        self.janela_debug.title("Modo Debug")
        self.janela_debug.geometry("800x500")
        self.janela_debug.focus_force()
        self.janela_debug.attributes('-topmost', True)
        self.janela_debug.after(10, lambda: self.janela_debug.attributes('-topmost', False))

        container = ctk.CTkFrame(self.janela_debug)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.texto_debug = ctk.CTkTextbox(container, width=400)
        self.texto_debug.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.saida_debug = ctk.CTkTextbox(container, width=200)
        self.saida_debug.pack(side="left", fill="both", expand=False)

        button_next = ctk.CTkButton(self.janela_debug, text="Próxima Instrução", command=self.executar_proxima_instrucao)
        button_next.pack(pady=10)

        self.texto_debug.configure(state="normal")
        self.texto_debug.delete("1.0", "end")
        for linha in self.cpu.programa:
            self.texto_debug.insert("end", linha + "\n")
        self.texto_debug.configure(state="disabled")

        self.texto_debug.tag_config("linha_atual", background="yellow", foreground="black")
        self.executar_proxima_instrucao()

    # Executar próxima instrução
    def executar_proxima_instrucao(self):
        self.saida_debug.delete("1.0", "end")
        self.limpar_destaque()

        try:
            ip = self.cpu.registers["IP"]
            if ip < len(self.cpu.programa):
                linha = self.cpu.programa[ip]

                linha_inicio = f"{ip + 1}.0"
                linha_fim = f"{ip+ 1}.end"
                if self.texto_debug and self.texto_debug.winfo_exists():
                    self.texto_debug.tag_add("linha_atual", linha_inicio, linha_fim)

                interpretar(self.cpu, linha)
                if self.cpu.registers['IP'] == ip:
                    self.cpu.registers["IP"] += 1

                self.mostrar_registradores()
            else:
                self.saida_debug.insert("end", "Fim da execução (EOF)")
                if self.texto_debug and self.texto_debug.winfo_exists():
                    self.texto_debug.tag_remove("linha_atual", "1.0", "end")

        except StopIteration as fim:
            self.mostrar_registradores()
            self.saida_debug.insert("end", f"\n{fim}")
            if self.texto_debug and self.texto_debug.winfo_exists():
                self.texto_debug.tag_remove("linha_atual", "1.0", "end")

        except Exception as e:
            self.mostrar_registradores()
            self.saida_debug.insert("end", f"\nErro: {e}")
            if self.texto_debug and self.texto_debug.winfo_exists():
                self.texto_debug.tag_remove("linha_atual", "1.0", "end")
    
    # Mostrar registradores no debug
    def mostrar_registradores(self):
        resultado = mostrar_registradores(self.cpu)
        self.saida_debug.configure(state="normal")
        self.saida_debug.delete("1.0", "end")
        self.saida_debug.insert("1.0", resultado)
        self.saida_debug.configure(state="disabled")
