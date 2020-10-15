from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import numpy as np
from miscFcns import oddsToDecimal
import copy
from miscFcns import monthToInt

dict = {"Date":[],"Home":[],"Away":[],"1":[],"X":[],"2":[]}
dict["AH 0 (1)"] = []
dict["AH 0 (2)"] = []
for i in range(24):
    for j in range(2):
        dict["AH " + str((i+1)/(-4)) + " (" + str(j+1) + ")"] = []
for i in range(24):
    for j in range(2):
        dict["AH " + str((i+1)/(4)) + " (" + str(j+1) + ")"] = []
for i in range(36):
    dict["Over " + str((i+1)/4)] = []
    dict["Under " + str((i+1)/4)] = []


gameUrls = []

#change every week - matchweek for predictions
inMW = False
mw = 5
intBreakCount = 1
dateStart = datetime.date(2020, 9, 11) + datetime.timedelta(days=7*(mw-1+intBreakCount))
dateThru = datetime.date(2020, 9, 11) + datetime.timedelta(days=7*(mw+intBreakCount))
browser = webdriver.Chrome(executable_path='chromedriver.exe')
browser.get("https://www.oddsportal.com/soccer/england/premier-league/")
soup = BeautifulSoup(browser.page_source, 'html.parser')
table = soup.find(class_="table-main")
rows = table.find_all("tr")
for row in rows:
    if (len(row.find_all(class_="first2 tl")) != 0):
        if (not "England" in row.find(class_="first2 tl").text):
            d = row.find(class_="first2 tl").text
            curDate = datetime.date(int(d.split()[2]), monthToInt(d.split()[1]), int(d.split()[0]))
            if (curDate < dateThru and curDate > dateStart):
                inMW = True
            else:
                inMW = False
    if (inMW):
        if (len(row.find_all("a")) != 0):
            temp = row.find("a")
            gameUrls.append("https://www.oddsportal.com" + temp["href"])


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
betTypes = ["#1X2;2","#ah;2","#over-under;2"]
for type in betTypes:
    for url in gameUrls:
        if (type == "#1X2;2"):
            browser.get(url + "/" + type)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            dict["Home"].append(soup.find("h1").string.split(" - ")[0])
            dict["Away"].append(soup.find("h1").string.split(" - ")[1])
            ps = soup.find_all("p")
            for p in ps:
                if (p.has_attr("class")):
                    dateStr = p.string.split(", ")[1].split(",")[0].split()
                    dict["Date"].append(dateStr[1] + " " + dateStr[0] + ", " + dateStr[2])
                    break
            table = soup.find("table")
            rows = table.find_all("tr")
            for row in rows:
                if (row.find(class_="name") != None):
                    if (row.find(class_="name").string == "Pinnacle"):
                        tds = row.find_all("a")
                        orderCount = 0
                        for td in tds:
                            if (td.has_attr("class") and td["class"][0] == "betslip"):
                                mlBool = True
                                if (orderCount == 0):
                                    dict["1"].append(oddsToDecimal(td.string))
                                elif (orderCount == 1):
                                    dict["X"].append(oddsToDecimal(td.string))
                                else:
                                    dict["2"].append(oddsToDecimal(td.string))
                                orderCount += 1
            if (not mlBool):
                dict["1"].append(np.nan)
                dict["X"].append(np.nan)
                dict["2"].append(np.nan)
            else:
                mlBool = False
        if (type == "#ah;2"):
            browser.get(url + "/" + type)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            rows = soup.find(id="odds-data-table").find_all(class_="table-container")
            for i in range(len(rows)):
                try:
                    browser.find_element_by_link_text("Compare odds").click()
                except:
                    break
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            time.sleep(10)
            for i in range(len(rows)):
                try:
                    row = soup.find(id="odds-data-table").find_all(class_="table-container")[i]
                    subR = row.find("tbody").find_all("tr")
                    for r in subR:
                        if (len(r.find_all(class_="name")) != 0 and r.find(class_="name").string == "Pinnacle" and r.text[-1] == "%"):
                            dict["AH " + str(float(r.find(class_="center").string)) + " (1)"].append(oddsToDecimal(r.find_all("a")[3].string))
                            dict["AH " + str(float(r.find(class_="center").string)) + " (2)"].append(oddsToDecimal(r.find_all("a")[4].string))
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
            browser.get(url + "/" + type)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            rows = soup.find(id="odds-data-table").find_all(class_="table-container")
            totals = []
            for i in range(len(rows)):
                try:
                    browser.find_element_by_link_text("Compare odds").click()
                except:
                    break
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            for i in range(len(rows)):
                row = soup.find(id="odds-data-table").find_all(class_="table-container")[i]
                if (row.find("a") == None):
                    continue
                try:
                    maybe = row.find("a").string.split("der ")[1]
                except:
                    continue
                if (float(row.find("a").string.split("der ")[1]) not in totals):
                    try:
                        subR = row.find("tbody").find_all("tr")
                    except:
                        continue
                    totals.append(float(maybe))
                    for r in subR:
                        if (len(r.find_all(class_="name")) != 0 and r.find(class_="name").string == "Pinnacle" and r.text[-1] == "%"):
                            dict["Over " + str(float(maybe))].append(oddsToDecimal(r.find_all("a")[3].string))
                            dict["Under " + str(float(maybe))].append(oddsToDecimal(r.find_all("a")[4].string))
                            ouBool = True
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
browser.quit()
for key in dict:
    print (key, len(dict[key]))
dfFinal = pd.DataFrame.from_dict(dict)
dfFinal.to_csv('../EPL_Csvs/2020-21_Season/match_odds/MW' + str(mw) + '.csv')
