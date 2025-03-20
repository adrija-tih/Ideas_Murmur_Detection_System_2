import pandas as pd 
import numpy as np
import librosa 
import pickle 
from sklearn.preprocessing import StandardScaler
import time 


#pre-process a signal
def preprocess_signal(signal, cut_duration=1.0, extract_duration=8.0):
    cut_samples = int(cut_duration * 2000)
    trimmed_signal = signal[cut_samples:]

    extract_samples = int(extract_duration * 2000)
    final_signal = trimmed_signal[:extract_samples]

    return final_signal

#function to extract features 
def extract_features(signal, sample_rate, frame_size_ms):
    # Number of samples in each frame
    frame_size_samples = int(sample_rate * frame_size_ms / 1000)
    # Total Number of Frames
    num_frames = len(signal) // frame_size_samples
    feature_vectors = []
    
    for i in range(num_frames):
        frame = signal[i * frame_size_samples:(i + 1) * frame_size_samples]
        
        # Time Domain features
        amplitude_envelope = np.max(np.abs(frame))
        rms_energy = np.sqrt(np.mean(frame ** 2))
        zcr = librosa.feature.zero_crossing_rate(frame, frame_length=len(frame), hop_length=len(frame))[0, 0]
        
        # Frequency Domain Features
        spectral_centroid = librosa.feature.spectral_centroid(y=frame, sr=sample_rate, win_length=len(frame), hop_length=len(frame))[0, 0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=frame, sr=sample_rate, win_length=len(frame), hop_length=len(frame))[0, 0]
        
        spectral_rolloff = librosa.feature.spectral_rolloff(y=frame, sr=sample_rate, roll_percent=0.85)[0, 0]
        
        mfccs = librosa.feature.mfcc(y=frame, sr=sample_rate, n_mfcc=13, fmax=sample_rate / 2).mean(axis=1)
        
        feature_vector = np.hstack([
            amplitude_envelope, rms_energy, zcr, spectral_centroid, spectral_bandwidth,
            spectral_rolloff, mfccs
        ])
        feature_vectors.append(feature_vector)
    
    return np.array(feature_vectors).flatten()
#method_1 for prediction using SVM
def prediction(wav_file):
    pickle_in = open('murmur_classifier.pkl', 'rb') 
    classifier = pickle.load(pickle_in)
    with open('scaling_params.pkl', 'rb') as file:
        scaling_params = pickle.load(file)
    pred=0
    data,sr=librosa.load(wav_file,sr=2000)
    processed_signal = preprocess_signal(data)
    features = extract_features(processed_signal, sample_rate=2000, frame_size_ms=50)
    #scaler = StandardScaler()
    features=np.expand_dims(features, axis=0)
    scaling_params["mean"]=np.expand_dims(scaling_params["mean"],axis=0)
    scaling_params["std"]=np.expand_dims(scaling_params["std"],axis=0)
    features_scaled = (features - scaling_params["mean"]) / scaling_params["std"]
    #features_fit=scaler.fit_transform(features_scaled)
    start_time = time.time()
    pred = classifier.predict(features_scaled)
    end_time = time.time()
    prediction_time = (end_time - start_time)*1000
    return pred,prediction_time


#method for prediction with Random forest
def prediction_1(wav_file):
    pickle_in = open('murmur_classifier_Random_Forest.pkl', 'rb') 
    classifier = pickle.load(pickle_in)
    with open('Random_Forest_classifier_scaling_params.pkl', 'rb') as file:
        scaling_params = pickle.load(file)
    pred=0
    data,sr=librosa.load(wav_file,sr=2000)
    processed_signal = preprocess_signal(data)
    features = extract_features(processed_signal, sample_rate=2000, frame_size_ms=50)
    #scaler = StandardScaler()
    features=np.expand_dims(features, axis=0)
    scaling_params["mean"]=np.expand_dims(scaling_params["mean"],axis=0)
    scaling_params["std"]=np.expand_dims(scaling_params["std"],axis=0)
    features_scaled = (features - scaling_params["mean"]) / scaling_params["std"]
    #features_fit=scaler.fit_transform(features_scaled)
    start_time = time.time()
    pred = classifier.predict(features_scaled)
    end_time = time.time()
    prediction_time = (end_time - start_time)*1000
    return pred,prediction_time