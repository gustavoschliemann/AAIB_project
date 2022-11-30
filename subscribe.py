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

#MQTT configuration

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic = "AAIB/project"

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
    print('chegou')
    np_message = np.array(ast.literal_eval(msg.payload.decode()[1:-1]))
    #np_message = np.frombuffer(msg.payload.decode('unicode-escape').encode('ISO-8859-1')[2:-1], dtype='float32')
    print(np_message)
    with placeholder2.container():
        st.write('Finished recording')
        st.write('Processing...')
        st.write(np_message)
        display(np_message)
    
    
def subscribe():  
    client.subscribe(topic)
    client.on_message = on_message
    print('Subscribing')
    client.loop_forever()

def display(data):
    #fs = 1024
    #t = data.shape[0] / fs
    fig, ax = plt.subplots()
    #x = np.arange(0,t,1/fs)
    #y = data.mean(data, axis=0)
    ax.plot(data)
    st.pyplot(fig)


def mqtt_thread():
    for i in range(60):
        if 'mqttThread' not in st.session_state:
            st.session_state.mqttThread = threading.Thread(target=subscribe)
            add_script_run_ctx(st.session_state.mqttThread)
            st.session_state.mqttThread.start()
            
        time.sleep(1)
    del st.session_state['mqttThread']


#def convert_csv(data_):
    #file = open("values.csv")
    #reader = csv.reader(file)
    #sample = len(list(reader))
    #sample+=1
    #with open('values.csv', mode='a', newline='') as csv_file:
        #csv_file_writer = csv.writer(csv_file, delimiter= ',')
        #csv_file_writer.writerow(data_)

def headers():
    try:
        with open('values.csv', 'r') as csv_file:
            pass
    except:       
         with open('values.csv', mode ='w', newline='') as csv_file:
            fieldnames = ['sample','valor']
            writer = csv.DictWriter(csv_file, fieldnames= fieldnames)
            writer.writeheader()

client = connect_mqtt()
headers()

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
            client.publish(topic,'Start')
            st.write('Started recording...')
            placeholder2 = st.empty()
            mqtt_thread()

    with col2:
        if st.button('Download', key='down'):
            st.write(var)
        #st.download_button(
            #label="Download",
            #data=convert_df(data),
            #file_name='large_df.csv',
            #mime='text/csv',
        #) 