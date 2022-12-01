from paho.mqtt import client as mqtt_client
import threading
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
import ast
import librosa
import librosa.display
import json
import pandas as pd

#MQTT configuration

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic_sub = "AAIB/project/sub"
topic_start = "AAIB/project/pub"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    np_data = np.array(data)
    with placeholder2.container():
        st.write('Finished recording')
        st.write('Processing...')
        display(np_data)
        #download(np_data)
    if 'download' not in st.session_state:
        st.session_state.download = np_data
        #download(np_data)
        #st.session_state.download = threading.Thread(target=download, args=(1,))
        #add_script_run_ctx(st.session_state.download)
        #st.session_state.download.start()
        
    
def subscribe():  
    client.subscribe(topic_sub)
    client.on_message = on_message
    print('Subscribing')
    client.loop_forever()

def display(data):
    FRAME_SIZE = 512
    HOP_SIZE = 128
    fs = 22050

    fig, ax = plt.subplots()
    imgdb = librosa.display.specshow(data,sr=fs,hop_length=HOP_SIZE,n_fft=FRAME_SIZE, y_axis='log', x_axis='time', ax=ax)
    ax.set(title='Log-Power spectrogram')
    fig.colorbar(imgdb, ax=ax, format="%+2.0f dB")
    st.pyplot(fig)

@st.cache
def convert_df(df):

    return df.to_csv().encode('utf-8')

def mqtt_thread():
    for i in range(8):
        if 'mqttThread' not in st.session_state:
            st.session_state.mqttThread = threading.Thread(target=subscribe)
            add_script_run_ctx(st.session_state.mqttThread)
            st.session_state.mqttThread.start()
            
        time.sleep(1)
    del st.session_state['mqttThread']

client = connect_mqtt()

#Streamlit Frontend

st.title("Real-Time Audio Recorder using Paho MQTT")
st.write(
    'This is a project developed for the subject of AIIB at FCT-UNL'
)

placeholder = st.empty()

with placeholder.container():

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Record', key='rec'):
            client.publish(topic_start,'Start')
            st.write('Started recording...')
            placeholder2 = st.empty()
            mqtt_thread()

    with col2:
        if 'download' in st.session_state:
            df = pd.DataFrame(data = st.session_state.download)
            csv= convert_df(df)
            #st.write(csv)
            st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='data.csv',
            mime='text/csv',
        )
            