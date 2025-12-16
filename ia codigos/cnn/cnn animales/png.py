import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Extensiones permitidas (imágenes reales)
EXTENSIONES_IMAGEN = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}

def es_imagen(nombre):
    extension = os.path.splitext(nombre)[1].lower()
    return extension in EXTENSIONES_IMAGEN

def limpiar_carpeta():
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta a limpiar")

    if not carpeta:
        return

    eliminados = 0
    total = 0

    for archivo in os.listdir(carpeta):
        ruta = os.path.join(carpeta, archivo)
        total += 1

        if not os.path.isfile(ruta):
            continue

        if not es_imagen(archivo):
            try:
                os.remove(ruta)
                eliminados += 1
            except Exception as e:
                print("Error eliminando:", ruta, e)

    messagebox.showinfo(
        "Proceso completado",
        f"Archivos totales: {total}\n"
        f"Imágenes eliminadas: {eliminados}"
    )

# Interfaz gráfica simple
app = tk.Tk()
app.title("Limpieza de imágenes")
app.geometry("350x150")

btn = tk.Button(app, text="Seleccionar carpeta y limpiar", command=limpiar_carpeta, font=("Arial", 12))
btn.pack(pady=40)

app.mainloop()
