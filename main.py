import time
import pandas as pd
import json
from editDataframe import df
#from main_file import fileName

descriptorFileName = str(input("Enter the name you want to give to your descriptor file (along with the .json extension): \n"))

try:
    df.pop('index')
except:
    pass
try:
    df.pop('Unnamed: 0')
except:
    pass
try:
    df.pop('level_0')
except:
    pass

json_data = df.to_json(orient ='records' , indent=4)

my_dict = {}
my_dict["statements"] = json.loads(json_data)

print(json.dumps(my_dict, indent=4))

#descriptorFileName = str(input('Type your descriptor file name WITH the .json extension: \n'))

# Writing to sample.json
with open(descriptorFileName, "w") as outfile:
    json.dump(my_dict, outfile)

outfile.close()