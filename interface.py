import customtkinter as ctk
from emulador import CPU

# inicia a tela
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# cria a janela
app = ctk.CTk()
app.title("miqmiq viado")
app.geometry("800x600")

# botoes superiores
topo_frame = ctk.CTkFrame(app)
topo_frame.pack(pady=10, padx=10, fill="x")

button_rodar = ctk.CTkButton(topo_frame, text="Executar", command=lambda: executar_codigo())
button_rodar.pack(side="left", padx=5)

button_debug = ctk.CTkButton(topo_frame, text="Debug")
button_debug.pack(side="left", padx=5)

# entrada de código
texto_codigo = ctk.CTkTextbox(app, height=250)
texto_codigo.pack(pady=10, padx=10, fill="both", expand=True)

# área de saída
area_saida = ctk.CTkLabel(app, text="Saída:")
area_saida.pack(anchor="w", padx=10)

texto_saida = ctk.CTkTextbox(app, height=150)
texto_saida.pack(pady=10, padx=10, fill="x")

cpu = CPU()

def executar_codigo():
  codigo = texto_codigo.get("1.0", "end")

  try:
    cpu.reset()
    cpu.carregar_programa(codigo)
    cpu.executar()
    linhas = []
    for k, v in cpu.registers.items():
      linhas.append(f"{k} = {v}")
    resultado = "\n".join(linhas)
    texto_saida.insert("1.0", resultado)
  except StopIteration as fim:
    texto_saida.insert("1.0", f"Execução finalizada.\n{fim}\n\n")
    linhas = []
    for k, v in cpu.registers.items():
      linha = f"{k} = {v}"
      linhas.append(linha)
    resultado = "\n".join(linhas)
    texto_saida.insert("end", resultado)
  except Exception as e:
    texto_saida.insert("1.0", f"Erro: {e}")

app.mainloop()