# --- 1. Importar librerías ---
import numpy as np
import os, re
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, LeakyReLU
from tensorflow.keras.layers import BatchNormalization, Conv2D, MaxPooling2D

from tkinter import Tk, filedialog
from skimage.transform import resize

# --- 2. Ruta del dataset y modelo ---
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "animals")
imgpath = base_dir + os.sep

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "animals_model.h5")

# ======================================================
# 🟦 SI YA EXISTE EL MODELO, SOLO SE CARGA Y SE USA
# ======================================================
if os.path.exists(model_path):
    print("\n🔵 MODELO ENCONTRADO. NO SE ENTRENARÁ.")
    print("📁 Cargando modelo:", model_path)

    model = load_model(model_path)

    # Leer nombres de clases
    animales = sorted(os.listdir(base_dir))
    animales = [a for a in animales if os.path.isdir(os.path.join(base_dir, a))]

    print("\n🏷️ Clases detectadas:", animales)

    # --- Función para predecir ---
    def seleccionar_y_predecir():
        print("\n📸 Ingresa la ruta completa de la imagen a clasificar:")
        filepath = input("Ruta: ").strip().replace('"', '')

        if not os.path.exists(filepath):
            print("❌ La ruta no existe. Intenta de nuevo.")
            return

        try:
            image = plt.imread(filepath)
        except Exception as e:
            print(f"⚠ Error leyendo la imagen: {e}")
            return

        if len(image.shape) == 2:
            image = np.stack((image,) * 3, axis=-1)

        image_resized = resize(image, (25, 25), anti_aliasing=True)
        X_pred = np.array([image_resized], dtype=np.float32) / 255.

        pred = model.predict(X_pred)[0]
        clase = animales[np.argmax(pred)]
        confianza = np.max(pred) * 100

        print("\n🔍 RESULTADO:")
        print("  ✔ Clase detectada:", clase)
        print(f"  ✔ Confianza: {confianza:.2f}%")
        seleccionar_y_predecir()



    # Preguntar al usuario
    opc = input("\n¿Quieres clasificar una imagen? (s/n): ").lower()
    if opc == "s":
        seleccionar_y_predecir()

    exit()


# ======================================================
# 🟥 SI NO EXISTE EL MODELO, SE ENTRENA COMPLETO
# ======================================================
print("\n🟥 NO EXISTE MODELO. ENTRENANDO DESDE CERO...")
print("📂 Leyendo imágenes desde:", imgpath)

# --- 3. Leer imágenes ---
images = []
directories = []
dircount = []
prevRoot = ''
cant = 0

IMG_SIZE = (25, 25)

for root, dirnames, filenames in os.walk(imgpath):
    for filename in filenames:
        if filename == '.DS_Store':
            continue
        if re.search(r"\.(jpg|jpeg|png|bmp|tiff)$", filename, re.IGNORECASE):

            filepath = os.path.join(root, filename)
            cant += 1

            try:
                image = plt.imread(filepath)

                if len(image.shape) == 2:
                    image = np.stack((image,) * 3, axis=-1)

                image = resize(image, IMG_SIZE, anti_aliasing=True)
                images.append(image)

            except Exception as e:
                print(f"⚠ Error leyendo {filepath}: {e}")
                continue

            print(f"Leyendo imagen {cant} en carpeta: {os.path.basename(root)}", end="\r")

            if prevRoot != root:
                print(f"\n📁 Carpeta encontrada: {os.path.basename(root)}")
                prevRoot = root
                directories.append(root)
                dircount.append(cant)
                cant = 0

dircount.append(cant)
dircount = dircount[1:]
if len(dircount) > 0:
    dircount[0] += 1

print("\n📸 Imágenes por carpeta:", dircount)
print("🧮 Total:", sum(dircount))

# --- 4. Crear etiquetas ---
animales = []
labels = []
indice = 0

for directorio in directories:
    name = os.path.basename(directorio)
    animales.append(name)
    print(indice, name)

    for i in range(dircount[indice]):
        labels.append(indice)

    indice += 1

y = np.array(labels)
X = np.array(images, dtype=np.float32)

print("\nDataset:", X.shape)

# --- 5. Separar datos ---
train_X, test_X, train_Y, test_Y = train_test_split(X, y, test_size=0.2)
train_X, valid_X, train_label, valid_label = train_test_split(
    train_X, train_Y, test_size=0.2, random_state=13
)

# --- 6. Normalizar ---
train_X /= 255.
test_X /= 255.
valid_X /= 255.

# --- 7. One-hot ---
train_label = to_categorical(train_label)
valid_label = to_categorical(valid_label)
test_Y_one_hot = to_categorical(test_Y)

# --- 8. Hiperparámetros ---
INIT_LR = 1e-3
epochs = 150
batch_size = 64
filters = 32
dense_neurons = 64

# --- 9. Definir modelo ---
model = Sequential()

model.add(Conv2D(filters, (3, 3), activation='linear', padding='same',
                 input_shape=(25, 25, 3)))
model.add(LeakyReLU(alpha=0.1))
model.add(MaxPooling2D((2, 2), padding='same'))
model.add(Dropout(0.3))

model.add(Conv2D(filters*2, (3, 3), activation='linear', padding='same'))
model.add(LeakyReLU(alpha=0.1))
model.add(MaxPooling2D((2, 2), padding='same'))
model.add(Dropout(0.3))

model.add(Flatten())
model.add(Dense(dense_neurons, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(animales), activation='softmax'))

# --- 10. Compilar ---
model.compile(
    loss=tf.keras.losses.categorical_crossentropy,
    optimizer=tf.keras.optimizers.Adam(learning_rate=INIT_LR),
    metrics=['accuracy']
)

# --- 11. Entrenar ---
print("\n🚀 Entrenando modelo...\n")

model.fit(
    train_X, train_label,
    batch_size=batch_size,
    epochs=epochs,
    verbose=1,
    validation_data=(valid_X, valid_label)
)

# --- 12. Guardar modelo ---
model.save(model_path)
print("\n💾 Modelo guardado en:", model_path)

# --- 13. Evaluar ---
eval = model.evaluate(test_X, test_Y_one_hot)
print("\nPrecisión:", eval[1] * 100)

# --- 14. Reporte ---
y_pred = model.predict(test_X)
y_pred_classes = np.argmax(y_pred, axis=1)

print("\n📊 Reporte:")
print(classification_report(test_Y, y_pred_classes, target_names=animales))

print("\n✔ Entrenamiento terminado.")

