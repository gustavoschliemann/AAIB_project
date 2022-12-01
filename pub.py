from paho.mqtt import client as mqtt_client
import numpy as np
import librosa
import threading
import sounddevice as sd
import json

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

def publish(msg):
    result = client.publish(topic_sub,msg)
    msg_status = result[0]
    if msg_status ==0:
        print(f"Message sent to topic {topic_sub}")
    else:
        print(f"Failed to send message to topic {topic_sub}")

def on_message(client, userdata, msg):
    if str(msg.payload.decode('latin1')) == 'Start':
        audio_rec()
        
def subscribe():  
    client.subscribe(topic_start)
    client.on_message = on_message
    client.loop_forever()
    
# adjustments made to the recording to fit the librosa.stft format on line 53

def audio_rec():
    FRAME_SIZE = 2048
    HOP_SIZE = 512
    duration = 5  #seconds
    fs = 22050
    print("Recording...")
    record = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Finished")
    S = np.abs(librosa.stft(record.transpose()[0].astype('float32'), n_fft = FRAME_SIZE, hop_length= HOP_SIZE))
    power = librosa.power_to_db(S**2, ref=np.max)
    msg = json.dumps(power.tolist())
    publish(msg)

client = connect_mqtt()  

sub=threading.Thread(target=subscribe)
sub.start()