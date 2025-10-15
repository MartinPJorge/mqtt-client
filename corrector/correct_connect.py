import pyshark
import sys
import json

# python3 correct_connect.py X pcap-path solution-path

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
for pkt in cap:
    # Check that the highest layer is an MQTT msg
    if not any(['mqtt' in p for p in pkt[pkt.highest_layer]._all_fields]):
        continue

    if pkt[pkt.highest_layer]._all_fields['mqtt.msgtype'] == '1':
        clientid = pkt[pkt.highest_layer]._all_fields['mqtt.clientid']
        ok += 1 if clientid == respuestas['clientid'] else 0


print(ok)
print(int(respuestas['ackmessagetype'] in [2, '2']))






