#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from evernote.api.client import EvernoteClient
from HTMLParser import HTMLParser
import talkey
from weather import weatherReport
import threading 
import time

# import library using grovepi 
from grovepi import *
from grove_oled import *

from Nettime import TimeUpdate

logging.basicConfig(level='INFO')
# define a global threading lock 
Global_Lock = threading.Lock()


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.ToDo = []
        self.Flag = None
    def handle_starttag(self, tag, attrs):
        logging.info("Encountered a start tag: %s, %s", tag,attrs)
        if tag == "en-todo":
            logging.info( "this is to do tag:")
            if len(attrs) == 0:                                             # Here is the things that need to be done
                self.Flag = True
                logging.info("Here is need to be done")
            else:
                if (attrs[0][0] == "checked" and attrs[0][1] == "true"):
                    logging.info("Here is already done")
    def handle_data(self, data):
        #print("Encountered some data  :", data)
        if self.Flag == True:
            logging.info(data)
            self.Flag = False
            self.ToDo.append(data)
        else:
            pass
    def GetResult(self):
        result = self.ToDo
        self.ToDo = []
        return result
        

# 3bee4c0c-2caf-413c-9e49-d51da6fcdc8c
dev_token = "S=s1:U=92b7b:E=15d39d06877:C=155e21f3928:P=1cd:A=en-devtoken:V=2:H=1304173954fbc76d7432cdf262f7b228"
noteGuid  = "1e77d88b-49e6-4410-aaf5-c85c3bb70a0d"

tts = talkey.Talkey()
tts.say("This is a test")

# Sign in the Evernote
client = None
noteStore = None

def SignInEvernote():
    global client,noteStore 
    result = False
    try:
        client = EvernoteClient(token=dev_token)
        userStore = client.get_user_store()
        user = userStore.getUser()          # here will throw an error
        logging.info(user.username)
        noteStore = client.get_note_store()
        result    = True 
    except Exception, e:
        logging.warn(e)
    return result


def GetNoteContent(noteGuid):
    global noteStore
    content = None
    try:
        content = noteStore.getNoteContent(noteGuid)
    except Exception,e:
        logging.warn(e)
    return content

#parser = MyHTMLParser()
#parser.feed(content)

#This is the Time Out var.
TimeOutIndex = 0

weatherSpeach = None
city          = "shenzhen"
weather       = weatherReport(city)

def weatherInformation(weather):
    speach       = None
    if weather.getWeather() == True:
        speach = ("The weather is %s. Temperature: %.1f. Humidity: %.1f%%. Wind speed: %.1f meters per second" % (weather.weather_desc,weather.temperature,weather.humidity,weather.wind_speed))
        logging.info(speach)
    return speach


# A new class that used to manage the thread 

class GetWeatherInfoThread(threading.Thread):
    def __init__(self,timeout = 1.0):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self._running = True
        self.weatherSpeach = None
        self.subthread = None

    def terminate(self):
        self._running = False
    def runloop(self,TimeInterval):
        self._running = True 
        def TargetFun(self, _TimeInterval):
            while self._running:
                global weather
                speach = weatherInformation(weather)
                if speach != None:
                    global Global_Lock
                    Global_Lock.acquire()
                    self.weatherSpeach = speach
                    Global_Lock.release()
                else:
                    pass
                import time
                time.sleep(_TimeInterval)
        self.subthread = threading.Thread(target=TargetFun,args=(self, TimeInterval,))
        self.subthread.start()
    def isRunning(self):
        if self.subthread.is_alive():
            return True
        else:
            return False

# A new class that used to manage the thread 

class GetEvernoteThread(threading.Thread):
    def __init__(self,timeout = 1.0):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self._running = True
        self.content = None
        self.subthread = None

    def terminate(self):
        self._running = False
    def runloop(self,TimeInterval,noteGuid):
        self._running = True 
        def TargetFun(self, _TimeInterval,_noteGuid):
            while self._running:
                content = GetNoteContent(_noteGuid)
                if content != None:
                    global Global_Lock
                    Global_Lock.acquire()
                    self.content = content
                    Global_Lock.release()
                else:
                    pass
                import time
                time.sleep(_TimeInterval)
        self.subthread = threading.Thread(target=TargetFun,args=(self, TimeInterval,noteGuid))
        self.subthread.start()
    def isRunning(self):
        if self.subthread.is_alive():
            return True
        else:
            return False

class OLEDUpdateThread(threading.Thread):
    def __init__(self,timeout = 1.0):
        threading.Thread.__init__(self)
        oled_init()
        oled_clearDisplay()
        oled_setNormalDisplay()
        oled_setVerticalMode()
        time.sleep(.1)
              
        oled_setTextXY(0,1)			#Print "WEATHER" at line 1
        oled_putString("Assistant")    
        oled_setTextXY(1,0)			#Print "WEATHER" at line 1
        oled_putString("------------")     

        oled_setTextXY(3,1)			#Print "WEATHER" at line 1
        oled_putString("----- --:--")
        
        oled_setTextXY(5,0)			#Print "WEATHER" at line 1
        oled_putString("------------")
        

 
        self.timeout = timeout
        self._running = True
        self.subthread = None
    
    def terminate(self):
        self._running = False
    def runloop(self,TimeInterval):
        self._running = True
        def TargetFun(self,_TimeInterval):
            
            while self._running:
                try:
                    global weather
                    oled_setTextXY(3,1)			#Print "WEATHER" at line 1
                    oled_putString(TimeUpdate())
                    oled_setTextXY(6,1)			#Print "WEATHER" at line 1
                    oled_putString(weather.weather_desc)
                    oled_setTextXY(8,1)			#Print "WEATHER" at line 1
                    oled_putString(str(weather.temperature)+"*C")     
                    oled_setTextXY(10,1)			#Print "WEATHER" at line 1
                    oled_putString("Power@Seeed")                   
                    import time
                    time.sleep(_TimeInterval)
                    logging.info("This is OLED threading")
                except Exception,e:
                    logging.warn(e)
                
        self.subthread = threading.Thread(target=TargetFun,args=(self, TimeInterval))
        self.subthread.start()
    def isRunning(self):
        if self.subthread.is_alive():
            return True
        else:
            return False
        
# The handle of door port
HandlePort = 14  # A0 Port
pinMode(HandlePort,"INPUT")
def ifButtonPressed():
    global HandlePort,Task1,Task2
    try:
        sensor_value = analogRead(HandlePort)
        if sensor_value > 800:
            return True
        else:
            return False
    except Exception,e:
        logging.warn(e)

        
if __name__ == "__main__":

    Task1Weather = GetWeatherInfoThread()
    Task1Weather.runloop(50)   # The Time Interval is 5 second

    Task3OLED = OLEDUpdateThread()
    Task3OLED.runloop(55)
    
    SignResult = SignInEvernote()
    while False == SignResult:
        TimeOutIndex = TimeOutIndex + 1
        logging.info(TimeOutIndex)
        if TimeOutIndex == 10:
            logging.warn("Still Can't Sign in the Evernote")
            TimeOutIndex = 0
            break
        SignResult = SignInEvernote()
        time.sleep(5)
        logging.warn("Can't Sign in the Evernote")
        
 # At here we're successed sign in the evernote  
    Task2Evernote = GetEvernoteThread() 
    if True == SignResult:
        Task2Evernote.runloop(10,noteGuid) 
    else:
        pass
    parser = MyHTMLParser()

    logging.info("Next we'll in loopever")
    
    while True:
        try:
            if True == ifButtonPressed():
                logging.info("There is someone want to go out")  
                logging.info(Task1Weather.weatherSpeach)
                if Task1Weather.weatherSpeach != None:
                    tts.say(Task1Weather.weatherSpeach)
                else:
                    pass
                if Task2Evernote.content != None:
                    parser.feed(Task2Evernote.content)
                    content = parser.GetResult()
                    for result in content:
                        logging.info("The result is :%s",result)
                        tts.say(result)
            else :
                pass
            time.sleep(.1)

        except KeyboardInterrupt:
            Task1Weather.terminate()
            Task2Evernote.terminate()
            Task3OLED.terminate()
            exit()
        except Exception, e:
            logging.info(e)

            