#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import csv

from config import *

NEW_VAT_PROCESSING = True

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
    
                vat = float(row[12])
                
                if (vat <> 0):
                    toChange =appData ["withvat"] 
                else:
                    toChange =appData ["nonvat"]
                toChange["downloads"] += 1
                exRate = 1
                if row[15] != "":
                    exRate = float(row[15]) 
                vat = float(row[12]) * exRate
                if NEW_VAT_PROCESSING:
                    toChange["vat"] += vat * 0.7
                    toChange["charged"] += float(row[16]) - vat * 0.7
                else:
                    toChange["vat"] += vat 
                    toChange["charged"] += float(row[16]) - vat
                    
                
                
                               
                price = row[11]
                price = price.replace(",","")
                if len(row[15]) == 0:
                    row[15] = 0 
                if NEW_VAT_PROCESSING:
                    toChange["google"] += (exRate * float(price)) * 0.3 + vat * 0.3
                else:
                    toChange["google"] += (exRate * float(price)) * 0.3
        counter += 1
    # display results
    print "Name;Items;Charged (inc. VAT and Google provision);VAT;Profit (exc. VAT);Google"
    for appId in appsStats:
        dict = appsStats[appId]
        name = apps[appId]
        for typ in ("withvat", "nonvat"):
            print "%s;%d;%f;%f;%f;%f" % (name, dict[typ]["downloads"],dict[typ]["charged"] + dict[typ]["google"] + dict[typ]["vat"], dict[typ]["vat"], dict[typ]["charged"], dict[typ]["google"])

def main():
    if len(sys.argv) == 1:
        print "No filename specified"
    else:
        fileToImport = sys.argv[1]
        processStats(fileToImport)

if __name__ == "__main__":
    main()