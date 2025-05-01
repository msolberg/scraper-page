#!/bin/env python3.8

import os
import urllib.request
import json
import time

from prometheus_client import start_http_server, Gauge

# Set a few globals here
height = Gauge('height', 'River height')
height.set(1.2)

siteCode = "02333500"

def get_river_height(siteCode="02333500"):
    variable = None
    value = None
    waterservices_url = 'https://waterservices.usgs.gov/nwis/iv/?format=json&sites=%s&siteStatus=all'% siteCode
    try:
        with urllib.request.urlopen(waterservices_url) as response:
            json_response = response.read()
    
        stats = json.loads(json_response)
        
        for v in stats['value']['timeSeries']:
            if v['variable']['variableCode'][0]['value'] == "00065":
                variable = v
                value = v['values'][0]['value'][0]['value']
        
        height.set(float(value))
        print("River height %s"% value)
    
    except urllib.error.URLError as e:
        print("Error accessing waterservices.usgs.gov: %s"% e.reason)
    
    return value

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    
    while True:
        get_river_height(siteCode="02333500")
        time.sleep(60)
