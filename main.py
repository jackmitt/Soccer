import scrapers as scr

#ISRAEL1 2010-2011 season was down
leagues = ["Iran1","UAE1","Singapore1","Qatar1","SouthAfrica1","Morocco1","Algeria1"]
for league in leagues:
    scr.nowgoal(league)
