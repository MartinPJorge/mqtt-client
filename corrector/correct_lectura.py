import sys
solution_path = sys.argv[2]
sys.path.append(solution_path)
import utils
import json
from math import ceil


# python3 correct_lectura.py X path
X = int(sys.argv[1])
LAST_LINE = X
num_lines = ceil(X/2)
lines = utils.read_report(
        'Human_vital_signs_R.csv', LAST_LINE, num_lines)

# respuestas-X.json
lectura_json = f'{solution_path}/respuestas-{X}.json'
with open(lectura_json) as f:
    respuestas = json.load(f)


# How many lines were correctly printed
print(int(sum([l in respuestas['lectura'] for l in lines])\
        / len(respuestas['lectura'])))


