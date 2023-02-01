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
    if (data['statements'][i]['section'] == 'PREPARED_REMARKS') or (data['statements'][i]['section'] == 'Q_AND_A'):
        print("NO ERROR")
    else:
        print("ERROR ON LINE:{}".format(i))
        print(data['statements'][i]['statement'])
        print('...')
        break
    i += 1
   
# Closing file
f.close()