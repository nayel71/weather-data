import pandas as pd
import numpy as np

class UrbanWeather:
    """A class to analyse urban temperature data from datasets. Assume a location to
       be urban if it is within urban_radius kilometres of some city.
    """
    @staticmethod
    def haversine_np(loc1, loc2):
        """Return the great circle distance in kilometres between two locations."""
        lat1, lng1, lat2, lng2 = map(np.radians, [loc1[0], loc1[1], loc2[0], loc2[1]])
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlng/2.0)**2
        c = 2 * np.arcsin(np.sqrt(a))
        km = 6367 * c
        return km

    def __init__(self, cities_csv, climate_csv, urban_radius):
        self.cities = pd.read_csv(cities_csv)
        self.climate = pd.read_csv(climate_csv)

        city_coords = self.cities[["lat", "lng"]].to_numpy()
        climate_coords = self.climate[["lat", "lng"]].to_numpy()
        self.climate["LOCAL_DATE"] = pd.to_datetime(
            self.climate["LOCAL_DATE"],
            errors="coerce"
        )
        self.climate["LOCAL_DATE"] = self.climate["LOCAL_DATE"].dt.date
        urban_list = []
        urban_dict = {}

        for location in climate_coords:
            loc_tuple = tuple(location)
            if loc_tuple in urban_dict:
                urban_list.append(urban_dict[loc_tuple])
                continue
            is_urban = False
            for city in city_coords:
                if self.haversine_np(city, location) < urban_radius:
                    is_urban = True
                    break
            urban_list.append(is_urban)
            urban_dict[loc_tuple] = is_urban

        self.climate["urban"] = urban_list
        self.urbans = self.climate[self.climate["urban"] == True]

    def urban_temp(self, date):
        """Return the urban temperature on date as a pandas column."""
        date = pd.to_datetime(date)
        today = self.urbans[self.urbans["LOCAL_DATE"] == date]
        today = today.reset_index(drop="True")
        return today["MEAN_TEMPERATURE"]

if __name__ == "__main__":
    data = UrbanWeather("cities.csv", "climate.csv", 25) # take urban_radius = 25
    date = "2020-01-01"
    temperatures = data.urban_temp(date)
    print("Mean urban temparature on", date + ":\t", temperatures.mean())
    print("Median urban temparature on", date + ":\t", temperatures.median())
