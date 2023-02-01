import pandas as pd
import numpy as np
import json

df = pd.read_csv('new_test_sentence_pre_collapse.csv')
df = df.reset_index(inplace=False)
#df.set_index()

json_data = df.to_json(orient ='index' , indent=4)
print(json_data)

json_object = json.loads(json_data)
#print(json_object)

#print(type(json_object))
#print(json_object)

#json_object.to_json(orient ='index', indent=4)
#print(json_object)

#edited_json_data = {"statements" : [json_data]}
#print({"statements" : [json_data]})