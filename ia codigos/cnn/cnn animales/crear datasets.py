import cv2
import os
import tkinter as tk
from tkinter import filedialog

# ================================
#   Seleccionar video
# ================================
def seleccionar_video():
    ruta_video = filedialog.askopenfilename(
        title="Seleccionar video",
        filetypes=[("Videos", "*.mp4 *.avi *.mov *.mkv")]
    )
    return ruta_video

# ================================
#   Seleccionar carpeta destino
# ================================
def seleccionar_carpeta():
    ruta = filedialog.askdirectory(
        title="Seleccionar carpeta donde guardar imágenes"
    )
    return ruta

# ================================
#   Extraer imágenes
# ================================
def extraer_frames(video_path, output_path, salto_frames=10):
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("❌ No se pudo abrir el video")
        return
    
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"🎞 Total frames en el video: {total_frames}")

    frame_num = 0
    img_num = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break  # No más frames
        
        # Solo guardar cada N frames
        if frame_num % salto_frames == 0:
            nombre_imagen = os.path.join(output_path, f"fra2_{img_num:05d}.jpg")
            cv2.imwrite(nombre_imagen, frame)
            print(f"🖼 Guardada: {nombre_imagen}")
            img_num += 1

        frame_num += 1

    video.release()
    print("\n✅ Proceso completado.")
    print(f"📸 Total imágenes guardadas: {img_num}")

# ================================
#   Programa principal
# ================================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal

    print("📂 Selecciona el video a procesar...")
    video_path = seleccionar_video()

    if not video_path:
        print("❌ No seleccionaste ningún video.")
        exit()

    print("📁 Selecciona la carpeta donde se guardarán las imágenes...")
    output_path = seleccionar_carpeta()

    if not output_path:
        print("❌ No seleccionaste ninguna carpeta.")
        exit()

    # 🔧 Ajusta cada cuántos frames quieres guardar una imagen
    FRAMES_SALTO = 1   # ejemplo: guardar 1 imagen cada 15 frames

    extraer_frames(video_path, output_path, salto_frames=FRAMES_SALTO)
