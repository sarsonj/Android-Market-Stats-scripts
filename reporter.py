#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import urllib2
import csv
import os
import time


kurzy = {}
appsStats = {}

#configuration - fill your apps info here

appNames = {
            "babyam": "Baby Monitor Alarm",
            "geotag": "Geotag Photos Pro",
            "enumbers": "E Numbers Calc"
            }

nameToAppId = {
             "com.tappytaps.android.babymonitoralarm.full": "babyam",             
             "com.tappytaps.android.geotagphotospro": "geotag",
             "com.tappytaps.android.enumbers.full": "enumbers",
             }


def getDataForApp(appName):
    if appName in nameToAppId:
        appId = nameToAppId[appName]
        if not appId in appsStats:
            appsStats[appId] = {"withvat": {"downloads": 0, "vat": 0, "charged": 0, "google": 0}, "nonvat":{"downloads": 0, "vat": 0, "charged": 0, "google": 0}} 
        return appsStats[appId]
    else:
        print "Unknown app %s" % appName
        sys.exit()
        return None    
        
def convertToCzk(amount, currency, table):
    return float(amount) * table[currency]
    

def processStats(fileName):
    # loads CSV with stats
    csvData = csv.reader(open(fileName, 'r'))
    counter = 0
    for row in csvData:
        if counter <> 0:
            appData = getDataForApp(row[7])
            if (appData <> None):
    
                vat = float(row[10])
                
                if (vat <> 0):
                    toChange =appData ["withvat"] 
                else:
                    toChange =appData ["nonvat"]
                toChange["downloads"] += 1
                exRate = 1
                if row[13] != "":
                    exRate = float(row[13]) 
                
                toChange["vat"] += float(row[10]) * exRate 
                toChange["charged"] += float(row[14])
                toChange["google"] += float(row[9]) * exRate - float(row[14])
        counter += 1
    # display results
    print "Name;Items;Charged;VAT;Profit;Google"
    for appId in appsStats:
        dict = appsStats[appId]
        name = appNames[appId]
        for typ in ("withvat", "nonvat"):
            print "%s;%d;%f;%f;%f;%f" % (name, dict[typ]["downloads"],dict[typ]["vat"] + dict[typ]["charged"] + dict[typ]["google"], dict[typ]["vat"], dict[typ]["charged"], dict[typ]["google"])

def main():
    if len(sys.argv) == 1:
        print "No filename specified"
    else:
        fileToImport = sys.argv[1]
        processStats(fileToImport)

if __name__ == "__main__":
    main()