import pyshark
import sys
import json
import numpy as np
import os

# python3 correct_qos1.py X pcap-path solution-path keepalive=(x1,x2)

X = int(sys.argv[1])
pcap_path = sys.argv[2]

# Open saved trace file 
cap = pyshark.FileCapture(pcap_path)

# Open solution file
solution_path = sys.argv[3]
respuestas_json = f'{solution_path}/respuestas-{X}.json'
with open(respuestas_json) as f:
    respuestas = json.load(f)



ok = 0
dups = []
for pkt in cap:
    time = pkt.frame_info._all_fields['frame.time_relative']
    # frame.time_relative

    if pkt.highest_layer != 'MQTT':
        continue

    # print(pkt['TCP']._all_fields)
    # print(len(pkt['TCP']._all_fields['tcp.payload'].split(':')))
    # print(pkt['TCP']._all_fields['tcp.pdu.size'])
    # print([k for k in pkt])

    # It may happen several MQTT headers are stacked inside one TCP payload
    for l,k in enumerate(pkt):
        if 'mqtt.msgtype' not in pkt[l]._all_fields:
            continue

        if pkt[l]._all_fields['mqtt.msgtype'] == '3': # PUBLISH
            # Store the duplicate Message Idx
            if pkt[l]._all_fields['mqtt.dupflag'] in ['1', 'True']:
                dups += [ int(pkt[l]._all_fields['mqtt.msgid']) ]


# Check if all the answered duplicates are in the PCAP
# and check their lengths match
answer = 'duplicates' if sys.argv[4]=='x1' else 'duplicatesx2'
print(sum([rd in dups for rd in respuestas[answer] ]) / len(dups))
#print(int(all([rd in dups for rd in respuestas[answer] ])\
#        and len(respuestas[answer])==len(dups) ))

