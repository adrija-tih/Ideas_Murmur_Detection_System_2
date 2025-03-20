import streamlit_extras
from streamlit_extras.grid import grid
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

import tempfile
import os
from urllib.parse import urlparse
import io

import db
import db_2
import ingestion_gui
import Analysis_gui
import Prediction_gui
import model_gui
# import Time_Series_Analysis_gui
# import ML_Modelling_gui
# import storytelling_gui

db.init_db() #Create the tables and sequences in DuckDB if not present
db_2.init_db()

uploaded_file="wav"


if st.session_state.get('uploaded_file') is None:
    st.session_state['uploaded_file'] = None
    print("Setting st.session_state['uploaded_file'] to None")

if st.session_state.get('uploaded_file_name') is None:
    st.session_state['uploaded_file_name'] = None

# if st.session_state.get('get_description') is None:
#     text_input = st.text_input(
#         "Enter the description",
#         label_visibility=st.session_state.visibility,
#         disabled=st.session_state.disabled,
#         placeholder=st.session_state.placeholder,
#     )

st.set_page_config(page_title="IDEAS Webapp", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

my_grid = grid([4,22,5], [2,5],1, vertical_align="center")

my_grid.image('./IDEAS-TIH_new.jpg', width=200)
my_grid.markdown("<h1 style='text-align: center; color: black;'>Heart Murmur Detection System</h1> <p style='text-align: center; color: black; font-size: 16px;'>Collaborative Project of IDEAS and CSI</p>", unsafe_allow_html=True)
#my_grid.markdown("<h1 style='text-align: center; color: black;'>Collaborative Project of IDEAS and CSI </h1>", unsafe_allow_html=True)
my_grid.image('./CSI_new.jpg',width=200)

# Row 1:
with my_grid.container(height=640, border=True):  #Menu

    selected = option_menu(None, ["Ingestion", "Analysis", "Prediction", "Models"], icons=['database-add','bar-chart-steps', 'box'])
    # if selected=="Time Series Analysis":
    #     sel1=option_menu(None,["ARIMA","ARIMAX"])
    # if selected=="ML Modelling":
    #     sel2= option_menu(None,["SVR","RF"])    
body = my_grid.container(height=640, border=True)  #Main body



# Row 2:
# with my_grid.container(height=640, border=True):  #Menu

#     selected = option_menu(None, ["Ingestion", "Analysis", "Prediction", "Models"], icons=['database-add','bar-chart-steps', 'box'])
#     # if selected=="Time Series Analysis":
#     #     sel1=option_menu(None,["ARIMA","ARIMAX"])
#     # if selected=="ML Modelling":
#     #     sel2= option_menu(None,["SVR","RF"])    
# body = my_grid.container(height=640, border=True)  #Main body

# Row 3 - Footer:
my_grid.markdown("<h2 style='text-align: center; color: black;'> &#169;IDEAS-TIH </h2>", unsafe_allow_html=True)  #&#169; HTML code for copyright emoji


with body:
    if selected == "Ingestion":
        ingestion_gui.ingestion_gui()                        
            # if st.session_state['uploaded_file_name'] is not None:
            #     st.write("Uploaded File Name: ", st.session_state['uploaded_file_name'])

    if selected == "Analysis":
        Analysis_gui.Analysis_gui()
    
    if selected=="Prediction":
        Prediction_gui.Prediction_gui()

    if selected == "Models":
        model_gui.model_gui()

#     if selected == "ML Modelling":
#         ML_Modelling_gui.ML_Modelling_gui()

#     if selected == "Storytelling":
#         storytelling_gui.storytelling_gui()