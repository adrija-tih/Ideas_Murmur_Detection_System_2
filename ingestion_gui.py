import pandas as pd
import streamlit as st
from streamlit_extras.grid import grid
import time
import urllib.request
import os
import db
import io
from pydub import AudioSegment


def init(): #added so that session variables get initialised
    st.session_state['dataset_file_content'] = 'Dummy content'
    st.session_state['dataset_file_name'] = None
    st.session_state['mime_type'] = None

def put_selected_file_details_in_sesion():
    selection = st.session_state['selection']
    checkedBoxes = selection['Select'].tolist()
    if True in checkedBoxes:
        dataset_file_name = selection['file_name'].tolist()[checkedBoxes.index(True)]
        mime_type = "audio/wav"
        df = db.get_dataset_file(dataset_file_name)
        st.session_state['dataset_file_content'] = df
        st.session_state['dataset_file_name'] = dataset_file_name
        st.session_state['mime_type'] = mime_type


def ingestion_gui():
    init()
    colT1,colT2 = st.columns([1,8])
    with colT2:
        st.write("**Currently available audio files**")  #** for bold
        
    data_grid = grid([1], vertical_align="centre")
    container = data_grid.container()
    with container:
        ph = st.empty()
        dataset_df = db.get_datasets()
        dataset_df.insert(0, 'Select', False)
        selection = ph.data_editor(dataset_df, height=300,hide_index=True, column_config={"Select": st.column_config.CheckboxColumn(help="Select only one dataset"), "dataset_id":"Audio File ID", "file_name": "File Name", "mime_type": "File Type", "file_size": "File Size in bytes", "date_created": "File Uploaded","description":"Description"})
        st.session_state['selection'] = selection
        message = st.empty()
        put_selected_file_details_in_sesion()

        if st.button("Delete selected file", type="primary"):
            selection = st.session_state['selection']           
            checkedBoxes = selection['Select'].tolist()

            if True in checkedBoxes:
                dataset_id = selection['dataset_id'].tolist()[checkedBoxes.index(True)]
                result = db.delete_dataset(dataset_id)
                    #print(result)
                dataset_file_name = selection['file_name'].tolist()[checkedBoxes.index(True)]
                db.delete_dataset_file(dataset_file_name)
                message.success("File deleted")
                time.sleep(1)
                message.empty()                  
                dataset_df = db.get_datasets()
                dataset_df.insert(0, 'Select',False)
                ph.data_editor(dataset_df, hide_index=True, column_config={"Select": st.column_config.CheckboxColumn(help="Select only one dataset"), "dataset_id":"Dataset ID", "file_name": "File Name", "mime_type": "File Type", "file_size": "File Size in bytes", "date_created": "Data Uploaded"})

        if st.download_button(label="Download selected file", data=st.session_state['dataset_file_content'], mime=st.session_state['mime_type'], file_name=st.session_state['dataset_file_name']):
                message.success("file downloaded")
                time.sleep(1)
                message.empty()                  


        file,url = st.tabs(["Upload local file","Load from URL"])
                        
        with file:
            with st.form("upload-form", clear_on_submit=True):
                uploaded_file = st.file_uploader("FILE UPLOADER",type = ['wav'])
                description = st.text_area("Enter a description for the audio file")
                submitted = st.form_submit_button("UPLOAD AUDIO FILES")
                                    
            if submitted and uploaded_file is not None:
                fileName = uploaded_file.name
                st.session_state['dataset_file_name'] = fileName
                fileSize = uploaded_file.getvalue().__sizeof__()
                mime_type='wav'
                if uploaded_file.type == "audio/wav":
                    st.session_state['mime_type'] = 'audio/wav'
                    mime_type = 'wav'
                    print(type(uploaded_file))
                    
                    audio_data = uploaded_file.read()
                else:
                                      
                    print("please upload wav file")
                
                fileBytes = audio_data
                #print(type(fileBytes))
                # result = db.save_df_as_table(data_df,fileName)
                file_path = os.path.join("dataset_files/", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.session_state['uploaded_file'] = uploaded_file
                st.session_state['uploaded_file_name'] = uploaded_file.name
                result = db.insert_dataset(fileName, fileBytes, mime_type, fileSize,description)
                dataset_df = db.get_datasets() #connection.execute('SELECT dataset_id, file_name, date_created from datasets').df()
                dataset_df.insert(0, 'Select',False)
                ph.data_editor(dataset_df, hide_index=True, column_config={"Select": st.column_config.CheckboxColumn(help="Select only one dataset"), "dataset_id":"Dataset ID", "file_name": "File Name", "mime_type": "File Type", "file_size": "File Size in bytes", "date_created": "Date Uploaded","description": "Description" })
                
        # with url:
        #     with st.form("url-form", clear_on_submit=True):
        #         url_input = st.text_input("Enter URL 👇")
        #         submitted = st.form_submit_button("LOAD DATASET")

        #     if submitted and url_input is not None:
        #         response = urllib.request.urlopen(url_input, headers={'User-Agent': 'Mozilla/5.0'})
        #         fileSize = response.info().get('Content-Length', 0)
        #         st.session_state['mime_type'] =response.info().get('Content-Type', "text/csv")
        #         if st.session_state['mime_type'] =='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        #             mime_type = "Excel"
        #         else:
        #             mime_type = "CSV"

        #         #data_df = pd.read_csv(url_input)
        #         urlPath = urllib.parse.urlparse(url_input)
        #         fileName = os.path.basename(urlPath.path)
        #         fileBytes = audio_data.to_parquet()
        #         result = db.insert_dataset(fileName, fileBytes, mime_type, fileSize)
        #         dataset_df = db.get_datasets()
        #         dataset_df.insert(0, 'Select',False)
        #         ph.data_editor(dataset_df, hide_index=True, column_config={"Select": st.column_config.CheckboxColumn(help="Select only one dataset"), "dataset_id":"Dataset ID", "file_name": "File Name", "mime_type": "File Type", "file_size": "File Size in bytes", "date_created": "Date Uploaded"})