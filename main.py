import customtkinter as ctk
from tkinter import filedialog
from tei_generator import generar_tei

def cargar_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("Texto plano", "*.txt")])
    if ruta:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
            entrada_texto.delete("1.0", "end")
            entrada_texto.insert("1.0", contenido)

def generar():
    texto = entrada_texto.get("1.0", "end").strip()
    api_key = entrada_api.get().strip()

    salida_texto.delete("1.0", "end")  # Limpia antes de escribir

    if not api_key:
        salida_texto.insert("1.0", "⚠️ Debes ingresar tu API key de Groq.")
        return

    resultado = generar_tei(texto, api_key)
    salida_texto.insert("1.0", resultado)

def guardar():
    contenido = salida_texto.get("1.0", "end").strip()
    ruta = filedialog.asksaveasfilename(defaultextension=".xml")
    if ruta:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)

# Interfaz
ctk.set_appearance_mode("light")
ventana = ctk.CTk()
ventana.title("Automatización TEI")

# 🔥 CORREGIDO: ahora indica claramente que es una API de Groq
entrada_api = ctk.CTkEntry(ventana, placeholder_text="API Key de Groq (gsk_...)")
entrada_api.pack(pady=10, fill="x", padx=20)

boton_cargar = ctk.CTkButton(ventana, text="Cargar archivo .txt", command=cargar_archivo)
boton_cargar.pack(pady=10)

entrada_texto = ctk.CTkTextbox(ventana, height=200)
entrada_texto.pack(padx=20, pady=10, fill="both", expand=True)

boton_generar = ctk.CTkButton(ventana, text="Generar TEI", command=generar)
boton_generar.pack(pady=10)

salida_texto = ctk.CTkTextbox(ventana, height=200)
salida_texto.pack(padx=20, pady=10, fill="both", expand=True)

boton_guardar = ctk.CTkButton(ventana, text="Guardar TEI", command=guardar)
boton_guardar.pack(pady=10)

ventana.mainloop()

