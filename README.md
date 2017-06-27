# Mapping Where Housing would be Built

This project attempts to map where housing would be built if it was evenly distributed to locations within a 60 minute drive, without traffic, from jobs. Using detailed Census data on job and housing location and a new dataset on driving times between Census Tracts in the US, we can compare where housing would go under this scenario to where housing actually exists today, and map the difference. The analysis excludes Census Tracts as residential tracts if they hold over 4,000 jobs. 

The idea is to get a rough estimate of which neighborhoods could use more housing near jobs and which already have a lot of capacity built relative to jobs nearby. Of course, there are many other ways to do this analysis, so I've provided my code for creating it here so you can change the areas with which you disagree. The driving time dataset was creating using the steps outlined in another [repo](https://github.com/UI-Research/spark-osrm).

### Running the programs in calculate-points

Run the programs in the calculate-points folder in the following order to create data by tract on housing need based on jobs vs. actual housing:

1. Get a Census Tract travel time dataset produced from this [repo](https://github.com/UI-Research/spark-osrm).
2. Run get_jobs.py - Downloads the Census LEHD website and condenses it to a single CSV file.
3. Run get_housing.py - Downloads the Census Housing Unit data and condenses it to a single CSV file. You'll need to replace `key` with your Census API Key (if you don't have one, you can get [one](http://api.census.gov/data/key_signup.html)).
4. Run calculate_housing.py - Links the three datasets and produces a dataset ready to be used to generate dot density maps.

### Create dot density files

Run the programs in the create-points to create dot density tiles for interactives:

