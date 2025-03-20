import pandas as pd
import streamlit as st
from streamlit_extras.grid import grid
import db_2
import os 
import io
import time
import pickle

def init(): #added so that session variables get initialised
    st.session_state['model_file_content'] = 'Dummy content'
    st.session_state['model_file_name'] = None
    st.session_state['mime_type'] = None

def model_gui():
    init()
    colT1,colT2 = st.columns([1,8])
    with colT2:
        st.write("**Currently available models**")  #** for bold
        
    data_grid = grid([1], vertical_align="centre")
    container = data_grid.container()
    with container:
        ph = st.empty()
        dataset_df = db_2.get_models()
        dataset_df.insert(0, 'Select', False)
        selection = ph.data_editor(dataset_df, height=300,hide_index=True, column_config={"Select": st.column_config.CheckboxColumn(help="Select only one model"), "model_id":"Model ID", "file_name": "File Name", "mime_type": "File Type", "file_size": "File Size in bytes","description":"DESCRIPTION","date_created": "Data Uploaded"})
        st.session_state['selection'] = selection
        message = st.empty()
        #put_selected_file_details_in_sesion()

        if st.button("Delete selected models", type="primary"):
            selection = st.session_state['selection']           
            checkedBoxes = selection['Select'].tolist()

            if True in checkedBoxes:
                model_id = selection['model_id'].tolist()[checkedBoxes.index(True)]
                result=db_2.delete_models(model_id)
                model_file_name = selection['file_name'].tolist()[checkedBoxes.index(True)]
                db_2.delete_model_file(model_file_name)
                message.success("model deleted")
                time.sleep(1)
                message.empty() 
                model_df=db_2.get_models()                 
                model_df.insert(0, 'Select',False)
                ph.data_editor(model_df, hide_index=True, column_config={"Select": st.column_config.CheckboxColumn(help="Select only one model"), "model_id":"Model ID", "file_name": "File Name", "mime_type": "File Type", "file_size": "File Size in bytes","title":"TITLE","date_created": "Data Uploaded"})
 
        if st.download_button(label="Download selected Model", data=st.session_state['model_file_content'], mime=st.session_state['mime_type'], file_name=st.session_state['model_file_name']):
                message.success("Model downloaded")
                time.sleep(1)
                message.empty()                  


        file = st.tabs(["Upload local file"])
    
       
        with st.form("upload-form", clear_on_submit=True):
            uploaded_file = st.file_uploader("Model Uploader",type=['pkl'])
            title = st.text_area("Enter a title for the model")
            submitted = st.form_submit_button("UPLOAD MODEL")
                                    
        if submitted and uploaded_file is not None:
               
            file_name = uploaded_file.name
            st.session_state['model_file_name'] = file_name
            file_size = uploaded_file.size
            mime_type = 'application/octet-stream'
            if uploaded_file.type=="application/octet-stream":
                    st.session_state['mime_type']='application/octet-stream'
                    mime_type='octet-stream'
                    pickle.loads(uploaded_file.read())
                    uploaded_file.seek(0)
                    uploaded_file_bytes=uploaded_file.read()
            else:
                    print("please upload pkl file")
                           
            fileBytes = uploaded_file_bytes
                             
            file_path = os.path.join("model_files/", uploaded_file.name)
            with open(file_path, "wb") as f:
                  f.write(uploaded_file.getbuffer())
            st.session_state['uploaded_file'] = uploaded_file
            st.session_state['uploaded_file_name'] = uploaded_file.name
            result=db_2.insert_models(file_name, mime_type,file_size,fileBytes,title)
                #result = db.insert_dataset(fileName, fileBytes, mime_type, fileSize,description)
            dataset_df = db_2.get_models() #connection.execute('SELECT dataset_id, file_name, date_created from datasets').df()
            dataset_df.insert(0, 'Select',False)
            ph.data_editor(dataset_df, hide_index=True, column_config={"Select": st.column_config.CheckboxColumn(help="Select only one dataset"),"model_id":"Model ID", "file_name": "File Name", "mime_type": "File Type", "file_size": "File Size in bytes","title":"TITLE","date_created": "Data Uploaded" })
            