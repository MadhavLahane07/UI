import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def convert_to_spectrogram(input_folder, output_folder):
    # Create output folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if file.endswith(".wav"):
            file_path = os.path.join(input_folder, file)
            
            # Load audio
            y, sr = librosa.load(file_path, sr=None)
            
            # Create spectrogram
            plt.figure(figsize=(3, 3))
            S = librosa.feature.melspectrogram(y=y, sr=sr)
            S_db = librosa.power_to_db(S, ref=np.max)
            
            librosa.display.specshow(S_db, sr=sr)
            
            # Remove axes
            plt.axis('off')
            
            # Save image
            output_file = os.path.join(output_folder, file.replace(".wav", ".png"))
            plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
            plt.close()

# Convert both real and fake datasets
convert_to_spectrogram("../dataset/real", "../spectrograms/real")
convert_to_spectrogram("../dataset/fake", "../spectrograms/fake")

print("✅ Spectrograms generated successfully!")