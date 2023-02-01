import pandas as pd
import json

# Opening JSON file
f = open('test_sentence_pre_collapse.json',)
   
# returns JSON object as 
# a dictionary
data = json.load(f)

#print(data)
   
# Iterating through the json
# list
i = 0
while i < len(data['statements']):
    if (data['statements'][i]['stop'] > data['statements'][i+1]['start']):
        print("ERROR: {}".format(data['statements'][i]))
        i += 1
        break
    else:
        print(i)
        print(data['statements'][i]['statement'])
        print('...')
        i += 1
   
# Closing file
f.close()