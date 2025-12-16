import cv2
import os
import tkinter as tk
from tkinter import filedialog

# --- Seleccionar VIDEO ---
root = tk.Tk()
root.withdraw()  # Ocultar ventana principal
video_path = filedialog.askopenfilename(
    title="Selecciona el video",
    filetypes=[("Videos", "*.mp4 *.avi *.mov *.mkv")]
)

if not video_path:
    print("❌ No seleccionaste ningún video.")
    exit()

# --- Seleccionar CARPETA DE SALIDA ---
output_folder = filedialog.askdirectory(title="Selecciona la carpeta donde guardar las imágenes")

if not output_folder:
    print("❌ No seleccionaste carpeta de salida.")
    exit()

print(f"📹 Video seleccionado: {video_path}")
print(f"📁 Carpeta de salida: {output_folder}")

# Porcentaje del centro a recortar
crop_percent = 0.30  # Recorta el 30% del centro (puedes cambiarlo)

cap = cv2.VideoCapture(video_path)
frame_number = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # Tamaño del recorte
    ch = int(h * crop_percent)
    cw = int(w * crop_percent)

    # Coordenadas del recorte centrado
    x1 = w//2 - cw//2
    x2 = w//2 + cw//2
    y1 = h//2 - ch//2
    y2 = h//2 + ch//2

    # Recortar
    cropped = frame[y1:y2, x1:x2]

    # Guardar
    output_path = os.path.join(output_folder, f"frame_{frame_number}.jpg")
    cv2.imwrite(output_path, cropped)

    print(f"Guardado: frame_{frame_number}.jpg")
    frame_number += 1

cap.release()
print("\n✔️ Todos los frames recortados han sido guardados exitosamente.")
