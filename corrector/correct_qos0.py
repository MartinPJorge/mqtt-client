import pyshark
import sys
import json
import numpy as np
import os

# python3 correct_qos0.py X pcap-path solution-path log-path

X = int(sys.argv[1])
pcap_path = sys.argv[2]

# Open saved trace file 
cap = pyshark.FileCapture(pcap_path)

# Open solution file
solution_path = sys.argv[3]
respuestas_json = f'{solution_path}/respuestas-{X}.json'
with open(respuestas_json) as f:
    respuestas = json.load(f)

# Inspect log
# get successfully sent PUBLISH according to client
# get ERR sent PUBLISH according to client (due to no connection)
log_path = sys.argv[4]
succ = []
err = []
with open(log_path, 'r') as file:
    for line in file:
        if 'SUCC' in line:
            succ += [ int(line.split(',')[-1][1:-2]) - 1 ]
        elif 'NO_CONN' in line:
            err += [ int(line.split(',')[-1][1:-2]) - 1 ]




ok = 0
pings = []
pcap_sent = []
for pkt in cap:
    time = pkt.frame_info._all_fields['frame.time_relative']
    # frame.time_relative

    if pkt.highest_layer != 'MQTT':
        continue

    if pkt[pkt.highest_layer]._all_fields['mqtt.msgtype'] == '3': # PUBLISH

        # Get the PUBLISH payload as string
        # https://stackoverflow.com/a/66073701
        hex_string = str(pkt[pkt.highest_layer]._all_fields['mqtt.msg'])
        hex_split = hex_string.split(':')
        hex_as_chars = map(lambda hex: chr(int(hex, 16)), hex_split)
        human_readable = ''.join(hex_as_chars)

        # Store the published index
        report_idx = human_readable.split(',')[0]
        pcap_sent += [int(report_idx)]


# Obtain not detected losses
not_detected_losses = [idx for idx in succ if idx not in pcap_sent]


# Check if answers miss some PUBLISH Idx
ok_perdidas_cliente = 0 if any([idx not in respuestas['perdidascliente']\
        for idx in err]) else 1
ok_perdidas = 0 if any([idx not in respuestas['perdidas']\
        for idx in not_detected_losses+err]) else 1

print(ok_perdidas_cliente)
print(ok_perdidas)

