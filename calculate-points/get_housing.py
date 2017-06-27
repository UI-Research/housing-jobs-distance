import requests
import json
import pandas as pd
import numpy as np

states = '01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56'.split(' ')
key = 'YOUR CENSUS API KEY'
url = 'http://api.census.gov/data/2015/acs5?get=NAME,B25001_001E&for=tract:*&in=state:{}&key={}'

data_store = []
for state in states:
	print("On state {}".format(state))
	data = json.loads(requests.get(url.format(state,key)).text)
	for line in data[1:]:
		data_store.append({"tract": "{}{}{}".format(line[2],line[3],line[4]),"housing_units":line[1]})

data_frame = pd.DataFrame(data_store)
data_frame.to_csv('housing_data.csv', index = False)