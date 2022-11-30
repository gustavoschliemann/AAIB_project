from paho.mqtt import client as mqtt_client
import numpy as np
import librosa
import threading
import time
import sounddevice as sd

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

def publish(msg):
    result = client.publish(topic,msg)
    msg_status = result[0]
    if msg_status ==0:
        print(f"Message sent to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")

def on_message(client, userdata, msg):
    if str(msg.payload.decode('latin1')) == 'Start':
        audio_rec()
        
def subscribe():  
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()

def audio_rec():
    FRAME_SIZE = 512
    HOP_SIZE = 128
    duration = 5  #seconds
    fs = 1024
    #print("Recording...")
    #record = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    #sd.wait()
    #print("Finished")
    #S = np.abs(librosa.stft(record.astype('float32'), n_fft = FRAME_SIZE, hop_length= HOP_SIZE)) ** 2
    #print(np.shape(S.transpose()[0].transpose()))
    #print(S.transpose()[0])
    #Y_scale_send = [[str(element) for element in index]for index in Y_scale]
    #publish(str(S.tolist()))
    publish('ola')

client = connect_mqtt()  

sub=threading.Thread(target=subscribe)
pub=threading.Thread(target=publish, args=(1,))
sub.start()