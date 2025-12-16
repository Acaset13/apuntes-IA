import cv2
import os

# Crear carpeta de la persona (si no existe)
personName = input("Nombre de la persona: ").strip()
dataPath = os.path.dirname(os.path.abspath(__file__))
personPath = os.path.join(dataPath, personName)

if not os.path.exists(personPath):
    os.makedirs(personPath)
    print(f"✅ Carpeta creada: {personPath}")
else:
    print(f"⚠️ Ya existe la carpeta: {personPath}")

# Inicializar cámara
cap = cv2.VideoCapture(0)
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

count = 0
print("\n Presiona [ESC] para salir o espera a que se tomen 100 fotos\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = frame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (100, 100), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(os.path.join(personPath, f"rostro_{count}.jpg"), rostro)
        count += 1

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f'Capturando {personName} - {count}', (x, y-10), 2, 0.7, (0,255,0), 1, cv2.LINE_AA)

    cv2.imshow('Captura de Rostros', frame)

    if cv2.waitKey(1) == 27 or count >= 600:  # ESC o 100 fotos
        break

cap.release()
cv2.destroyAllWindows()
print(f"\n Se guardaron {count} imágenes en: {personPath}")
