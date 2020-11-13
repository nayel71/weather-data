# Analyse Weather Data for Canadian Cities

## Task

Attached are two files.  One has climate information for a few weeks in early 2020 collected at weather stations around Canada.  The second has demographic information about Canadian cities and includes the majority of Canada's urban population.  The latitude and longitude values can be used to associate the cities and the weather stations.

Your task is to provide a method that reads both files, accepts a date, and computes the mean and median temperature for Canadians daytime temperature that urban Canadian's experienced on that day.

Please track any assumptions or trade-offs that you make during the exercise and justify the decisions you made.

If you see any other interesting patterns or results that you can extract from the data feel free to highlight a couple.

For this exercise it's not important to consider scaling this to larger datasets but think about how that would change your approach.

## Solution

`urban_temp.py`: It is a Python program that will print the mean and median urban temperatures for a specified date (on line 57). 

### Methods

- The primary method of interest is `UrbanWeather.urban_temp()`, which takes the date parameter as a string (in the format “YYYY-MM-DD”) and returns the corresponding urban temperature data (as a pandas column). One can then call the `pd.mean()` and `pd.median()` methods to obtain the specific values of interest.
- The static method `UrbanWeather.haversine_np()` takes the longitudes and latitudes of two points and returns their great circle distance in kilometres. 

### Assumptions

- I took `urban_radius` to be 25 on line 54. This represents the great circle distance in kilometres from a city’s coordinates within which an area is to be classified as “urban”.
- While calculating the temperatures I worked with the `MEAN_TEMPERATURE` data from `climate.csv`. This can be modified as necessary in the `UrbanWeather.urban_temp()` method.

### Comments

- The program takes about 2 seconds to answer a single query for the given dataset, so it should be able to handle larger datasets efficiently. Once the data files and `urban_radius` are specified on line 54, the program processes the data once and can quickly answer subsequent queries for any given date.
- I spent roughly 3 hours on the problem and some more on improving the presentation. 

### Other Observations

- I noticed that with a 25 km `urban_radius` there were only 4 urban areas identified from the climates data. With a 20 km value there were only 3, and with 50 km there were 5.
