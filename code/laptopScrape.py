import scrapers as scr
import datetime
import time

#leagues = ["USA1","Brazil1","Brazil2","Japan1","Japan2","Korea1","Australia1","Australia2","Iran1","UAE1","Singapore1","Qatar1","SouthAfrica1","Morocco1","Algeria1","Czech1","Czech2","Denmark1","Denmark2","Finland1","Finland2","Sweden1","Sweden2","Norway1","Norway2"]
leagues = ["Albania1","Austria1","Austria2","Belarus1","Belgium1","Belgium2","Bosnia1","Bulgaria1","Croatia1","Cyprus1","Estonia1","Greece1","Hungary1","Iceland1","Ireland1","Ireland2","Israel2","Kazakhstan1","Lithuania1","Montenegro1","NorthernIreland1","Poland1","Poland2","Portugal1","Portugal2","Romania1","Russia1","Russia2","Scotland1","Scotland2","Serbia1","Slovakia1","Slovakia2","Slovenia1","Turkey1","Turkey2","Ukraine1","Wales1"]
while(1):
    for league in leagues:
        try:
            scr.nowgoalPt2(league)
        except:
            continue
