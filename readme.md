# Voice Assitant
-----
## Intrudction
This is an APP that can read the weather info form the openweathermap as well as the Evernote note and then speak it out

## Install Espeak
* Open your favourite terminate and excute the following commands
```
sudo apt-get install python-dev
```
```
sudo agt-get install espeak
sudo apt-get install python-espeak
```
* Test it
```
espeak "hello world"
```
## Install Talkey
[Talkey](http://talkey.readthedocs.org/) is a simple Text-To-Speech (TTS) interface library with multi-language and multi-engine support.
* Install from talkey
```
pip install talkey
```
* Test it in python 
```
import talkey
tts = talkey.Talkey()
tts.say('Old McDonald had a farm')
```
## Install Evernote SDK
The Evernote provide a very useful  python api. Click [here](https://dev.evernote.com/doc/start/python.php) to get a Quick-start Guid about python SDK.
```
pip install evernote
```

## Change the Code 
Chane the code in line 45 and 46 to your own dev_token and NoteGuid
```
dev_token = "your own token"
noteGuid  = "your note book Guid"
```
## Run the Code
```
python EvernoteTest.py
```

If you have any questions about this project, please just let me know, my email lidreamer@foxmail.com or lidreamer@163.com

##License

This is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
