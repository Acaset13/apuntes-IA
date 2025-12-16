import os
import cv2

# ================================
# CONFIGURACIÓN
# ================================
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "animals")
TARGET_SIZE = (25, 25)
VALID_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")

print("📂 Carpeta base:", BASE_DIR)

# ================================
# PROCESAR
# ================================
total_redimensionadas = 0

for root, dirs, files in os.walk(BASE_DIR):

    # Saltar la carpeta principal, procesar solo subcarpetas
    if root == BASE_DIR:
        continue

    nombre_carpeta = os.path.basename(root)
    print(f"\n📁 Procesando carpeta: {nombre_carpeta}")

    procesadas = 0

    for filename in files:

        if not filename.lower().endswith(VALID_EXT):
            continue

        img_path = os.path.join(root, filename)

        # Leer imagen
        img = cv2.imread(img_path)

        if img is None:
            print(f"❌ ERROR leyendo: {img_path}")
            continue

        # Redimensionar
        img_resized = cv2.resize(img, TARGET_SIZE, interpolation=cv2.INTER_AREA)

        # Guardar
        cv2.imwrite(img_path, img_resized)

        procesadas += 1
        total_redimensionadas += 1

        print(f"✔ {filename} redimensionada")

    print(f"📌 Total en {nombre_carpeta}: {procesadas}")

print("\n🎉 PROCESO FINALIZADO")
print(f"🖼 Total imágenes redimensionadas: {total_redimensionadas}")
