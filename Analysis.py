import pandas as pd
import numpy as np 
import librosa
import librosa.display
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
from io import BytesIO

def show_PCG(wav_file):
    data,sr=librosa.load(wav_file, sr=2000)
    plot= librosa.display.waveshow(data, sr=2000)
    plt.title("PCG Signal")
    plt.ylabel('Amplitude')
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf


def show_spectogram(wav_file):
    data,sr=librosa.load(wav_file,sr=2000)
    mel_spectrogram = librosa.feature.melspectrogram(y=data, sr=sr)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 4))
    img = librosa.display.specshow(mel_spectrogram_db, 
                                       x_axis='time', 
                                       y_axis='mel', 
                                       sr=sr, 
                                       cmap='viridis', 
                                       fmax=8000, 
                                       ax=ax)
    cbar = fig.colorbar(img, ax=ax)  
    cbar.set_label('Amplitude (dB)')
    cbar.formatter = ticker.FormatStrFormatter('%+2.0f dB')  # Properly format the colorbar
    cbar.update_ticks()
    ax.set_title("Mel Spectrogram")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf
   
    
     