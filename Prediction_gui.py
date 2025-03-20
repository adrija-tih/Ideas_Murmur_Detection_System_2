import streamlit as st
from streamlit_extras.grid import grid 
import db
import os
from pydub import AudioSegment
import io

import Prediction
import db_2


def get_insights(dataset_file_name,dataset_df):
    Prediction_grid = grid([1], vertical_align="centre")
    with Prediction_grid.container():
        #tab1,tab2=st.tabs(['PCG','MFCC'])  
        base_path = "dataset_files/"
        full_path=os.path.join(base_path,dataset_file_name)
        Pred=Prediction.prediction(full_path)
        res=int(Pred[0])
        if res==0:
            st.text_area("Prediction Result is:","Normal subject")
        else:
            st.text_area("Prediction Result is:","Murmur subject")
        st.text_area("Prediction time taken in millisecond",Pred[1])  

def get_insights_1(dataset_file_name,dataset_df):
    Prediction_grid = grid([1], vertical_align="centre")
    with Prediction_grid.container():
        #tab1,tab2=st.tabs(['PCG','MFCC'])  
        base_path = "dataset_files/"
        full_path=os.path.join(base_path,dataset_file_name)
        Pred=Prediction.prediction_1(full_path)
        print(Pred)
        res=Pred[0]
        if res==0:
            st.text_area("Prediction Result is:","Normal subject")
        else:
            st.text_area("Prediction Result is:","Murmur subject")
        st.text_area("Prediction time taken in millisecond",Pred[1])  

              

def Prediction_gui():
    dataset_df = db.get_datasets_1()
    dataset_df_1=db_2.get_models()
    dataset_file_name = None
    dataset_file_name = st.selectbox('Select an audio file',dataset_df['file_name'].tolist(), index=None, placeholder="Select an audio file...")
    if dataset_file_name is not None:
        model_name=st.selectbox('Select a model',dataset_df_1['title'].tolist(),index=None,placeholder="Select a model")
        pred_button=st.button("Perform Prediction on audio file",use_container_width=True)
        model_type=dataset_df_1['title'].tolist()
        if model_name == model_type[0] and pred_button:
            get_insights(dataset_file_name,dataset_df)
        elif model_name==model_type[1] and pred_button:
            get_insights_1(dataset_file_name,dataset_df)
        
        
        