import pandas as pd
import duckdb
import streamlit as st
import os


connection = None

def init_db():
    if 'connection' not in st.session_state:
        connection = duckdb.connect("Murmur_db.db")
        st.session_state['connection'] = connection
        connection.execute('CREATE SEQUENCE IF NOT EXISTS "seq_dataset_id" START 1')
        connection.execute("CREATE TABLE IF NOT EXISTS datasets (dataset_id integer primary key default nextval('seq_dataset_id'), file_name varchar(1000) unique, mime_type varchar(1000),file_size integer, audio_data BLOB,description varchar(1000),date_created datetime)")
       
        print(connection.execute("SHOW TABLES").df())

def get_datasets():
    if 'connection' in st.session_state:
        connection = st.session_state['connection'] 
    return connection.execute("SELECT dataset_id, file_name, mime_type,file_size, date_created,description from datasets").df()

def get_datasets_1():
    if 'connection' in st.session_state:
        connection = st.session_state['connection'] 
    return connection.execute("SELECT dataset_id, file_name, mime_type,file_size, date_created,audio_data,description from datasets").df()

def delete_dataset(dataset_id):
    if 'connection' in st.session_state:
        connection = st.session_state['connection'] 
    return connection.execute('DELETE FROM datasets where dataset_id=?', [dataset_id])

def delete_dataset_file(file_name):
    if os.path.exists("dataset_files/" + file_name):
        os.remove("dataset_files/" + file_name)
    if os.path.exists("Converted_dataset_files/"+"converted_"+file_name):
        os.remove("Converted_dataset_files/"+"converted_"+file_name)
    else:
        print("The dataset file does not exist")

def get_dataset_file(dataset_file_name):
    path = "dataset_files/" + dataset_file_name
    print(path)
    if os.path.exists(path):
        #os.read("dataset_files/" + dataset_file_name)
        f = open(path, mode="rb")
        data = f.read()
        return data
    else:
        print("The dataset file does not exist")


def insert_dataset(fileName, fileBytes, mime_type,fileSize,description):
    dir = "dataset_files"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    new_folder_path = os.path.join(current_dir, dir)
    path = os.path.join(new_folder_path, fileName)
    if not os.path.isfile(new_folder_path):
        os.makedirs(new_folder_path, exist_ok=True)
    with open(path, "wb") as f:
        f.write(fileBytes)
    if 'connection' in st.session_state:
        connection = st.session_state['connection'] 
    return connection.execute("INSERT INTO datasets VALUES (nextval('seq_dataset_id'), ?, ?, ?, ?,?,get_current_timestamp())", [fileName,mime_type, fileSize,fileBytes,description])
    #return connection.execute(f"INSERT INTO datasets VALUES (nextval('seq_dataset_id'), ?, get_current_timestamp()), {fileBytes}::blob" , [fileName])

def load_df_from_parquet(dataset_file_name, preprocess = False):
    print(dataset_file_name)
    dir = "dataset_files"
    path = os.path.join(dir, dataset_file_name)
    with open(path, "rb") as f:
        df = pd.read_parquet(f)
    if preprocess:
        df = df.dropna().drop_duplicates().reset_index(drop = True)

    return df

def get_dataset_id_from_dataset_file_name(file_name):
    if 'connection' in st.session_state:
        connection = st.session_state['connection']
    return connection.execute("SELECT dataset_id from datasets where file_name = ?", [file_name]).df().iloc[0]["dataset_id"].item()






    




