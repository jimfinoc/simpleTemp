#This is My Nest but it will slowly be converted to superClock!

import urllib
import urllib2
import sys
import json
import time
import datetime
#import requests
#from Adafruit_7SegmentPlus import SevenSegment
#from optparse import OptionParser
import myColorText
import MCP9808
import socket

# Make sure your higher level directory has the JSON file called passwordFile.json
# The file should contain the information in the JSON format. See below for an example
# {"username": "email@somewhere.com", "password": "yourSuperSecretPassword!!!"}
# all temps from the Nest site are stored in degrees Celsius 

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8) #for using PrintColor

#fileData = open('../passwordFile.json')
#usernameAndPassword = json.load(fileData)
valueTimeDate = None

#print "username:" + str(usernameAndPassword['username'])
#print "password:" + str(usernameAndPassword['password'])

sensor2 = MCP9808.MCP9808()
sensor2.begin()

print "Press CTRL+Z to exit"

class Zone(datetime.tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return datetime.timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
        return datetime.timedelta(hours=1) if self.isdst else datetime.timedelta(0)
    def tzname(self,dt):
        return self.name

GMT = Zone(0,False,'GMT')
# True if DST is on
# Fales if now DST
EST = Zone(-5,True,'EST')

#print datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S %Z')
print datetime.datetime.now(GMT).strftime('%m/%d/%Y %H:%M:%S %Z')
print datetime.datetime.now(EST).strftime('%m/%d/%Y %H:%M:%S %Z')



def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

def main():
    try:
        localip = socket.gethostbyname(socket.gethostname())
    except:
        localip = "No ip"
    try:
        print "this is normal printing"
        myColorText.printColor("this is in Yellow", YELLOW)
        sensor2Data = sensor2.readTempC()
        print c_to_f(sensor2Data)
    except:
        print " cannot print in color"
    try:
        with open('/var/www/index.html', 'w') as f:
            tempInF = str(c_to_f(sensor2Data))
#            f.write(tempInF)
#            x = json.dumps({'Local Time' : datetime.datetime.now(EST).strftime('%m/%d/%Y %H:%M:%S %Z') , 'Temperature' : tempInF })
            x = {"Local ip": localip, 'Local Time' : datetime.datetime.now(EST).strftime('%m/%d/%Y %H:%M:%S %Z') , 'Temperature' : tempInF }
            json.dump(x,f)
        f.closed
    except:
        print " cannot open file"

if __name__=="__main__":
    main()
