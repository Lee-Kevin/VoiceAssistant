#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib
import logging
import time

logging.basicConfig(level='INFO')

class weatherReport():
    def __init__(self,city):
        self.Flag         = False 
        self.weather_desc = None
        self.temperature  = None
        self.pressure     = None
        self.humidity     = None
        self.wind_speed   = None
        self.appID = "a9764b47b351cacfc45a5a352af45441"
        self.url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&APPID=" + self.appID
    def getWeather(self):
        try:
            jsonurl = urllib.urlopen(self.url)
            text    = json.loads(jsonurl.read())

            self.weather_desc = text["weather"][0]["main"]
            self.temperature  = float(text["main"]["temp"]) - 273.15
            self.pressure     = text["main"]["pressure"]
            self.humidity     = text["main"]["humidity"]
            self.wind_speed   = text["wind"]["speed"]
            self.Flag         = True 
        except Exception, e:
            self.Flag         = False 
            logging.warn(e)
        return self.Flag

def main():
    weather = weatherReport("beijing")
    if weather.getWeather() == True:
        logging.info("The weather in the city is:")
        logging.info("%s,%.2f,%.2f,%.2f,%.2f",weather.weather_desc,weather.temperature,weather.pressure,weather.humidity,weather.wind_speed)

if __name__ == "__main__":
    logging.info("The Test code is beginning")
    while True:
        main()
        time.sleep(5)