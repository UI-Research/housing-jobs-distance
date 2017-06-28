import pandas as pd
import numpy as np

print("Prepping Data")
data = pd.read_csv('dots_ready.csv')
data["tract"] = [str(int(x)).zfill(11) for x in data["tract"]]

convert = pd.read_csv('tract_to_place.csv', header=1)
convert['tract'] = ['{}{}'.format(str(x).zfill(5),str(int(y*100)).zfill(6)) for x,y in zip(convert["county"],convert["2010 Tract"])]
convert = convert[["tract","placefp","tract to placefp alloc factor"]]
convert = convert.rename(columns={"tract to placefp alloc factor":"factor"})

data = data.merge(convert, on = "tract", how = "left")
cols = ["base", "shortage", "additional"]
for col in cols:
	data["{}_factor".format(col)] = np.multiply(data[col],data["factor"])

group = data.groupby("placefp")
aggregate = group[["{}_factor".format(a) for a in cols]].apply(np.sum).reset_index()
aggregate["placefp"] = [str(int(x)).zfill(5) for x in aggregate["placefp"]]
renames = {"{}_factor".format(a):"{}".format(a) for a in cols}
aggregate = aggregate.rename(columns=renames)
for col in cols:
	aggregate[col] = [int(round(x)) for x in aggregate[col]]

print("Results")
print("")
aggregate["net"] = np.subtract(aggregate["additional"],aggregate["shortage"])
print("Nationally: {:,}").format(np.sum(aggregate["net"]))
print("Place (net): {:,}".format(np.sum(aggregate["net"][aggregate["placefp"] != '99999'])))
print("Non Place (net): {:,}".format(aggregate["net"][aggregate["placefp"] == '99999'].values[0]))
print("")

convert = pd.read_csv('tract_to_place.csv', header=1)
convert["placefp"] = [str(int(x)).zfill(5) for x in convert["placefp"]]
convert = convert[["placefp","Place Name","Total HUs, 2010 census"]]
convert = convert.drop_duplicates('placefp')
aggregate = aggregate.merge(convert, on = "placefp", how = "left")
aggregate = aggregate[[int(x) < 99999 for x in aggregate["placefp"]]]
aggregate = aggregate[aggregate["base"] >= 5000]

print("Worst Cities, total number:")
print(aggregate[["Place Name","net"]].sort_values('net').head(50))
print("")
print("Best Cities, total number:")
print(aggregate[["Place Name","net"]].sort_values('net', ascending=False).head(50))
print("")

aggregate["net_perc"] = np.divide(aggregate["net"],aggregate["base"].astype(float))

print("Worst Cities, percentage:")
print(aggregate[["Place Name","net_perc"]].sort_values('net_perc').head(50))
print("")
print("Best Cities, percentage:")
print(aggregate[["Place Name","net_perc"]].sort_values('net_perc', ascending=False).head(50))
print("")

aggregate.to_csv('place_results.csv', index = False)
