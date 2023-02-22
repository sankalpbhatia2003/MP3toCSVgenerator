import pandas as pd
import json

df = pd.read_csv('audio.csv')
try:
    df = df.reset_index(inplace=False)
except:
    pass

try:
    df = df.drop(['Unnamed: 0'], axis=1)
except:
    pass

try:
    df = df.drop(['level_0'], axis=1)
except:
    pass

try:
    df = df.drop(['index'], axis=1)
except:
    pass

json_data = df.to_json(orient ='records' , indent=4)

my_dict = {}
my_dict["statements"] = json.loads(json_data)

# Writing to audio.json
with open('audio.json', "w") as outfile:
    json.dump(my_dict, outfile)

outfile.close()
