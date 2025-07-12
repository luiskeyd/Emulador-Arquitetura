# Imports
import customtkinter as ctk
from emulador import CPU
from debug import Debugger  
from instrucoes import mostrar_registradores

# Inicia a aparência da interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Janela principal
app = ctk.CTk()
app.title("Emulador Assembly")
app.geometry("900x700")

# Frame superior com botões
fundo = app.cget("fg_color")
topo_frame = ctk.CTkFrame(app, fg_color=fundo)
topo_frame.pack(pady=10, padx=10)

centralizador = ctk.CTkFrame(topo_frame, fg_color=fundo)
centralizador.pack(expand=True)

button_rodar = ctk.CTkButton(centralizador, text="Executar", command=lambda: executar_codigo())
button_rodar.pack(side="left", padx=10)

# Cria o widget de texto para entrada
# texto_codigo = ctk.CTkTextbox(app, height=200)
# texto_codigo.pack(pady=10, padx=10, fill="both", expand=True)
# texto_codigo.configure(font=("Arial", 16))

# # Cria o caixa de texto para registradores.
# texto_registradores = ctk.CTkTextbox(app, height = 200)
# texto_registradores.pack(anchor = "e", pady = 10, padx = 10, fill = "y", expand= True)
# texto_registradores.configure(font=("Arial", 16))

#posicionado as duas caixas

# Frame para colocar as duas caixas lado a lado
frame_caixas = ctk.CTkFrame(app, fg_color=fundo)
frame_caixas.pack(padx=10, pady=10, fill="both", expand=True)

# Configura para expandir
frame_caixas.grid_columnconfigure(0, weight=150)
frame_caixas.grid_columnconfigure(1, weight=1)
frame_caixas.grid_rowconfigure(0, weight=1)

# Caixa de código à esquerda
texto_codigo = ctk.CTkTextbox(frame_caixas)
texto_codigo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
texto_codigo.configure(font=("Arial", 16))


# Caixa de registradores à direita
texto_registradores = ctk.CTkTextbox(frame_caixas)
texto_registradores.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
texto_registradores.configure(font=("Arial", 16))



# Debugger
debugger = Debugger(texto_codigo)
button_debug = ctk.CTkButton(
    centralizador,
    text="Debug",
    command=lambda: debugger.abrir_debug(texto_codigo.get("1.0", "end"))
)
button_debug.pack(side="left", padx=10)

# Área de saída
area_saida = ctk.CTkLabel(app, text="Saída:")
area_saida.pack(anchor="w", padx=10)

texto_saida = ctk.CTkTextbox(app, height=170)
texto_saida.pack(pady=10, padx=10, fill="x")
texto_saida.configure(font=("Arial", 16))

cpu = CPU()

def executar_codigo():
    texto_saida.delete("1.0", "end")  # Limpar a tela
    codigo = texto_codigo.get("1.0", "end")  # Pegar o código fornecido
    texto_saida.tag_config("erro", foreground="red") # Mensagem em cor vermelha para erro

    # Código em branco
    if not codigo.strip():
        texto_saida.insert("1.0", "Digite algo", "erro")
        return

    # Execução do código
    try:
        cpu.reset()
        cpu.carregar_programa(codigo)
        cpu.executar()
        texto_registradores.configure(state="normal") 
        texto_registradores.delete("1.0", "end")
        texto_registradores.insert("1.0", mostrar_registradores(cpu))
        texto_registradores.configure(state="disabled")
        # texto_saida.insert("1.0", mostrar_registradores(cpu))
    except StopIteration as fim:
        texto_saida.insert("1.0", mostrar_registradores(cpu))
        texto_saida.insert("end", f"\n\n{fim}")
    except Exception as e:
        texto_saida.insert("1.0", str(e), "erro")

app.mainloop()