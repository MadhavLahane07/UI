import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from PIL import Image
import os

IMG_SIZE = 128

# Load trained model
model = load_model("model.h5")

def audio_to_image(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    plt.figure(figsize=(3,3))
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_db = librosa.power_to_db(S, ref=np.max)

    librosa.display.specshow(S_db, sr=sr)
    plt.axis('off')

    temp_img = "temp.png"
    plt.savefig(temp_img, bbox_inches='tight', pad_inches=0)
    plt.close()

    return temp_img

def predict_audio(audio_path):
    img_path = audio_to_image(audio_path)

    img = Image.open(img_path).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0][0]

    os.remove(img_path)

    if prediction > 0.5:
        return "Deepfake Voice", float(prediction)
    else:
        return "Real Voice", float(1 - prediction)


# 🔥 TEST SECTION (YOU CAN CHANGE FILE HERE)

if __name__ == "__main__":
    # Test REAL audio
    result, confidence = predict_audio("../dataset/real/sample1.wav")

    # To test FAKE, comment above line and use below:
    # result, confidence = predict_audio("../dataset/fake/Fsample1.wav")

    print(f"Result: {result}")
    print(f"Confidence: {confidence*100:.2f}%")