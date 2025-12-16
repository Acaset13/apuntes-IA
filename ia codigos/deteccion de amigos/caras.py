import cv2
import os
import numpy as np

# Ruta donde están las carpetas de personas (mismo lugar que este archivo)
basePath = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(basePath, 'fisherfaces_model.xml')

# Listar las carpetas (personas)
peopleList = [d for d in os.listdir(basePath) if os.path.isdir(os.path.join(basePath, d)) and d != "__pycache__"]
print("Personas detectadas:", peopleList)

# --- Crear o cargar el modelo ---
face_recognizer = cv2.face.FisherFaceRecognizer_create()

# Si el modelo ya existe, cargarlo (evita reentrenar)
if os.path.exists(model_path):
    print("\n Modelo existente encontrado. Cargando sin reentrenar...")
    face_recognizer.read(model_path)
else:
    # --- Preparar datos ---
    labels = []
    facesData = []
    label = 0
    total_fotos = 0

    # Contar total de imágenes (para mostrar progreso)
    for nameDir in peopleList:
        personPath = os.path.join(basePath, nameDir)
        total_fotos += len(os.listdir(personPath))

    procesadas = 0

    for nameDir in peopleList:
        personPath = os.path.join(basePath, nameDir)
        print(f"\n Leyendo imágenes de: {nameDir}")

        for fileName in os.listdir(personPath):
            imagePath = os.path.join(personPath, fileName)
            img = cv2.imread(imagePath, 0)

            #  Validar si la imagen se cargó correctamente
            if img is None:
                print(" Imagen no válida:", imagePath)
                continue

            #  Redimensionar para acelerar el entrenamiento
            img = cv2.resize(img, (100, 100), interpolation=cv2.INTER_CUBIC)

            facesData.append(img)
            labels.append(label)

            procesadas += 1
            print(f"  Progreso: {procesadas}/{total_fotos} imágenes procesadas", end='\r')

        label += 1

    print("\n\n Lectura de imágenes completada.")

    # --- Entrenar modelo Fisherfaces ---
    print("\nEntrenando modelo, por favor espera...")
    face_recognizer.train(facesData, np.array(labels))
    print(" Modelo entrenado correctamente")

    # Guardar modelo entrenado en la carpeta del código
    face_recognizer.write(model_path)
    print(f" Modelo guardado en: {model_path}")

# --- Prueba con cámara ---
print("\nIniciando cámara para reconocimiento... (presiona ESC para salir)")
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = gray[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (100, 100), interpolation=cv2.INTER_CUBIC)
        label, confidence = face_recognizer.predict(rostro)

        # --- Precisión ajustada ---
        if confidence < 80:
            name = peopleList[label]
            color = (0, 255, 0)
        else:
            name = "Desconocido"
            color = (0, 0, 255)

        text = f'{name} ({round(confidence, 2)})'
        cv2.putText(frame, text, (x, y-10), 2, 0.7, color, 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    cv2.imshow('🎥 Reconocimiento Facial - Fisherfaces', frame)
    if cv2.waitKey(1) == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
print("\n Programa finalizado.")
