import streamlit as st
from streamlit_extras.grid import grid 
import db
import Analysis
import io
import os
import glob
import subprocess

dataset_file_name = None 


def get_insights(dataset_file_name,dataset_df):
    Analysis_grid = grid([1], vertical_align="centre")
    with Analysis_grid.container():
        #tab1,tab2=st.tabs(['PCG','MFCC'])  
        base_path = "dataset_files/"
        full_path=os.path.join(base_path,dataset_file_name)
        plot=Analysis.show_PCG(full_path)
        plot_1=Analysis.show_spectogram(full_path)
        st.image(plot)
        st.write("<b>Description:</b>","Phonocardiography(PCG) is the graphical representation heart sounds and murmurs.It is a two dimensional plot of heart sound intensity over time.",unsafe_allow_html=True)
        st.image(plot_1)
        st.write("<b>Description:</b>","Mel spectrogram represents sound as 2D image,the color intensity shows how loud each frequency is at any given time.",unsafe_allow_html=True) 


def Analysis_gui():
    dataset_df = db.get_datasets_1()
    print(dataset_df)
    dataset_file_name = None
    dataset_file_name = st.selectbox(
        'Select an audio_file',dataset_df['file_name'].tolist(), index=None, placeholder="Select an audio file...")
    visualize,feature,audio_display=st.tabs(["Visualize audio file","Feature Description","Listen to the audio file"])
    with visualize:
        if dataset_file_name is not None:
            get_insights(dataset_file_name,dataset_df)
            
            #st.text_area("")
    with feature:
        if dataset_file_name is not None:
            st.image("Feature_description.png")
            st.image("output.png")
            
    with audio_display:
        if dataset_file_name is not None:
            file_path = os.path.join("dataset_files/",dataset_file_name)
            output_file_path=os.path.join("Converted_dataset_files/", "converted_" + os.path.splitext(dataset_file_name)[0] + ".wav")
            subprocess.run([
            "ffmpeg",
            "-i", file_path,        
            "-c:a", "pcm_s16le",     
            "-ar", "44100",          
            "-ac", "2",              
            output_file_path], check=True)
            st.audio(output_file_path, format="audio/mpeg")