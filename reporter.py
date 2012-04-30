#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import csv

from config import *


kurzy = {}
appsStats = {}

#configuration - fill your apps info here


def getDataForApp(appName):
    if appName in apps:
        appId = appName
        if not appId in appsStats:
            appsStats[appId] = {"withvat": {"downloads": 0, "vat": 0, "charged": 0, "google": 0}, "nonvat":{"downloads": 0, "vat": 0, "charged": 0, "google": 0}} 
        return appsStats[appId]
    else:
        print "Unknown app %s" % appName
        sys.exit()
        return None    
        

def processStats(fileName):
    # loads CSV with stats
    csvData = csv.reader(open(fileName, 'r'))
    counter = 0
    for row in csvData:
        if row[0][:5].isdigit():
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
                price = row[9]
                price = price.replace(",","")
                toChange["google"] += float(price) * exRate - float(row[14])
        counter += 1
    # display results
    print "Name;Items;Charged;VAT;Profit;Google"
    for appId in appsStats:
        dict = appsStats[appId]
        name = apps[appId]
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