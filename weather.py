import csv
import datetime
import json
import os
import shutil
import time
from datetime import timedelta, date
# module to convert an address into latitude and longitude values
from geopy.geocoders import Nominatim
import pandas as pd
import requests

def select_keys(d, ks):
    return {k: d[k] for k in ks if k in d}

class Weather(object):
    """API for getting the weather at a spacetime point"""

    def __init__(self):
        super(Weather, self).__init__()
        self.debug = os.environ.get('DEBUG', False)
        self.apikey = os.environ.get('WEATHER_API_KEY')
        self.geolocator = Nominatim()

    def _address_to_latlon(self, address):
        location = self.geolocator.geocode(address)
        return location.latitude, location.longitude

    def _dt_to_str(self, dt):
        return dt.strftime('%Y%m%d')

    def _get_json(self, url):
        return requests.get(url).json()

    def weather_at_spacetime(self, lat, lon, dt):
        start = self._dt_to_str(dt)
        end = self._dt_to_str(dt + timedelta(days=1))
        tpl = 'http://api.weather.com/v1/geocode/{lat}/{lon}/observations/historical.json' + \
                '?apiKey={apikey}&units=m&language=en-US' + \
                '&startDate={startDate}&endDate={endDate}'
        url = tpl.format(**dict(lat=lat, lon=lon, apikey=self.apikey,
            startDate=start, endDate=end))
        return self._get_json(url)

    def weather_forecast(self, lat, lon):
        "3 day forecast"
        tpl = "http://api.weather.com/v1/geocode/{lat}/{lon}/forecast/daily/3day.json" + \
                    "?apiKey={apikey}&units=m"
        url = tpl.format(**dict(lat=lat, lon=lon, apikey=self.apikey))
        return self._get_json(url)

    def parse_forecast(self, forecast):
        "Precip & temp data for next 3 (1/2) days"
        ## 'max_temp', 'min_temp', 'qpf'
        ## 'snow_qpf' (opt)
        ## 'night' / 'day'
        fcs = forecast['forecasts']
        return [select_keys(fc, ('max_temp', 'min_temp', 'qpf', 'snow_qpf'))
                for fc in fcs]

    def forecast_summary(self, address):
        "Ye olde business logick"
        lat, lon = self._address_to_latlon(address)
        forecast = self.weather_forecast(lat, lon)
        data = self.parse_forecast(forecast)
        if self.debug:
            print(data)
        freeze = any(fc['min_temp'] <= 0.0 for fc in data)
        rain = sum(fc['qpf'] for fc in data) > 0.0
        ## just return flag, deal with display messaging in main app
        if freeze:
            return 'freeze'
        elif rain:
            return 'rain'
        else:
            return 'ok'

def main():
    import sys
    import pprint
    import dotenv
    dotenv.load_dotenv(dotenv.find_dotenv())
    if len(sys.argv) == 2:
        address = sys.argv[1]
    else:
        address = '1644 Platte St, Denver, CO'
    weather = Weather()
    # lat, lon = weather._address_to_latlon(address)
    # forecast = weather.weather_forecast(lat, lon)
    # data = weather.parse_forecast(forecast)
    # pprint.pprint(data)
    print(weather.forecast_summary(address))
    ## pprint.pprint(forecast)
    ## print(json.dumps(forecast, indent=2))

if __name__ == '__main__':
    main()
