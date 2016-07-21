#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import urllib
import time
from grovepi import *
from grove_oled import *
from Nettime import TimeUpdate

from threading import Timer

weather_desc = "UnKonw"                  # General description of the weather
tempOut      = "UnKonw"                  # Temperature in C
pressure     = "UnKonw"                  # Pressure in hPa
humidity     = "UnKonw"                  # Humidity %
wind_speed   = "UnKonw"   
Task1        = None
Task2        = None
weather_Status = "系统正在初始化"        # the weather voice need to be display

TimeInterval1 = 1800  #  update weather data time interval  unit second
TimeInterval2 = 10   #  update time data interval          unit second
dht_sensor_port = 3	 # 
playCommand = "mplayer voice.wav"

weatherStatus = {
                 "Rain":"今天有雨，不要忘了带伞。",\
                 "Clouds":"今天多云，但是我还是希望你有个好心情。",\
                 "Haze":"今天有雾霾，不要忘了带口罩哦。",\
                 "Drizzle":"今天有毛毛雨，淅沥淅沥的下个不停。",\
                 "Clear":"今天天气真不错啊，好想出去约会呢。",\
                 "Mist":"今天有点雾，开车要慢一点，听到了没。",\
                 "UnKonw":"我不知道这个天气用中文怎么说，帮帮我吧。"
                }

                
                
                
# weather information
city="shenzhen"
appID = "a9764b47b351cacfc45a5a352af45441"
url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&APPID=" + appID

def initLCD():
    oled_init()
    oled_clearDisplay()
    oled_setNormalDisplay()
    oled_setVerticalMode()
    time.sleep(.1)
    oled_setTextXY(0,1)			#Print "WEATHER" at line 1
    oled_putString("----- --:--")

# DHT Sensor Port 3    
dht_sensor_port = 3    
def updateLocalWeather():
    global weather_desc,tempOut,pressure,humidity,wind_speed,weather_Status
    try:
        [ temp,hum ] = dht(dht_sensor_port,1)		#Get the temperature and Humidity from the DHT sensor
        print "temp =", temp, "C\thumidity =", hum,"%" 	
        t = str(temp)
        h = str(hum)
        
        oled_setTextXY(0,1)			#Print "WEATHER" at line 1
        oled_putString(TimeUpdate())
        
        oled_setTextXY(2,0)			#Print "TEMP" and the temperature in line 3
        oled_putString("---Indoor---")
        
        oled_setTextXY(3,0)			#Print "TEMP" and the temperature in line 3
        oled_putString("Temp:")
        oled_putString(t+'C')
		
        oled_setTextXY(4,0)			#Print "HUM :" and the humidity in line 4
        oled_putString("Hum :")
        oled_putString(h+"%")
        
        oled_setTextXY(6,0)			#Print "TEMP" and the temperature in line 3
        oled_putString("--Out door--")
        
        oled_setTextXY(7,0)
        oled_putString(weather_desc)
        
        oled_setTextXY(8,0)
        oled_putString("Temp:")
        oled_putString(str(tempOut)+'C')       
        
        oled_setTextXY(9,0)
        oled_putString("Wind:")
        oled_putString(str(wind_speed))               
        
        
    except (IOError,TypeError) as e:
        print "Error"

# The handle of door port
HandlePort = 14  # A0 Port
pinMode(HandlePort,"INPUT")
def ifButtonPressed():
    global HandlePort,Task1,Task2
    try:
        sensor_value = analogRead(HandlePort)
        print("sensor_value = ", sensor_value)
        if sensor_value > 800:
            return True
        else:
            return False
    except KeyboardInterrupt:
        Task1.cancel()
        Task2.cancel()
        exit()
    except:
        print("Error")

def weatherReport(status):
    global playCommand
    command = "ekho " + status + " -o voice.wav"
    os.system(command)
    os.system(playCommand)

    
def updateWeather():
    global weather_desc,tempOut,pressure,humidity,wind_speed,weather_Status
    jsonurl = urllib.urlopen(url)                      # open the url
    text = json.loads(jsonurl.read())
    
    weather_desc=text["weather"][0]["main"]            # General description of the weather
    tempOut = float(text["main"]["temp"])-273.15       # Temperature in C
    pressure=text["main"]["pressure"]                  # Pressure in hPa
    humidity=text["main"]["humidity"]                  # Humidity %
    wind_speed=text["wind"]["speed"]                   # Wind speed mps

    try:
        weather_Status = weatherStatus[weather_desc]
    except:
        weather_Status = weatherStatus["UnKonw"]
        weatherStatus[weather_desc] = weather_desc
    weather_Status += ("温度：" + str(tempOut) + "度。")   
    weather_Status += ("相对湿度：百分之" + str(humidity) + "。")  
    weather_Status += ("风速：" + str(wind_speed) + "级。")  
    # weatherReport(weather_Status)
    
    print weather_desc,tempOut,pressure,humidity,wind_speed
    updateTask1()
    
    
def updateTime():
    # print(TimeUpdate())
    updateLocalWeather()
    updateTask2()
    

# Create Tasks
def updateTask1():
    global Task1
    Task1 = Timer(TimeInterval1,updateWeather)
    Task1.start()
def updateTask2():
    global Task2
    Task2 = Timer(TimeInterval2,updateTime)
    Task2.start()
    
if __name__ == "__main__":
    initLCD()
    updateWeather()
    updateTime()
    updateLocalWeather()
    while True:
        try:
            # print("LOOP")
            if True == ifButtonPressed():
                print("True")
                weatherReport(weather_Status)
            else :
                print("False")
            # print(TimeUpdate())
            time.sleep(.1)
        except KeyboardInterrupt:
            Task1.cancel()
            Task2.cancel()
            exit()
       