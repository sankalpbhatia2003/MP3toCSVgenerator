import pandas as pd
import json
from deepgram_file import data

i = 0
print("ORIGINAL DF...")
print(data)

while i < len(data['statement']):
    if ((data['stop'][i] > data['start'][i]) and ((data['stop'][i] - data['start'][i]) > 1)):
        pass
    else:
        #data = data.drop(data.index[(data['stop'][i] == data['stop'][i])],axis=0,inplace=True)
        data = data.drop(labels=i, axis=0)
    i += 1

print("EDITED DF...")
print(data)

data = data.reset_index(inplace=False)

i = 1
while i < len(data['statement']):
    if (data['start'][i] < data['stop'][i-1]):
        data['start'][i] = data['stop'][i-1]
    else:
        pass
    i += 1

print('')

data['type'][0] = "CALIBRATION"
data['type'][1:len(data)] = "ANALYSIS"

print("PRINTING DATA FROM EDITFRAME FILE...")
print(data)

df = data