from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import date
import pandas as pd
import numpy as np
from miscFcns import oddsToDecimal
import gc
#from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

# seasonUrls = ["https://www.whoscored.com/Regions/108/Tournaments/5/Seasons/5441/Italy-Serie-A", "https://www.whoscored.com/Regions/108/Tournaments/5/Seasons/5970/Italy-Serie-A", "https://www.whoscored.com/Regions/108/Tournaments/5/Seasons/6461/Italy-Serie-A", "https://www.whoscored.com/Regions/108/Tournaments/5/Seasons/6974/Italy-Serie-A", "https://www.whoscored.com/Regions/108/Tournaments/5/Seasons/7468/Italy-Serie-A"]
# gameUrls = []
# # req_proxy = RequestProxy()
# # proxies = req_proxy.get_proxy_list()
# # proxyUseCount = 2
# browser = webdriver.Chrome(executable_path='chromedriver.exe')
# for season in seasonUrls:
#     # PROXY = proxies[proxyUseCount].get_address()
#     # proxyUseCount += 1
#     # webdriver.DesiredCapabilities.CHROME['proxy']={
#     #     "httpProxy":PROXY,
#     #     "ftpProxy":PROXY,
#     #     "sslProxy":PROXY,
#     #     "proxyType":"MANUAL",
#     # }
#     browser.get(season)
#     time.sleep(3)
#     try:
#         browser.find_element_by_css_selector(".qc-cmp-button").click()
#         time.sleep(1)
#         browser.find_element_by_css_selector(".qc-cmp-button.qc-cmp-save-and-exit").click()
#         time.sleep(10)
#         browser.get(season)
#         time.sleep(3)
#     except:
#         pass
#     while(1):
#         soup = BeautifulSoup(browser.page_source, 'html.parser')
#         table = soup.find(id="tournament-fixture")
#         for tr in table.find_all("a"):
#             if (tr.has_attr("href") and "Matches" in tr["href"] and "Live" in tr["href"] and "https://www.whoscored.com" + tr["href"] not in gameUrls):
#                 gameUrls.append("https://www.whoscored.com" + tr["href"])
#         try:
#             browser.find_element_by_css_selector(".previous.button.ui-state-default.rc-l.is-default").click()
#         except:
#             break
# browser.quit()
# tempDict = {"Urls":gameUrls}
# print (gameUrls)
# dfFinal = pd.DataFrame.from_dict(tempDict)
# dfFinal.to_csv("./whoscoredGameUrlsSA.csv")

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
#
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
gameUrlDict = pd.DataFrame().from_csv("./whoscoredGameUrlsSA.csv", encoding = "UTF-8")
gameUrlDict = gameUrlDict.to_dict("list")
dict = pd.DataFrame().from_csv("./whoscoredGameStatsSA.csv", encoding = "UTF-8")
dict = dict.to_dict("list")
gamesAccountedFor = len(dict["Date"])
for i in reversed(range(len(gameUrlDict["Urls"]))):
    if (i < gamesAccountedFor):
        gameUrlDict["Urls"].pop(i)
for game in gameUrlDict["Urls"]:
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
    for key in dict:
        print (key, len(dict[key]))
    dfFinal = pd.DataFrame.from_dict(dict)
    dfFinal.to_csv("./whoscoredGameStatsSA.csv")
browser.quit()
