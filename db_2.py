import pandas as pd
import duckdb
import streamlit as st
import os

connection = None

def init_db():
    if 'connection_1' not in st.session_state:
        connection = duckdb.connect("model.db")
        st.session_state['connection_1'] = connection
        connection.execute('CREATE SEQUENCE IF NOT EXISTS "seq_model_id" START 1')
        connection.execute("CREATE TABLE IF NOT EXISTS models (model_id integer primary key default nextval('seq_model_id'), file_name varchar(1000) unique, mime_type varchar(1000),file_size integer,model_data BLOB,title varchar(1000),uploaded_on datetime)")
       
        print(connection.execute("SHOW TABLES").df())

def get_models():
    if 'connection_1' in st.session_state:
        connection = st.session_state['connection_1'] 
    return connection.execute("SELECT model_id, file_name, mime_type,file_size,title,uploaded_on from models").df()    


def delete_models(model_id):
    if 'connection_1' in st.session_state:
        connection = st.session_state['connection_1'] 
    return connection.execute('DELETE FROM models where model_id=?', [model_id])

def delete_model_file(model_name):
    if os.path.exists("model_files/" + model_name):
        os.remove("model_files/" + model_name)
    else:
        print("The model file does not exist")

def get_dataset_file(model_name):
    path = "model_files/" + model_name
    print(path)
    if os.path.exists(path):
        #os.read("dataset_files/" + dataset_file_name)
        f = open(path, mode="rb")
        data = f.read()
        return data
    else:
        print("The model file does not exist")


def insert_models(fileName, mime_type,fileSize,fileBytes,title):
    dir = "model_files"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    new_folder_path = os.path.join(current_dir, dir)
    path = os.path.join(new_folder_path, fileName)
    if not os.path.isfile(new_folder_path):
        os.makedirs(new_folder_path, exist_ok=True)
    with open(path, "wb") as f:
        f.write(fileBytes)
    if 'connection_1' in st.session_state:
        connection = st.session_state['connection_1'] 
    return connection.execute("INSERT INTO models VALUES (nextval('seq_model_id'), ?, ?, ?, ?,?,get_current_timestamp())", [fileName,mime_type,fileSize,fileBytes,title])