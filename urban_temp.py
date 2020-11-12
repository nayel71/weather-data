import pandas as pd
import numpy as np

class UrbanWeather:
	"""A class to analyse urban temperature data from datasets. Assume a location to
	   be urban if it is within urban_radius kilometres of some city.
	"""
	@staticmethod
	def haversine_np(lng1, lat1, lng2, lat2):
		"""Return the great circle distance in kilometres between two locations with
		   coordinates (lng1, lat1) and (lng2, lat2) specified in decimal degrees.
		"""
		lng1, lat1, lng2, lat2 = map(np.radians, [lng1, lat1, lng2, lat2])
		dlng = lng2 - lng1
		dlat = lat2 - lat1
		a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlng/2.0)**2
		c = 2 * np.arcsin(np.sqrt(a))
		km = 6367 * c
		return km

	def __init__(self, cities_csv, climate_csv, urban_radius):
		self.cities = pd.read_csv(cities_csv)
		self.climate = pd.read_csv(climate_csv)

		city_coords = self.cities[["lng", "lat"]].to_numpy()
		climate_coords = self.climate[["lng", "lat"]].to_numpy()
		self.climate["LOCAL_DATE"] = pd.to_datetime(
			self.climate["LOCAL_DATE"],
			errors="coerce"
		)
		self.climate["LOCAL_DATE"] = self.climate["LOCAL_DATE"].dt.date
		urban = []

		for climate_city in climate_coords:
			lng = climate_city[0]
			lat = climate_city[1]
			for city in city_coords:
				if self.haversine_np(city[0], city[1], lng, lat) < urban_radius:
					urban.append(True)
					break
				else:
					urban.append(False)
					break

		self.climate["urban"] = urban
		self.urbans = self.climate[self.climate["urban"] == True]

	def urban_temp(self, date):
		"""Return the urban temperature on date as a pandas column."""
		date = pd.to_datetime(date)
		today = self.urbans[self.urbans["LOCAL_DATE"] == date]
		today = today.reset_index(drop="True")
		return today["MEAN_TEMPERATURE"]

if __name__ == "__main__":
	data = UrbanWeather("cities.csv", "climate.csv", 25) # take urban_radius = 25
	for day in range(10, 32):
		date = "2020-01-" + str(day)
		temperatures = data.urban_temp(date)
		print("Mean urban temparature on", date + ":", temperatures.mean())
		print("Median urban temparature on", date + ":", temperatures.median())
