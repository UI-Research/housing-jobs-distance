import pandas as pd
import numpy as np
import urllib
import gzip
import os

states = ["al","ak","az","ar","ca","co","ct","de","dc","fl","ga","hi","id","il","in","ia","ks","ky","la","me","md","ma","mi","mn","ms","mo","mt","ne","nv","nh","nj","nm","ny","nc","nd","oh","ok","or","pa","ri","sc","sd","tn","tx","ut","vt","va","wa","wv","wi","wy"]
url = 'https://lehd.ces.census.gov/data/lodes/LODES7/{}/wac/{}_wac_S000_JT00_2014.csv.gz'
data = pd.DataFrame(columns = ['tract','jobs'])

for state in states:
	print("Working on {}".format(state))
	url1 = url.format(state,state)
	if state == 'wy': url1 = url1.replace('2014','2013')
	fname = url1.split('/')[-1]
	urllib.urlretrieve(url1,fname)
	data1 = pd.read_csv(fname, compression = 'gzip')
	data1["tract"] = [str(x).zfill(15)[:11] for x in data1["w_geocode"]]
	data1 = data1[["tract","C000"]].rename(columns={"C000":"jobs"})
	data = data.append(data1, ignore_index = True)
	os.remove(fname)

group = data.groupby('tract', as_index = True)
aggregate = group['jobs'].apply(np.sum).reset_index()
aggregate['tract'] = [str(x).zfill(11) for x in aggregate['tract']]
aggregate.to_csv('jobs_data.csv', index = False)