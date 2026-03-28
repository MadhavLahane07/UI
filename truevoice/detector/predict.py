import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from PIL import Image
import os

IMG_SIZE = 128

# 🔥 Load model using absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.h5")

model = load_model(model_path)

def audio_to_image(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    plt.figure(figsize=(3,3))
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_db = librosa.power_to_db(S, ref=np.max)

    librosa.display.specshow(S_db, sr=sr)
    plt.axis('off')

    temp_img = os.path.join(BASE_DIR, "temp.png")
    plt.savefig(temp_img, bbox_inches='tight', pad_inches=0)
    plt.close()

    return temp_img

def predict_audio(audio_path):
    img_path = audio_to_image(audio_path)

    # 🔥 Convert to RGB (fix 4-channel issue)
    img = Image.open(img_path).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0][0]

    os.remove(img_path)

    if prediction > 0.5:
        return "Real Voice", float(prediction)
    else:
        return "Deepfake Voice", float(1 - prediction)