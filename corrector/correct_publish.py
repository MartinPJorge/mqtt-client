import pyshark
import sys
import json
import numpy as np

# python3 correct_publish.py X pcap-path solution-path

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
pings = []
for pkt in cap:
    time = pkt.frame_info._all_fields['frame.time_relative']
    # frame.time_relative

    if pkt[pkt.highest_layer]._all_fields['mqtt.msgtype'] == '3': # PUBLISH

        # Get the PUBLISH payload as string
        # https://stackoverflow.com/a/66073701
        hex_string = str(pkt[pkt.highest_layer]._all_fields['mqtt.msg'])
        hex_split = hex_string.split(':')
        hex_as_chars = map(lambda hex: chr(int(hex, 16)), hex_split)
        human_readable = ''.join(hex_as_chars)

        # Check if it matches the required one
        report_idx = human_readable.split(',')[0]
        if report_idx == (X % 5) + 1:
            ok += 1 if report_idx in str(solucion['instantemuestraX']) else 0



    if pkt[pkt.highest_layer]._all_fields['mqtt.msgtype'] == '12': # PING REQ
        pings += [float(time)]


# OK PING interval?
mean_ping = np.mean([p2-p1 for p1,p2 in zip(pings[:-1], pings[1:])])
#print('mean ping', mean_ping)
ok += 1 if abs(respuestas['tiempopings'] - mean_ping) / mean_ping < 0.1 else 0
#print(abs(respuestas['tiempopings'] - mean_ping) / mean_ping)


print(ok)
print(int(respuestas['ackmessagetype'] in [2, '2']))






