import scrapers as scr

leagues = ["England1","England2","England3","England4","Spain1","Spain2"]
while(1):
    for league in leagues:
        try:
            scr.nowgoalPt2(league)
        except:
            continue
