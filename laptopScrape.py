import scrapers as scr
import datetime
import time


leagues = ["Czech1","Czech2","Denmark1","Denmark2","Finland1","Finland2","Sweden1","Sweden2","Norway1","Norway2"]
while(1):
    for league in leagues:
        try:
            scr.nowgoalPt2(league)
        except:
            continue
