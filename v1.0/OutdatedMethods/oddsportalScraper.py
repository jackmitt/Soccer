from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import date
import pandas as pd
import numpy as np
from miscFcns import oddsToDecimal
import copy
#
# dict = {"Date":[],"Home":[],"Away":[],"Home Score":[],"Away Score":[],"1":[],"X":[],"2":[]}
# dict["AH 0 (1)"] = []
# dict["AH 0 (2)"] = []
# for i in range(24):
#     for j in range(2):
#         dict["AH " + str((i+1)/(-4)) + " (" + str(j+1) + ")"] = []
# for i in range(24):
#     for j in range(2):
#         dict["AH " + str((i+1)/(4)) + " (" + str(j+1) + ")"] = []
# for i in range(36):
#     dict["Over " + str((i+1)/4)] = []
#     dict["Under " + str((i+1)/4)] = []


# years = []
# yr = 2008
# while (yr <= 2020):
#     years.append(yr)
#     yr += 1
# pages = [1,2,3,4,5,6,7,8]
# urls = []
# for i in range(len(years)):
#     if (years[i] == 2019):
#         break
#     for pg in pages:
#         urls.append("https://www.oddsportal.com/soccer/england/premier-league-" + str(years[i]) + "-" + str(years[i+1]) + "/results/#/page/" + str(pg))
gameUrls = []
# for url in urls:
#     browser = webdriver.Chrome(executable_path='chromedriver.exe')
#     browser.get(url)
#     soup = BeautifulSoup(browser.page_source, 'html.parser')
#     table = soup.find(class_="table-main")
#     rows = table.find_all('tr')
#     for row in rows:
#         if ("deactivate" in row["class"]):
#             temp = row.find(class_="name table-participant")
#             temp = temp.find("a")
#             gameUrls.append("https://www.oddsportal.com/" + temp["href"])
#     time.sleep(1)
#     browser.quit()

a = pd.DataFrame().from_csv("./gameurls.csv", encoding = "UTF-8")

gameUrls = a["GameUrls"].tolist()
for url in gameUrls:
     if ("chelsea-portsmouth-6wUVZEWq" in url or "west-ham-sunderland-zilXac7o" in url or "burnley-birmingham-W2XZM1nE" in url or "manchester-united-blackburn-OAJsRPyi" in url):
         gameUrls.remove(url)
dict = pd.DataFrame().from_csv("./SomeHistoricOdds.csv", encoding = "UTF-8")
gamesAccountedFor = len(dict["1"].tolist())
for i in reversed(range(len(gameUrls))):
    if (i < gamesAccountedFor):
        gameUrls.pop(i)

dict = dict.to_dict("list")
backUpDict = {}
for key in dict:
    backUpDict[key] = []
    for i in range(len(dict[key])):
        backUpDict[key].append(dict[key][i])


count = 1
miscCounter = 0
mlCounter = 0
ahCounter = 0
ouCounter = 0
forceQuit = False
miscBool = False
mlBool = False
ahBool = False
ouBool = False
betTypes = ["#1X2;2", "#ah;2", "#over-under;2"]
# tempDf = pd.DataFrame()
# tempDf["GameUrls"] = gameUrls
# tempDf.to_csv("./gameurls.csv")
for url in gameUrls:
    tempDf = pd.DataFrame().from_dict(dict)
    tempDf.to_csv("./SomeHistoricOdds.csv")
    print (str(count) + " out of " + str(len(gameUrls)) + " games")
    count += 1
    for type in betTypes:
        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        browser.get(url + "/" + type)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        if (type == "#1X2;2"):
            try:
                dict["Home"].append(soup.find("h1").string.split(" - ")[0])
                miscBool = True
                dict["Away"].append(soup.find("h1").string.split(" - ")[1])
                ps = soup.find_all("p")
                for p in ps:
                    if (p.has_attr("class")):
                        dateStr = p.string.split(", ")[1].split(",")[0].split()
                        dict["Date"].append(dateStr[1] + " " + dateStr[0] + ", " + dateStr[2])
                        break
                resultStr = soup.find(id="event-status").find("strong").string
                dict["Home Score"].append(resultStr.split(":")[0])
                dict["Away Score"].append(resultStr.split(":")[1])
            except:
                pass
            if (miscBool):
                miscCounter += 1
                for key in dict:
                    if (("Home" in key or "Away" in key or "Date" in key) and len(dict[key]) < miscCounter):
                        dict[key].append(np.nan)
                miscBool = False
            else:
                for key in dict:
                    if ("Home" in key or "Away" in key or "Date" in key):
                        dict[key].append(np.nan)
            table = soup.find("table")
            rows = table.find_all("tr")
            for row in rows:
                if (row.find(class_="name") != None):
                    if (row.find(class_="name").string == "Pinnacle"):
                        tds = row.find_all("td")
                        orderCount = 0
                        for td in tds:
                            try:
                                if (td.has_attr("class") and "odds" in td["class"]):
                                    if (orderCount == 0):
                                        dict["1"].append(oddsToDecimal(td.find("div").string))
                                        mlBool = True
                                    elif (orderCount == 1):
                                        dict["X"].append(oddsToDecimal(td.find("div").string))
                                        mlBool = True
                                    else:
                                        dict["2"].append(oddsToDecimal(td.find("div").string))
                                        mlBool = True
                                    orderCount += 1
                            except:
                                orderCount += 1
                                pass
            if (mlBool):
                mlCounter += 1
                for key in dict:
                    if (("1" in key or "X" in key or "2" in key) and len(dict[key]) < ahCounter):
                        dict[key].append(np.nan)
                mlBool = False
            else:
                for key in dict:
                    if ("1" in key or "X" in key or "2" in key):
                        dict[key].append(np.nan)
        if (type == "#ah;2"):
            rows = soup.find(id="odds-data-table").find_all("div")
            spreads = []
            for row in rows:
                if (row.find("a") == None):
                    continue
                try:
                    maybe = float(row.find("a").string.split("cap ")[1])
                except:
                    continue
                if (float(row.find("a").string.split("cap ")[1]) not in spreads and (row.find("a").string.split("cap ")[1][0] == "+" or row.find("a").string.split("cap ")[1][0] == "-")):
                    spreads.append(float(row.find("a").string.split("cap ")[1]))
                    try:
                        dict["AH " + str(float(row.find("a").string.split("cap ")[1])) + " (1)"].append(oddsToDecimal(row.find_all("a")[2].string))
                        dict["AH " + str(float(row.find("a").string.split("cap ")[1])) + " (2)"].append(oddsToDecimal(row.find_all("a")[1].string))
                        ahBool = True
                    except:
                        pass
            if (ahBool):
                ahCounter += 1
                for key in dict:
                    if ("AH" in key and len(dict[key]) < ahCounter):
                        dict[key].append(np.nan)
                ahBool = False
            else:
                for key in dict:
                    if ("AH" in key):
                        dict[key].append(np.nan)
        if (type == "#over-under;2"):
            rows = soup.find(id="odds-data-table").find_all("div")
            totals = []
            for row in rows:
                if (row.find("a") == None):
                    continue
                try:
                    maybe = row.find("a").string.split("der ")[1]
                except:
                    continue
                if (float(row.find("a").string.split("der ")[1]) not in totals):
                    totals.append(float(row.find("a").string.split("der ")[1]))
                    try:
                        dict["Over " + str(float(row.find("a").string.split("der ")[1]))].append(oddsToDecimal(row.find_all("a")[2].string))
                        dict["Under " + str(float(row.find("a").string.split("der ")[1]))].append(oddsToDecimal(row.find_all("a")[1].string))
                        ouBool = True
                    except:
                        pass
            if (ouBool):
                ouCounter += 1
                for key in dict:
                    if (("Over" in key or "Under" in key) and len(dict[key]) < ouCounter):
                        dict[key].append(np.nan)
                ouBool = False
            else:
                for key in dict:
                    if ("Over" in key or "Under" in key):
                        dict[key].append(np.nan)
            lengths = []
            for key in dict:
                lengths.append(len(dict[key]))
            for key in dict:
                if (len(dict[key]) < np.average(lengths)):
                    dict[key].append(np.nan)
            tempVal = len(dict["Date"])
            for key in dict:
                if (len(dict[key]) != tempVal):
                    print ("SOMETHING IS MESSED UP")
                    forceQuit = True
                    print (url)
                    break
            if (forceQuit):
                for key in dict:
                    print (key, len(dict[key]))
                    print ('BACKUP', key, len(backUpDict[key]))
                dict = {}
                for key in backUpDict:
                    dict[key] = []
                    for i in range(len(backUpDict[key])):
                        dict[key].append(backUpDict[key][i])
                for key in dict:
                    print (key, len(dict[key]))
                    print ('BACKUP', key, len(backUpDict[key]))
                forceQuit = False
            else:
                backUpDict = {}
                for key in dict:
                    backUpDict[key] = []
                    for i in range(len(dict[key])):
                        backUpDict[key].append(dict[key][i])
        time.sleep(1)
        browser.quit()
dfFinal = pd.DataFrame.from_dict(dict)
dfFinal.to_csv("./EPLHistoricOdds.csv")
