import scrapers as scr
import datetime
import time


leagues = ["USA1","Brazil1","Brazil2","Japan1","Japan2","Korea1","Australia1","Australia2","Iran1"]
while(1):
    for league in leagues:
        try:
            scr.nowgoalPt2(league)
        except:
            continue
