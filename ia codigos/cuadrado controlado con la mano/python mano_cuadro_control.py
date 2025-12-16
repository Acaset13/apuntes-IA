import cv2
import mediapipe as mp
import numpy as np
import math

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Función para calcular distancia y ángulo
def distancia_y_angulo(p1, p2):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    distancia = math.sqrt(dx**2 + dy**2)
    angulo = math.degrees(math.atan2(dy, dx))
    return distancia, angulo

# Función para dibujar un cuadrado rotado
def dibujar_cuadro(frame, center, size, angle):
    # Crear una matriz de rotación
    rect = np.array([
        [-size/2, -size/2],
        [ size/2, -size/2],
        [ size/2,  size/2],
        [-size/2,  size/2]
    ])

    rotacion = np.array([
        [math.cos(math.radians(angle)), -math.sin(math.radians(angle))],
        [math.sin(math.radians(angle)),  math.cos(math.radians(angle))]
    ])

    rect_rotado = np.dot(rect, rotacion) + center
    puntos = rect_rotado.astype(np.int32)
    cv2.polylines(frame, [puntos], True, (0, 255, 0), 3)

# Captura de video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ No se pudo acceder a la cámara.")
    exit()

print("✅ Control de cuadrado con dedos (presiona 'q' para salir)")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Procesar la imagen con MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Coordenadas del pulgar e índice
            pulgar = hand_landmarks.landmark[4]
            indice = hand_landmarks.landmark[8]

            p1 = np.array([int(pulgar.x * w), int(pulgar.y * h)])
            p2 = np.array([int(indice.x * w), int(indice.y * h)])

            # Calcular distancia y ángulo
            distancia, angulo = distancia_y_angulo(p1, p2)

            # Escalar tamaño (ajustar sensibilidad)
            size = max(50, min(int(distancia * 2.5), 400))

            # Centro del cuadrado
            centro = (w // 2, h // 2)

            # Dibujar cuadrado
            dibujar_cuadro(frame, centro, size, angulo)

            # Mostrar datos
            cv2.putText(frame, f"Distancia: {int(distancia)}", (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, f"Angulo: {int(angulo)}°", (30, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Control con Mano - Escala y Rotacion", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
