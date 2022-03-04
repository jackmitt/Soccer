import scrapers as scr

leagues = ["Spain2","France1","France2","France3","Italy1","Italy2","Germany1","Germany2","Germany3"]
while(1):
    for league in leagues:
        try:
            scr.nowgoalPt2(league)
        except:
            continue
