import scrapers as scr

leagues = ["Russia1","Russia2","Poland1","Poland2","Ukraine1","Czech1","Czech2","Greece1","Romania1","Slovakia1","Slovakia2","Iceland1","Israel2","Belarus1","Lithuania1","Turkey1","Turkey2","Wales1","Hungary1","Croatia1","Bulgaria1","Slovenia1","Cyprus1","Serbia1","Albania1","Kazakhstan1","Bosnia1","Estonia1","Montenegro1","USA1","Brazil1","Brazil2","Japan1","Japan2","Korea1","Australia1","Australia2","Iran1"]
while(1):
    for league in leagues:
        try:
            scr.nowgoalPt2(league)
        except:
            continue
