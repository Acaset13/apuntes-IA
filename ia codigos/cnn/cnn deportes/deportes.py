# --- 1. Importar librerías ---
import numpy as np
import os, re
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, LeakyReLU
from tensorflow.keras.layers import (
    BatchNormalization, Conv2D, MaxPooling2D, Activation
)

# --- 2. Ruta del dataset ---
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sportimages")
imgpath = base_dir + os.sep
print("📂 Leyendo imágenes desde:", imgpath)

# --- 3. Leer imágenes ---
images = []
directories = []
dircount = []
prevRoot = ''
cant = 0

for root, dirnames, filenames in os.walk(imgpath):
    for filename in filenames:
        if filename == '.DS_Store':  # ignorar archivos del sistema
            continue
        if re.search(r"\.(jpg|jpeg|png|bmp|tiff)$", filename, re.IGNORECASE):
            cant += 1
            filepath = os.path.join(root, filename)
            image = plt.imread(filepath)
            if len(image.shape) == 3:
                images.append(image)
            print(f"Leyendo imagen {cant}", end="\r")
            if prevRoot != root:
                print(f"\n📁 Carpeta: {root}")
                prevRoot = root
                directories.append(root)
                dircount.append(cant)
                cant = 0
dircount.append(cant)

dircount = dircount[1:]
if len(dircount) > 0:
    dircount[0] += 1

print("\n✅ Directorios leídos:", len(directories))
print("📸 Imágenes por carpeta:", dircount)
print("🧮 Total de imágenes:", sum(dircount))

# --- 4. Crear etiquetas ---
deportes = []
indice = 0
labels = []

for directorio in directories:
    name = os.path.basename(directorio)
    print(indice, name)
    deportes.append(name)
    for i in range(dircount[indice]):
        labels.append(indice)
    indice += 1

y = np.array(labels)
X = np.array(images, dtype=np.uint8)
classes = np.unique(y)
nClasses = len(classes)
print("\n⚙️ Total de clases:", nClasses)
print("🏷️ Clases detectadas:", deportes)

# --- 5. Separar datos ---
train_X, test_X, train_Y, test_Y = train_test_split(X, y, test_size=0.2)
train_X, valid_X, train_label, valid_label = train_test_split(train_X, train_Y, test_size=0.2, random_state=13)

# --- 6. Normalizar ---
train_X = train_X.astype('float32') / 255.
test_X = test_X.astype('float32') / 255.
valid_X = valid_X.astype('float32') / 255.

# --- 7. One-hot encoding ---
train_label = to_categorical(train_label)
valid_label = to_categorical(valid_label)
test_Y_one_hot = to_categorical(test_Y)

print("\n✅ Datos preparados para el modelo.")
print(train_X.shape, valid_X.shape, train_label.shape, valid_label.shape)

# --- 8. Parámetros modificables ---
INIT_LR = 1e-3      # tasa de aprendizaje inicial
epochs = 15          # número de épocas (puedes cambiarlo)
batch_size = 64      # tamaño del lote
filters = 32         # cantidad de filtros convolucionales
dense_neurons = 64   # neuronas en la capa densa

# --- 9. Definir el modelo ---
sport_model = Sequential()

sport_model.add(Conv2D(filters, kernel_size=(3, 3), activation='linear',
                       padding='same', input_shape=(train_X.shape[1], train_X.shape[2], 3)))
sport_model.add(LeakyReLU(alpha=0.1))
sport_model.add(MaxPooling2D((2, 2), padding='same'))
sport_model.add(Dropout(0.3))

# Segunda capa convolucional opcional
sport_model.add(Conv2D(filters*2, kernel_size=(3, 3), activation='linear', padding='same'))
sport_model.add(LeakyReLU(alpha=0.1))
sport_model.add(MaxPooling2D((2, 2), padding='same'))
sport_model.add(Dropout(0.3))

# Capa densa
sport_model.add(Flatten())
sport_model.add(Dense(dense_neurons, activation='relu'))
sport_model.add(Dropout(0.5))
sport_model.add(Dense(nClasses, activation='softmax'))

sport_model.summary()

# --- 10. Compilación ---
sport_model.compile(
    loss=tf.keras.losses.categorical_crossentropy,
    optimizer=tf.keras.optimizers.Adam(learning_rate=INIT_LR),
    metrics=['accuracy']
)

# --- 11. Entrenamiento con porcentaje ---
print("\n🚀 Entrenando el modelo...\n")
sport_train = sport_model.fit(
    train_X, train_label,
    batch_size=batch_size,
    epochs=epochs,
    verbose=1,  # ya muestra porcentaje
    validation_data=(valid_X, valid_label)
)

# --- 12. Guardar modelo ---
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sport_model.h5")
sport_model.save(model_path)
print(f"\n💾 Modelo guardado en: {model_path}")

# --- 13. Evaluación ---
test_eval = sport_model.evaluate(test_X, test_Y_one_hot, verbose=1)
print(f"\n📉 Pérdida en prueba: {test_eval[0]:.4f}")
print(f"✅ Precisión en prueba: {test_eval[1]*100:.2f}%")

# --- 14. Curvas de aprendizaje ---
accuracy = sport_train.history['accuracy']
val_accuracy = sport_train.history['val_accuracy']
loss = sport_train.history['loss']
val_loss = sport_train.history['val_loss']
epochs_range = range(len(accuracy))

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, accuracy, 'bo-', label='Entrenamiento')
plt.plot(epochs_range, val_accuracy, 'r.-', label='Validación')
plt.title('Precisión del modelo')
plt.xlabel('Época')
plt.ylabel('Precisión')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, 'bo-', label='Entrenamiento')
plt.plot(epochs_range, val_loss, 'r.-', label='Validación')
plt.title('Pérdida del modelo')
plt.xlabel('Época')
plt.ylabel('Pérdida')
plt.legend()
plt.tight_layout()
plt.show()

# --- 15. Prueba con imagen nueva ---
from skimage.transform import resize

filenames = ['test/futbol.jpg']  # cambia por la imagen que tengas
images = []
for filepath in filenames:
    if os.path.exists(filepath):
        image = plt.imread(filepath)
        image_resized = resize(image, (train_X.shape[1], train_X.shape[2]), anti_aliasing=True)
        images.append(image_resized)
    else:
        print(f"⚠️ No se encontró la imagen {filepath}")

X_pred = np.array(images, dtype=np.float32) / 255.
predicted_classes = sport_model.predict(X_pred)

for i, img_tagged in enumerate(predicted_classes):
    print(f"{filenames[i]} → Predicción: {deportes[np.argmax(img_tagged)]}")
