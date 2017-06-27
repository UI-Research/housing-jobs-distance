import pandas as pd
import numpy as np

# Read in and convert travel time to include both ab and ba
data = pd.read_csv('tract_drive_times.csv')
data1 = data[data["minutes"] <= 60]
data2 = data[data["minutes"] <= 60]
data2["from_tract"] = data1["to_tract"]
data2["to_tract"] = data1["from_tract"]
data = data1.append(data2, ignore_index = True)
data = data.rename(columns={"from_tract":"tract"})

# Read in and merge jobs data, filtering out high-jobs tracts as residential destinations
jobs = pd.read_csv('jobs_data.csv')
jobs_distance = jobs.merge(data, on = "tract", how = "left")
jobs["high_density"] = [True if x >=4000 else False for x in jobs["jobs"]]
jobs = jobs.rename(columns={"tract":"to_tract"})
jobs_distance = jobs_distance.merge(jobs[["to_tract","high_density"]], on = "to_tract", how = "left")
jobs_distance = jobs_distance[jobs_distance["high_density"] != True]
group = jobs_distance.groupby('tract', as_index = True)
num_per = group["jobs"].count().reset_index().rename(columns={"jobs":"num_geos"})
jobs_distance = jobs_distance.merge(num_per, on = "tract", how = "inner")
housing_data = pd.read_csv('housing_data.csv')
jobs_per_unit = np.divide(np.sum(jobs["jobs"]),np.sum(housing_data["housing_units"]))
jobs_distance["units"] = np.multiply(np.divide(jobs_distance["jobs"],jobs_distance["num_geos"]), jobs_per_unit)
group = jobs_distance.groupby("to_tract", as_index = True)
total_jobs = group["units"].apply(np.sum).reset_index().rename(columns={"to_tract":"tract"})
total_jobs["tract"] = [str(int(x)).zfill(11) for x in total_jobs["tract"]]
total_jobs["units"] = [round(x) for x in total_jobs["units"]]
total_jobs["units"] = total_jobs["units"].astype(int)

# Merge unit data
housing_data["tract"] = [str(int(x)).zfill(11) for x in housing_data["tract"]]
total_jobs = total_jobs.merge(housing_data, on = "tract", how = "left")
total_jobs["diff"] = np.subtract(total_jobs["housing_units"],total_jobs["units"])
total_jobs["base"] = [x if y >= 0 else z for x,y,z in zip(total_jobs["units"],total_jobs["diff"],total_jobs["housing_units"])]
total_jobs["shortage"] = [abs(x) if x < 0 else 0 for x in total_jobs["diff"]]
total_jobs["additional"] = [x if x >= 0 else 0 for x in total_jobs["diff"]]
total_jobs[["tract","base","shortage","additional"]].to_csv('dots_ready.csv', index = False)