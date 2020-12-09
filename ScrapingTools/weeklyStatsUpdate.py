from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import numpy as np
import gc
from miscFcns import monthToInt
from miscFcns import standardizeTeamName
para = "EPL"


#change every week - number of matchweeks played
mwThru = 11
intBreakCount = 2
dateStart = datetime.date(2020, 9, 10) + datetime.timedelta(days=7*(mwThru-1+intBreakCount))
dateThru = datetime.date(2020, 9, 10) + datetime.timedelta(days=7*(mwThru+intBreakCount))




gameUrls = []
#
browser = webdriver.Chrome(executable_path='chromedriver.exe')
browser.get("https://understat.com/league/EPL/")
while (1):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    temp = soup.find(class_="calendar-prev")
    days = soup.find_all(class_="calendar-date-container")
    for day in days:
        d = day.find(class_="calendar-date").string
        curDate = datetime.date(int(d.split()[3]), monthToInt(d.split()[1]), int(d.split()[2].split(",")[0]))
        if (curDate > dateStart and curDate < dateThru):
            games = day.find_all(class_="calendar-game")
            for game in games:
                try:
                    gameUrls.append("https://understat.com/" + game.find(class_="match-info")["href"])
                except:
                    pass
    if (temp.has_attr("disabled")):
        break
    browser.find_element_by_css_selector(".calendar-prev").click()
browser.quit()

count = 1
dict = {"Date":[],"Home":[],"Away":[],"Home Score":[],"Away Score":[],"Home xG":[],"Away xG":[],"Home shots":[],"Away shots":[],"Home on target":[],"Away on target":[],"Home deep":[],"Away deep":[],"Home ppda":[],"Away ppda":[],"Home xPts":[],"Away xPts":[]}
browser = webdriver.Chrome(executable_path='chromedriver.exe')
for game in gameUrls:
    browser.get(game)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    dict["Date"].append(soup.find_all("li")[5].string)
    dict["Home"].append(soup.find(class_="progress-home progress-over").find(class_="progress-value").string)
    dict["Away"].append(soup.find(class_="progress-away").find(class_="progress-value").string)
    dict["Home Score"].append(soup.find(class_="block-match-result").text.split(" - ")[0].split()[-1])
    dict["Away Score"].append(soup.find(class_="block-match-result").text.split(" - ")[1].split()[0][0])
    stats = soup.find_all(class_="progress-bar")
    dict["Home xG"].append(float(stats[3].find_all(class_="progress-value")[0].text))
    dict["Away xG"].append(float(stats[3].find_all(class_="progress-value")[1].text))
    dict["Home shots"].append(int(stats[4].find_all(class_="progress-value")[0].text))
    dict["Away shots"].append(int(stats[4].find_all(class_="progress-value")[1].text))
    dict["Home on target"].append(int(stats[5].find_all(class_="progress-value")[0].text))
    dict["Away on target"].append(int(stats[5].find_all(class_="progress-value")[1].text))
    dict["Home deep"].append(int(stats[6].find_all(class_="progress-value")[0].text))
    dict["Away deep"].append(int(stats[6].find_all(class_="progress-value")[1].text))
    dict["Home ppda"].append(float(stats[7].find_all(class_="progress-value")[0].text))
    dict["Away ppda"].append(float(stats[7].find_all(class_="progress-value")[1].text))
    dict["Home xPts"].append(float(stats[8].find_all(class_="progress-value")[0].text))
    dict["Away xPts"].append(float(stats[8].find_all(class_="progress-value")[1].text))
browser.quit()
#
understat = pd.DataFrame.from_dict(dict)
print (understat)
#
#



gameUrls = []
browser = webdriver.Chrome(executable_path='chromedriver.exe')
browser.get("https://www.whoscored.com/Regions/252/Tournaments/2/England-Premier-League")
time.sleep(3)
try:
    browser.find_element_by_css_selector(".qc-cmp-button").click()
    time.sleep(1)
    browser.find_element_by_css_selector(".qc-cmp-button.qc-cmp-save-and-exit").click()
    time.sleep(10)
    browser.get(season)
    time.sleep(3)
except:
    pass
while(1):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    table = soup.find(id="tournament-fixture").find(class_="divtable-body")
    inclDay = False
    for x in table.children:
        if (len(x.find_all(class_="col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 divtable-header")) != 0):
            d = x.find(class_="col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 divtable-header").string
            curDate = datetime.date(int(d.split()[3]), monthToInt(d.split()[1]), int(d.split()[2]))
            if (curDate > dateStart and curDate < dateThru):
                inclDay = True
            else:
                inclDay =  False
            continue
        if (inclDay):
            for tr in x.find_all("a"):
                if (tr.has_attr("href") and "Matches" in tr["href"] and "Live/" in tr["href"] and "https://www.whoscored.com" + tr["href"] not in gameUrls):
                    gameUrls.append("https://www.whoscored.com" + tr["href"])
    try:
        browser.find_element_by_css_selector(".previous.button.ui-state-default.rc-l.is-default").click()
        time.sleep(1)
    except:
        break
browser.quit()

dict = {"Date":[],"Home":[],"Away":[]}
sides = ["Home", "Away"]
for side in sides:
    dict[side + " Shots"] = []
    dict[side + " Woodwork"] = []
    dict[side + " On Target"] = []
    dict[side + " Shots Blocked"] = []
    dict[side + " Possession"] = []
    dict[side + " Touches"] = []
    dict[side + " Total Passes"] = []
    dict[side + " Accurate Passes"] = []
    dict[side + " Key Passes"] = []
    dict[side + " Dribbles Won"] = []
    dict[side + " Dribbles Attempted"] = []
    dict[side + " Successful Tackles"] = []
    dict[side + " Tackles Attempted"] = []
    dict[side + " Clearances"] = []
    dict[side + " Interceptions"] = []
    dict[side + " Corners"] = []
    dict[side + " Dispossessed"] = []
    dict[side + " Errors"] = []
    dict[side + " Fouls"] = []
    dict[side + " Offsides"] = []

    dict[side + " passtype_cross"] = []
    dict[side + " passtype_freekick"] = []
    dict[side + " passtype_corner"] = []
    dict[side + " passtype_through"] = []
    dict[side + " passtype_throw"] = []
    dict[side + " passlength_long"] = []
    dict[side + " passlength_short"] = []
    dict[side + " passheight_chipped"] = []
    dict[side + " passheight_ground"] = []
    dict[side + " passdirection_forward"] = []
    dict[side + " passdirection_backward"] = []
    dict[side + " passdirection_left"] = []
    dict[side + " passdirection_right"] = []
    dict[side + " passzone_defensive_third"] = []
    dict[side + " passzone_middle_third"] = []
    dict[side + " passzone_final_third"] = []

browser = webdriver.Chrome(executable_path='chromedriver.exe')
browser.get("https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/4311/England-Premier-League")
time.sleep(3)
try:
    browser.find_element_by_css_selector(".qc-cmp-button").click()
    time.sleep(1)
    browser.find_element_by_css_selector(".qc-cmp-button.qc-cmp-save-and-exit").click()
    time.sleep(3)
except:
    pass
for game in gameUrls:
    browser.get(game)
    time.sleep(2.5)
    gc.collect()
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    try:
        dict["Date"].append(soup.find_all(class_="info-block cleared")[2].find_all("dd")[1].string.split(", ")[1])
    except:
        browser.quit()
        time.sleep(300)
        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        browser.get("https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/4311/England-Premier-League")
        time.sleep(3)
        browser.find_element_by_css_selector(".qc-cmp-button").click()
        time.sleep(1)
        browser.find_element_by_css_selector(".qc-cmp-button.qc-cmp-save-and-exit").click()
        time.sleep(3)
        browser.get(game)
        time.sleep(30)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        dict["Date"].append(soup.find_all(class_="info-block cleared")[2].find_all("dd")[1].string.split(", ")[1])
    dict["Home"].append(soup.find_all(class_="team-link")[0].string)
    dict["Away"].append(soup.find_all(class_="team-link")[1].string)
    cats = soup.find_all(class_="match-centre-stat-details")
    try:
        dict["Home Shots"].append(int(cats[1].find_all("span")[0].string))
    except:
        browser.quit()
        time.sleep(300)
        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        browser.get("https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/4311/England-Premier-League")
        time.sleep(3)
        browser.find_element_by_css_selector(".qc-cmp-button").click()
        time.sleep(1)
        browser.find_element_by_css_selector(".qc-cmp-button.qc-cmp-save-and-exit").click()
        time.sleep(3)
        browser.get(game)
        time.sleep(30)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        cats = soup.find_all(class_="match-centre-stat-details")
        dict["Home Shots"].append(int(cats[1].find_all("span")[0].string))
    dict["Away Shots"].append(int(cats[1].find_all("span")[2].string))
    dict["Home Woodwork"].append(int(cats[1].find_all("span")[3].string))
    dict["Away Woodwork"].append(int(cats[1].find_all("span")[5].string))
    dict["Home On Target"].append(int(cats[1].find_all("span")[6].string))
    dict["Away On Target"].append(int(cats[1].find_all("span")[8].string))
    dict["Home Shots Blocked"].append(int(cats[1].find_all("span")[12].string))
    dict["Away Shots Blocked"].append(int(cats[1].find_all("span")[14].string))

    dict["Home Possession"].append(float(cats[2].find_all("span")[0].string))
    dict["Away Possession"].append(float(cats[2].find_all("span")[2].string))
    dict["Home Touches"].append(int(cats[2].find_all("span")[3].string))
    dict["Away Touches"].append(int(cats[2].find_all("span")[5].string))

    dict["Home Total Passes"].append(int(cats[3].find_all("span")[3].string))
    dict["Away Total Passes"].append(int(cats[3].find_all("span")[5].string))
    dict["Home Accurate Passes"].append(int(cats[3].find_all("span")[6].string))
    dict["Away Accurate Passes"].append(int(cats[3].find_all("span")[8].string))
    dict["Home Key Passes"].append(int(cats[3].find_all("span")[9].string))
    dict["Away Key Passes"].append(int(cats[3].find_all("span")[11].string))

    dict["Home Dribbles Won"].append(int(cats[4].find_all("span")[0].string))
    dict["Away Dribbles Won"].append(int(cats[4].find_all("span")[2].string))
    dict["Home Dribbles Attempted"].append(int(cats[4].find_all("span")[3].string))
    dict["Away Dribbles Attempted"].append(int(cats[4].find_all("span")[5].string))

    dict["Home Successful Tackles"].append(int(cats[6].find_all("span")[0].string))
    dict["Away Successful Tackles"].append(int(cats[6].find_all("span")[2].string))
    dict["Home Tackles Attempted"].append(int(cats[6].find_all("span")[3].string))
    dict["Away Tackles Attempted"].append(int(cats[6].find_all("span")[5].string))
    dict["Home Clearances"].append(int(cats[6].find_all("span")[12].string))
    dict["Away Clearances"].append(int(cats[6].find_all("span")[14].string))
    dict["Home Interceptions"].append(int(cats[6].find_all("span")[15].string))
    dict["Away Interceptions"].append(int(cats[6].find_all("span")[17].string))

    dict["Home Corners"].append(int(cats[7].find_all("span")[0].string))
    dict["Away Corners"].append(int(cats[7].find_all("span")[2].string))

    dict["Home Dispossessed"].append(int(cats[8].find_all("span")[0].string))
    dict["Away Dispossessed"].append(int(cats[8].find_all("span")[2].string))
    dict["Home Errors"].append(int(cats[8].find_all("span")[3].string))
    dict["Away Errors"].append(int(cats[8].find_all("span")[5].string))
    dict["Home Fouls"].append(int(cats[8].find_all("span")[6].string))
    dict["Away Fouls"].append(int(cats[8].find_all("span")[8].string))
    dict["Home Offsides"].append(int(cats[8].find_all("span")[9].string))
    dict["Away Offsides"].append(int(cats[8].find_all("span")[11].string))

    browser.find_element_by_link_text("Chalkboard").click()
    time.sleep(2.5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    passing = soup.find_all(class_="filterz-filter-group")[1]

    dict["Home passtype_cross"].append(int(passing.find_all("span")[0].string))
    dict["Away passtype_cross"].append(int(passing.find_all("span")[1].string))
    dict["Home passtype_freekick"].append(int(passing.find_all("span")[2].string))
    dict["Away passtype_freekick"].append(int(passing.find_all("span")[3].string))
    dict["Home passtype_corner"].append(int(passing.find_all("span")[4].string))
    dict["Away passtype_corner"].append(int(passing.find_all("span")[5].string))
    dict["Home passtype_through"].append(int(passing.find_all("span")[6].string))
    dict["Away passtype_through"].append(int(passing.find_all("span")[7].string))
    dict["Home passtype_throw"].append(int(passing.find_all("span")[8].string))
    dict["Away passtype_throw"].append(int(passing.find_all("span")[9].string))
    dict["Home passlength_long"].append(int(passing.find_all("span")[12].string))
    dict["Away passlength_long"].append(int(passing.find_all("span")[13].string))
    dict["Home passlength_short"].append(int(passing.find_all("span")[14].string))
    dict["Away passlength_short"].append(int(passing.find_all("span")[15].string))
    dict["Home passheight_chipped"].append(int(passing.find_all("span")[16].string))
    dict["Away passheight_chipped"].append(int(passing.find_all("span")[17].string))
    dict["Home passheight_ground"].append(int(passing.find_all("span")[18].string))
    dict["Away passheight_ground"].append(int(passing.find_all("span")[19].string))
    dict["Home passdirection_forward"].append(int(passing.find_all("span")[24].string))
    dict["Away passdirection_forward"].append(int(passing.find_all("span")[25].string))
    dict["Home passdirection_backward"].append(int(passing.find_all("span")[26].string))
    dict["Away passdirection_backward"].append(int(passing.find_all("span")[27].string))
    dict["Home passdirection_left"].append(int(passing.find_all("span")[28].string))
    dict["Away passdirection_left"].append(int(passing.find_all("span")[29].string))
    dict["Home passdirection_right"].append(int(passing.find_all("span")[30].string))
    dict["Away passdirection_right"].append(int(passing.find_all("span")[31].string))
    dict["Home passzone_defensive_third"].append(int(passing.find_all("span")[32].string))
    dict["Away passzone_defensive_third"].append(int(passing.find_all("span")[33].string))
    dict["Home passzone_middle_third"].append(int(passing.find_all("span")[34].string))
    dict["Away passzone_middle_third"].append(int(passing.find_all("span")[35].string))
    dict["Home passzone_final_third"].append(int(passing.find_all("span")[36].string))
    dict["Away passzone_final_third"].append(int(passing.find_all("span")[37].string))

browser.quit()
whoscored = pd.DataFrame.from_dict(dict)
print(whoscored)

homeS = []
awayS = []
homeXg = []
awayXg = []
homeDeep = []
awayDeep = []
homePpda = []
awayPpda = []
homeXpts = []
awayXpts = []

found = False
for index, row in whoscored.iterrows():
    date = datetime.datetime(2000+int(row["Date"].split("-")[2]), monthToInt(row["Date"].split("-")[1]), int(row["Date"].split("-")[0]))
    for index1, row1 in understat.iterrows():
        date1 = datetime.datetime(int(row1["Date"].split()[2]), monthToInt(row1["Date"].split()[0]), int(row1["Date"].split()[1]))
        if ((date == date1 or date + datetime.timedelta(days=1) == date1 or date == date1 + datetime.timedelta(days=1)) and standardizeTeamName(row1["Home"], para) == standardizeTeamName(row["Home"], para) and standardizeTeamName(row1["Away"], para) == standardizeTeamName(row["Away"], para)):
            found = True
            homeS.append(row1["Home Score"])
            awayS.append(row1["Away Score"])
            homeXg.append(row1["Home xG"])
            awayXg.append(row1["Away xG"])
            homeDeep.append(row1["Home deep"])
            awayDeep.append(row1["Away deep"])
            homePpda.append(row1["Home ppda"])
            awayPpda.append(row1["Away ppda"])
            homeXpts.append(row1["Home xPts"])
            awayXpts.append(row1["Away xPts"])
            break
    if (not found):
        print (row["Date"], row["Home"], row["Away"])
        homeS.append(np.nan)
        awayS.append(np.nan)
        homeXg.append(np.nan)
        awayXg.append(np.nan)
        homeDeep.append(np.nan)
        awayDeep.append(np.nan)
        homePpda.append(np.nan)
        awayPpda.append(np.nan)
        homeXpts.append(np.nan)
        awayXpts.append(np.nan)
    else:
        found = False
whoscored["Home Score"] = homeS
whoscored["Away Score"] = awayS
whoscored["Home xG"] = homeXg
whoscored["Home deep"] = homeDeep
whoscored["Home ppda"] = homePpda
whoscored["Home xPts"] = homeXpts
whoscored["Away xG"] = awayXg
whoscored["Away deep"] = awayDeep
whoscored["Away ppda"] = awayPpda
whoscored["Away xPts"] = awayXpts

print(whoscored)
whoscored.to_csv('../EPL_Csvs/2020-21_Season/match_stats/MW' + str(mwThru) + '.csv')
