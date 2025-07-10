import customtkinter as ctk
from emulador import CPU
import debug

# Inicia a aparência da interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Janela principal
app = ctk.CTk()
app.title("Emulador Assembly")
app.geometry("800x600")

# Frame superior com botões
topo_frame = ctk.CTkFrame(app)
topo_frame.pack(pady=10, padx=10, fill="x")

button_rodar = ctk.CTkButton(topo_frame, text="Executar", command=lambda: executar_codigo())
button_rodar.pack(side="left", padx=5)

button_debug = ctk.CTkButton(
    topo_frame,
    text="Debug",
    command=lambda: debug.abrir_debug(texto_codigo.get("1.0", "end"))
)
button_debug.pack(side="left", padx=5)

# Entrada de código
texto_codigo = ctk.CTkTextbox(app, height=250)
texto_codigo.pack(pady=10, padx=10, fill="both", expand=True)

# Passa referência para debug
debug.set_texto_codigo_ref(texto_codigo)

# Área de saída
area_saida = ctk.CTkLabel(app, text="Saída:")
area_saida.pack(anchor="w", padx=10)

texto_saida = ctk.CTkTextbox(app, height=150)
texto_saida.pack(pady=10, padx=10, fill="x")

cpu = CPU()

def mostrar_registradores():
    linhas = []
    for k, v in cpu.registers.items():
        linhas.append(f"{k} = {v}")
    resultado = "\n".join(linhas)
    texto_saida.insert("1.0", resultado)

def executar_codigo():
    texto_saida.delete("1.0", "end")
    codigo = texto_codigo.get("1.0", "end")

    try:
        cpu.reset()
        cpu.carregar_programa(codigo)
        cpu.executar()
        mostrar_registradores()
    except StopIteration as fim:
        mostrar_registradores()
        texto_saida.insert("end", f"\n\n{fim}")
    except Exception as e:
        texto_saida.insert("1.0", f"Erro: {e}")

app.mainloop()