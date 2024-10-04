import time
import pandas as pd
import random
import time
from paho.mqtt import client as mqtt_client
from utils import read_report









FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

#def on_disconnect(client, userdata, rc):
def on_disconnect(client, userdata, flags, rc, properties):
    print("Disconnected with result code: %s", rc, flush=True)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        print("Reconnecting in %d seconds...", reconnect_delay, flush=True)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            print("Reconnected successfully!", flush=True)
            return
        except Exception as err:
            print("%s. Reconnect failed. Retrying...", err, flush=True)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    print("Reconnect failed after %s attempts. Exiting...", reconnect_count, flush=True)







broker = None # TODO
port = None # TODO
topic = None # TODO
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

def connect_mqtt():
    #def on_connect(client, userdata, flags, rc):
    def on_connect(client, userdata, flags, rc, properties):
    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    # def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!", flush=True)
        else:
            print(f"Failed to connect, return code {rc}\n", flush=True)
    # Set Connecting Client ID
    #client = mqtt_client.Client(client_id)

    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    client = mqtt_client.Client(client_id=client_id,
            callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
            clean_session=False)

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker, port, keepalive=10) # TODO
    return client





def publish(client):
    msg_count = 1


    #############################
    # VITAL SIGNS AUX VARIABLES #
    #############################
    # Fill here with necessary auxiliary variables
    # TODO


    while True:
        time.sleep(5)

        ######################
        ## READ VITAL SIGNS ##
        ######################

        print(FIRST_RECONNECT_DELAY, flush=True)
        # TODO: read next line(s) and store in "lines"
        lines = None # TODO
        # TODO: missing code to keep track of last read line

        lines = ';'.join(lines)

        msg = f"messages: {msg_count}" # SOL
        msg = lines
        result = client.publish(topic, msg, qos=0)
        print('result', flush=True)
        print(result, flush=True)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`", flush=True)
        else:
            print(f"Failed to send message to topic {topic}", flush=True)
        msg_count += 1






def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()






