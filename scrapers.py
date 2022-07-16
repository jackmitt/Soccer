from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from os.path import exists
import os
import datetime
from dateutil.relativedelta import relativedelta
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pickle
from helpers import Database
from helpers import standardizeTeamName

def nowgoal(league):
    A = Database(["Date","Home","Away","Open 1","Open X","Open 2","Close 1","Close X","Close 2","Open AH","Home Open AH Odds","Away Open AH Odds","Close AH","Home Close AH Odds","Away Close AH Odds","Open OU","Under Open OU Odds","Over Open OU Odds","Close OU","Under Close OU Odds","Over Close OU Odds","Home Score","Away Score","url"])
    driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1325x744")
    browser = webdriver.Chrome(executable_path=driver_path, options = chrome_options)
    browser.maximize_window()
    if (not exists("./nowgoal_gameUrls/" + league + "_new.csv")):
        oneyear = False
        if (league == "England1"):
            url = "https://football.nowgoal5.com/League/2008-2009/36"
            playoff = False
        elif (league == "England2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/37"
            playoff = True
        elif (league == "England3"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/39"
            playoff = True
        elif (league == "England4"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/35"
            playoff = True
        elif (league == "Italy1"):
            url = "https://football.nowgoal5.com/League/2008-2009/34"
            playoff = False
        elif (league == "Italy2"):
            url = "https://football.nowgoal5.com/subleague/2008-2009/40"
            playoff = True
        elif (league == "Spain1"):
            url = "https://football.nowgoal5.com/League/2008-2009/31"
            playoff = False
        elif (league == "Spain2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/33"
            playoff = True
        elif (league == "Germany1"):
            url = "https://football.nowgoal5.com/League/2008-2009/8"
            playoff = False
        elif (league == "Germany2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/9"
            playoff = True
        elif (league == "Germany3"):
            url = "https://football.nowgoal5.com/League/2008-2009/693"
            playoff = False
        elif (league == "France1"):
            url = "https://football.nowgoal5.com/League/2008-2009/11"
            playoff = False
        elif (league == "France2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/12"
            playoff = True
        elif (league == "France3"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/203"
            playoff = True
        elif (league == "Portugal1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/23"
            playoff = True
        elif (league == "Portugal2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/157"
            playoff = True
        elif (league == "Scotland1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/29"
            playoff = True
        elif (league == "Scotland2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/150"
            playoff = True
        elif (league == "Netherlands1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/16"
            playoff = True
        elif (league == "Netherlands2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/17"
            playoff = True
        elif (league == "Belgium1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/5"
            playoff = True
        elif (league == "Belgium2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/138"
            playoff = True
        elif (league == "Sweden1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/26"
            oneyear = True
            playoff = True
        elif (league == "Sweden2"):
            url = "https://football.nowgoal5.com/SubLeague/2008/122"
            oneyear = True
            playoff = True
        elif (league == "Finland1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/13"
            oneyear = True
            playoff = True
        elif (league == "Finland2"):
            url = "https://football.nowgoal5.com/SubLeague/2008/212"
            oneyear = True
            playoff = True
        elif (league == "Norway1"):
            url = "https://football.nowgoal5.com/League/2008/22"
            playoff = False
            oneyear = True
        elif (league == "Norway2"):
            url = "https://football.nowgoal5.com/SubLeague/2008/123"
            playoff = True
            oneyear = True
        elif (league == "Denmark1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/7"
            playoff = True
        elif (league == "Denmark2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/127"
            playoff = True
        elif (league == "Austria1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/3"
            playoff = True
        elif (league == "Austria2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/128"
            playoff = True
        elif (league == "Ireland1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/1"
            playoff = True
            oneyear = True
        elif (league == "Ireland2"):
            url = "https://football.nowgoal5.com/SubLeague/2008/139"
            playoff = True
            oneyear = True
        elif (league == "NorthernIreland1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/165"
            playoff = True
        elif (league == "Switzerland1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/27"
            playoff = True
        elif (league == "Switzerland2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/121"
            playoff = True
        elif (league == "Russia1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/10"
            playoff = True
            oneyear = True
        elif (league == "Russia2"):
            url = "https://football.nowgoal5.com/SubLeague/2008/235"
            playoff = True
            oneyear = True
        elif (league == "Poland1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/6"
            playoff = True
        elif (league == "Poland2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/221"
            playoff = True
        elif (league == "Ukraine1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/119"
            playoff = True
        elif (league == "Czech1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/137"
            playoff = True
        elif (league == "Czech2"):
            url = "https://football.nowgoal5.com/League/2008-2009/290"
            playoff = False
        elif (league == "Greece1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/32"
            playoff = True
        elif (league == "Romania1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/124"
            playoff = True
        elif (league == "Slovakia1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/132"
            playoff = True
        elif (league == "Slovakia2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/351"
            playoff = True
        elif (league == "Iceland1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/166"
            playoff = True
            oneyear = True
        elif (league == "Israel1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/118"
            playoff = True
        elif (league == "Israel2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/160"
            playoff = True
        elif (league == "Belarus1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/230"
            playoff = True
            oneyear = True
        elif (league == "Lithuania1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/217"
            playoff = True
            oneyear = True
        elif (league == "Turkey1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/30"
            playoff = True
        elif (league == "Turkey2"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/130"
            playoff = True
        elif (league == "Wales1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/135"
            playoff = True
        elif (league == "Hungary1"):
            url = "https://football.nowgoal5.com/League/2008-2009/136"
            playoff = False
        elif (league == "Croatia1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/133"
            playoff = True
        elif (league == "Bulgaria1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/131"
            playoff = True
        elif (league == "Slovenia1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/247"
            playoff = True
        elif (league == "Cyprus1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/159"
            playoff = True
        elif (league == "Serbia1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/129"
            playoff = True
        elif (league == "Albania1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/315"
            playoff = True
        elif (league == "Kazakhstan1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/466"
            playoff = True
            oneyear = True
        elif (league == "Bosnia1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/352"
            playoff = True
        elif (league == "Estonia1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/353"
            playoff = True
            oneyear = True
        elif (league == "Montenegro1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/562"
            playoff = True
        elif (league == "USA1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/21"
            playoff = True
            oneyear = True
        elif (league == "Brazil1"):
            url = "https://football.nowgoal5.com/League/2008/4"
            playoff = False
            oneyear = True
        elif (league == "Brazil2"):
            url = "https://football.nowgoal5.com/League/2008/358"
            playoff = False
            oneyear = True
        elif (league == "Japan1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/25"
            playoff = True
            oneyear = True
        elif (league == "Japan2"):
            url = "https://football.nowgoal5.com/SubLeague/2008/284"
            playoff = True
            oneyear = True
        elif (league == "Korea1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/15"
            playoff = True
            oneyear = True
        elif (league == "Australia1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/273"
            playoff = True
        elif (league == "Australia2"):
            url = "https://football.nowgoal5.com/SubLeague/2008/616"
            playoff = True
            oneyear = True
        elif (league == "Iran1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/279"
            playoff = True
        elif (league == "UAE1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/301"
            playoff = True
        elif (league == "Singapore1"):
            url = "https://football.nowgoal5.com/SubLeague/2008/194"
            playoff = True
            oneyear = True
        elif (league == "Qatar1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/313"
            playoff = True
        elif (league == "SouthAfrica1"):
            url = "https://football.nowgoal5.com/SubLeague/2008-2009/308"
            playoff = True
        elif (league == "Morocco1"):
            url = "https://football.nowgoal5.com/League/2008-2009/321"
            playoff = False
        elif (league == "Algeria1"):
            url = "https://football.nowgoal5.com/League/2008-2009/193"
            playoff = False

        if (oneyear):
            rootier = url.split("2008")[0]
        else:
            rootier = url.split("2008-2009")[0]
        league_num = url.split("/")[5]
        curSeason = "2021-2022"
        gameUrls = []
        while (curSeason != "2022-2023"):
            if ((league == "Russia1" or league == "Russia2") and curSeason == "2011-2012"):
                oneyear = False
            if (oneyear):
                browser.get(rootier + curSeason.split("-")[0] + "/" + league_num)
            else:
                browser.get(rootier + curSeason + "/" + league_num)
            time.sleep(1)
            if (playoff):
                try:
                    browser.find_element_by_xpath("//*[@id='SubSelectDiv']/ul/li[1]").click()
                except:
                    browser.find_element_by_xpath("//*[@id='SubSelectDiv']/ul/li").click()
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            i = 1
            j = 2
            while (1):
                try:
                    browser.find_element_by_xpath("//*[@id='Table2']/tbody/tr[" + str(i) + "]/td[" + str(j) + "]").click()
                    time.sleep(0.5)
                except:
                    if (i == 1):
                        i = 2
                        j = 1
                        continue
                    else:
                        curSeason = curSeason.split("-")[1] + "-" + str(int(curSeason.split("-")[1]) + 1)
                        break
                soup = BeautifulSoup(browser.page_source, 'html.parser')
                for t in soup.find_all(class_="odds-icon"):
                    gameUrls.append(t['href'])
                j += 1
        save = {}
        save["urls"] = gameUrls
        dfFinal = pd.DataFrame.from_dict(save)
        dfFinal = dfFinal.drop_duplicates()
        dfFinal.to_csv("./nowgoal_gameUrls/" + league + "_new.csv", index = False)

    else:
        gameUrls = pd.read_csv("./nowgoal_gameUrls/" + league + ".csv", encoding = "ISO-8859-1")["urls"].tolist()
    #
    #
    # counter = 0
    # if (exists("./csv_data/" + league + "/betting.csv")):
    #     A.initDictFromCsv("./csv_data/" + league + "/betting.csv")
    #     scrapedGames = pd.read_csv('./csv_data/' + league + '/betting.csv', encoding = "ISO-8859-1")["url"].tolist()
    #     for game in scrapedGames:
    #         gameUrls.remove(game)
    # #
    # for game in gameUrls:
    #     browser.get("https:" + game)
    #     soup = BeautifulSoup(browser.page_source, 'html.parser')
    #     try:
    #         A.addCellToRow(soup.find(id="headStr").find("span").text.split()[0])
    #         A.addCellToRow(soup.find_all(class_="o_team")[0].text)
    #         A.addCellToRow(soup.find_all(class_="o_team")[1].text)
    #         try:
    #             A.addCellToRow(soup.find_all(class_="odds-table-bg")[4].find_all("tr")[-2].find_all("td")[1].text)
    #             A.addCellToRow(soup.find_all(class_="odds-table-bg")[4].find_all("tr")[-2].find_all("td")[2].text)
    #             A.addCellToRow(soup.find_all(class_="odds-table-bg")[4].find_all("tr")[-1].find_all("td")[1].text)
    #             A.addCellToRow(soup.find_all(class_="odds-table-bg")[4].find_all("tr")[-1].find_all("td")[2].text)
    #         except:
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #         try:
    #             bet365 = soup.find(class_="odds-table-bg").find_all("tr")[5]
    #             test = float(bet365.find_all("td")[2].find("span").text) * -1
    #             test = float(bet365.find_all("td")[2].find("span").text) * -1
    #         except:
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(soup.find_all(class_="team_bf")[0].text)
    #             A.addCellToRow(soup.find_all(class_="team_bf")[1].text)
    #             A.addCellToRow(game)
    #             A.appendRow()
    #             continue
    #         try:
    #             A.addCellToRow(float(bet365.find_all("td")[2].text.replace(bet365.find_all("td")[2].find("span").text, "")) * -1)
    #         except:
    #             A.addCellToRow(float(bet365.find_all("td")[2].find("span").text) * -1)
    #         A.addCellToRow(float(bet365.find_all("td")[1].find_all("span")[0].text) + 1)
    #         A.addCellToRow(float(bet365.find_all("td")[3].find_all("span")[0].text) + 1)
    #         A.addCellToRow(float(bet365.find_all("td")[2].find("span").text) * -1)
    #         A.addCellToRow(float(bet365.find_all("td")[1].find_all("span")[1].text) + 1)
    #         A.addCellToRow(float(bet365.find_all("td")[3].find_all("span")[1].text) + 1)
    #         try:
    #             test = float(bet365.find_all("td")[4].find_all("span")[0].text)
    #         except:
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(np.nan)
    #             A.addCellToRow(soup.find_all(class_="team_bf")[0].text)
    #             A.addCellToRow(soup.find_all(class_="team_bf")[1].text)
    #             A.addCellToRow(game)
    #             A.appendRow()
    #             continue
    #         try:
    #             A.addCellToRow(float(bet365.find_all("td")[5].text.replace(bet365.find_all("td")[5].find("span").text, "")))
    #         except:
    #             A.addCellToRow(float(bet365.find_all("td")[5].find("span").text))
    #         A.addCellToRow(float(bet365.find_all("td")[4].find_all("span")[0].text) + 1)
    #         A.addCellToRow(float(bet365.find_all("td")[6].find_all("span")[0].text) + 1)
    #         A.addCellToRow(float(bet365.find_all("td")[5].find("span").text))
    #         A.addCellToRow(float(bet365.find_all("td")[4].find_all("span")[1].text) + 1)
    #         A.addCellToRow(float(bet365.find_all("td")[6].find_all("span")[1].text) + 1)
    #         A.addCellToRow(soup.find_all(class_="team_bf")[0].text)
    #         A.addCellToRow(soup.find_all(class_="team_bf")[1].text)
    #         A.addCellToRow(game)
    #         A.appendRow()
    #         counter += 1
    #         if (counter % 20 == 1):
    #             A.dictToCsv("./csv_data/" + league + "_spreads.csv")
    #     except:
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(np.nan)
    #         A.addCellToRow(game)
    #         A.appendRow()
    # # except:
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(np.nan)
    # #     A.addCellToRow(game)
    # #     A.appendRow()
    # #     A.dictToCsv("./csv_data/" + league + "_spreads.csv")
    # #     nowgoal(urlRoot, startMonth, league)
    # A.dictToCsv("./csv_data/" + league + "/betting.csv")
    # browser.close()

def nowgoalPt2(league):
    if (not exists("./csv_data/" + league)):
        os.makedirs("./csv_data/" + league)
    A = Database(["Date","Home","Away","Home Score","Away Score","Open 1","Open X","Open 2","Close 1","Close X","Close 2","1X2 Book","Open AH","Home Open AH Odds","Away Open AH Odds","Close AH","Home Close AH Odds","Away Close AH Odds","AH Book","Open OU","Over Open OU Odds","Under Open OU Odds","Close OU","Over Close OU Odds","Under Close OU Odds","OU Book","url"])
    driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1325x744")
    browser = webdriver.Chrome(executable_path=driver_path, options = chrome_options)
    browser.maximize_window()
    gameUrls = pd.read_csv("./nowgoal_gameUrls/" + league + ".csv", encoding = "ISO-8859-1")["urls"].tolist()
    if (exists("./nowgoal_gameUrls/" + league + "_new.csv")):
        newurls = pd.read_csv("./nowgoal_gameUrls/" + league + "_new.csv", encoding = "ISO-8859-1")["urls"].tolist()
        for url in newurls:
            gameUrls.append(url)
    #
    #
    counter = 0
    if (exists("./csv_data/" + league + "/betting.csv")):
        A.initDictFromCsv("./csv_data/" + league + "/betting.csv")
        scrapedGames = pd.read_csv('./csv_data/' + league + '/betting.csv', encoding = "ISO-8859-1")["url"].tolist()
        for game in scrapedGames:
            gameUrls.remove(game)
    #
    for game in gameUrls:
        browser.get("https:" + game)
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        #try:
        fullDate = soup.find(class_="LName").find_next_sibling()["data-t"].split()[0]
        try:
            fail = soup.find_all(class_="score")[0].text
        except IndexError:
            continue
        A.addCellToRow(datetime.date(int(fullDate.split("/")[2]), int(fullDate.split("/")[0]), int(fullDate.split("/")[1])))
        A.addCellToRow(soup.find_all(class_="sclassName")[0].find("a").text[1:])
        A.addCellToRow(soup.find_all(class_="sclassName")[1].find("a").text[1:])
        A.addCellToRow(soup.find_all(class_="score")[0].text)
        A.addCellToRow(soup.find_all(class_="score")[1].text)
        for row in soup.find_all(class_="odds-table-bg")[0].find_all("tr"):
            if ("oods-bg" in row["class"][0]):
                if (row.find("td").text.split()[0] == "Bet365"):
                    try:
                        hOddsLen = int(len(row.find_all("td")[4].text) / 2)
                        dOddsLen = int(len(row.find_all("td")[5].text) / 2)
                        aOddsLen = int(len(row.find_all("td")[6].text) / 2)
                        A.addCellToRow(row.find_all("td")[4].text[0:hOddsLen])
                        A.addCellToRow(row.find_all("td")[5].text[0:dOddsLen])
                        A.addCellToRow(row.find_all("td")[6].text[0:aOddsLen])
                        A.addCellToRow(row.find_all("td")[4].text[hOddsLen:hOddsLen*2])
                        A.addCellToRow(row.find_all("td")[5].text[dOddsLen:dOddsLen*2])
                        A.addCellToRow(row.find_all("td")[6].text[aOddsLen:aOddsLen*2])
                        A.addCellToRow(row.find("td").text.split()[0])
                    except:
                        found = False
                        for r in soup.find_all(class_="odds-table-bg")[0].find_all("tr"):
                            try:
                                hOddsLen = int(len(r.find_all("td")[4].text) / 2)
                                dOddsLen = int(len(r.find_all("td")[5].text) / 2)
                                aOddsLen = int(len(r.find_all("td")[6].text) / 2)
                                A.addCellToRow(r.find_all("td")[4].text[0:hOddsLen])
                                A.addCellToRow(r.find_all("td")[5].text[0:dOddsLen])
                                A.addCellToRow(r.find_all("td")[6].text[0:aOddsLen])
                                A.addCellToRow(r.find_all("td")[4].text[hOddsLen:hOddsLen*2])
                                A.addCellToRow(r.find_all("td")[5].text[dOddsLen:dOddsLen*2])
                                A.addCellToRow(r.find_all("td")[6].text[aOddsLen:aOddsLen*2])
                                A.addCellToRow(r.find("td").text.split()[0])
                                found = True
                                break
                            except:
                                continue
                        if (not found):
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)


                    try:
                        if ("/" in row.find_all("td")[2].find_all("span")[0].text):
                            if ("-" in row.find_all("td")[2].find_all("span")[0].text):
                                spread = 0 - round((abs(float(row.find_all("td")[2].find_all("span")[0].text.split("/")[0])) + abs(float(row.find_all("td")[2].find_all("span")[0].text.split("/")[1]))) / 2, 2)
                            else:
                                spread = round((float(row.find_all("td")[2].find_all("span")[0].text.split("/")[0]) + float(row.find_all("td")[2].find_all("span")[0].text.split("/")[1])) / 2, 2)
                        else:
                            spread = row.find_all("td")[2].find_all("span")[0].text
                        A.addCellToRow(spread)
                        A.addCellToRow(round(float(row.find_all("td")[1].find_all("span")[0].text) + 1,2))
                        A.addCellToRow(round(float(row.find_all("td")[3].find_all("span")[0].text) + 1,2))
                        if ("/" in row.find_all("td")[2].find_all("span")[1].text):
                            if ("-" in row.find_all("td")[2].find_all("span")[1].text):
                                spread = 0 - round((abs(float(row.find_all("td")[2].find_all("span")[1].text.split("/")[0])) + abs(float(row.find_all("td")[2].find_all("span")[1].text.split("/")[1]))) / 2, 2)
                            else:
                                spread = round((float(row.find_all("td")[2].find_all("span")[1].text.split("/")[0]) + float(row.find_all("td")[2].find_all("span")[1].text.split("/")[1])) / 2, 2)
                        else:
                            spread = row.find_all("td")[2].find_all("span")[1].text
                        A.addCellToRow(spread)
                        A.addCellToRow(round(float(row.find_all("td")[1].find_all("span")[1].text) + 1,2))
                        A.addCellToRow(round(float(row.find_all("td")[3].find_all("span")[1].text) + 1,2))
                        A.addCellToRow(row.find("td").text.split()[0])
                    except:
                        found = False
                        for r in soup.find_all(class_="odds-table-bg")[0].find_all("tr"):
                            try:
                                if ("/" in r.find_all("td")[2].find_all("span")[0].text):
                                    if ("-" in r.find_all("td")[2].find_all("span")[0].text):
                                        spread = 0 - round((abs(float(r.find_all("td")[2].find_all("span")[0].text.split("/")[0])) + abs(float(r.find_all("td")[2].find_all("span")[0].text.split("/")[1]))) / 2, 2)
                                    else:
                                        spread = round((float(r.find_all("td")[2].find_all("span")[0].text.split("/")[0]) + float(r.find_all("td")[2].find_all("span")[0].text.split("/")[1])) / 2, 2)
                                else:
                                    spread = r.find_all("td")[2].find_all("span")[0].text
                                A.addCellToRow(spread)
                                A.addCellToRow(round(float(r.find_all("td")[1].find_all("span")[0].text) + 1,2))
                                A.addCellToRow(round(float(r.find_all("td")[3].find_all("span")[0].text) + 1,2))
                                if ("/" in r.find_all("td")[2].find_all("span")[1].text):
                                    if ("-" in r.find_all("td")[2].find_all("span")[1].text):
                                        spread = 0 - round((abs(float(r.find_all("td")[2].find_all("span")[1].text.split("/")[0])) + abs(float(r.find_all("td")[2].find_all("span")[1].text.split("/")[1]))) / 2, 2)
                                    else:
                                        spread = round((float(r.find_all("td")[2].find_all("span")[1].text.split("/")[0]) + float(r.find_all("td")[2].find_all("span")[1].text.split("/")[1])) / 2, 2)
                                else:
                                    spread = r.find_all("td")[2].find_all("span")[1].text
                                A.addCellToRow(spread)
                                A.addCellToRow(round(float(r.find_all("td")[1].find_all("span")[1].text) + 1,2))
                                A.addCellToRow(round(float(r.find_all("td")[3].find_all("span")[1].text) + 1,2))
                                A.addCellToRow(r.find("td").text.split()[0])
                                found = True
                                break
                            except:
                                continue
                        if (not found):
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)


                    try:
                        if (".5/" in row.find_all("td")[8].find_all("span")[0].text):
                            total = row.find_all("td")[8].find_all("span")[0].text[0] + ".75"
                        elif ("/" in row.find_all("td")[8].find_all("span")[0].text):
                            total = row.find_all("td")[8].find_all("span")[0].text[0] + ".25"
                        else:
                            total = row.find_all("td")[8].find_all("span")[0].text
                        A.addCellToRow(total)
                        A.addCellToRow(round(float(row.find_all("td")[7].find_all("span")[0].text) + 1,2))
                        A.addCellToRow(round(float(row.find_all("td")[9].find_all("span")[0].text) + 1,2))
                        if (".5/" in row.find_all("td")[8].find_all("span")[1].text):
                            total = row.find_all("td")[8].find_all("span")[1].text[0] + ".75"
                        elif ("/" in row.find_all("td")[8].find_all("span")[1].text):
                            total = row.find_all("td")[8].find_all("span")[1].text[0] + ".25"
                        else:
                            total = row.find_all("td")[8].find_all("span")[1].text
                        A.addCellToRow(total)
                        A.addCellToRow(round(float(row.find_all("td")[7].find_all("span")[1].text) + 1,2))
                        A.addCellToRow(round(float(row.find_all("td")[9].find_all("span")[1].text) + 1,2))
                        A.addCellToRow(row.find("td").text.split()[0])
                    except:
                        found = False
                        for r in soup.find_all(class_="odds-table-bg")[0].find_all("tr"):
                            try:
                                if (".5/" in r.find_all("td")[8].find_all("span")[0].text):
                                    total = r.find_all("td")[8].find_all("span")[0].text[0] + ".75"
                                elif ("/" in r.find_all("td")[8].find_all("span")[0].text):
                                    total = r.find_all("td")[8].find_all("span")[0].text[0] + ".25"
                                else:
                                    total = r.find_all("td")[8].find_all("span")[0].text
                                A.addCellToRow(total)
                                A.addCellToRow(round(float(r.find_all("td")[7].find_all("span")[0].text) + 1,2))
                                A.addCellToRow(round(float(r.find_all("td")[9].find_all("span")[0].text) + 1,2))
                                if (".5/" in r.find_all("td")[8].find_all("span")[1].text):
                                    total = r.find_all("td")[8].find_all("span")[1].text[0] + ".75"
                                elif ("/" in r.find_all("td")[8].find_all("span")[1].text):
                                    total = r.find_all("td")[8].find_all("span")[1].text[0] + ".25"
                                else:
                                    total = r.find_all("td")[8].find_all("span")[1].text
                                A.addCellToRow(total)
                                A.addCellToRow(round(float(r.find_all("td")[7].find_all("span")[1].text) + 1,2))
                                A.addCellToRow(round(float(r.find_all("td")[9].find_all("span")[1].text) + 1,2))
                                A.addCellToRow(r.find("td").text.split()[0])
                                found = True
                                break
                            except:
                                continue
                        if (not found):
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
                            A.addCellToRow(np.nan)
        A.addCellToRow(game)
        A.appendRow()
        counter += 1
        if (counter % 100 == 1):
            A.dictToCsv("./csv_data/" + league + "/betting.csv")
    A.dictToCsv("./csv_data/" + league + "/betting.csv")
    browser.close()

def nowgoalCurSeason(league):
    dict = {"Date":[],"Home":[],"Away":[],"home_team_reg_score":[],"away_team_reg_score":[],"includedInPrior":[]}
    driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1325x744")
    browser = webdriver.Chrome(executable_path=driver_path, options = chrome_options)
    browser.maximize_window()
    if (league == "Japan1"):
        url = "https://football.nowgoal5.com/SubLeague/25"
    elif (league == "Japan2"):
        url = "https://football.nowgoal5.com/SubLeague/284"
    elif (league == "Korea1"):
        url = "https://football.nowgoal5.com/SubLeague/15"
    elif (league == "Norway1"):
        url = "https://football.nowgoal5.com/League/22"
    elif (league == "Norway2"):
        url = "https://football.nowgoal5.com/SubLeague/123"
    elif (league == "Sweden2"):
        url = "https://football.nowgoal5.com/SubLeague/122"
    elif (league == "Brazil1"):
        url = "https://football.nowgoal5.com/League/4"
    elif (league == "Brazil2"):
        url = "https://football.nowgoal5.com/League/358"

    inPrior = []
    if (exists("./csv_data/" + league + "/current/results.csv")):
        results = pd.read_csv("./csv_data/" + league + "/current/results.csv", encoding = "ISO-8859-1")
        for i in range(len(results.index)):
            results.at[i, "Date"] = datetime.date(int(results.at[i, "Date"].split("-")[0]), int(results.at[i, "Date"].split("-")[1]), int(results.at[i, "Date"].split("-")[2]))
        for index, row in results.iterrows():
            inPrior.append({"Date":row["Date"],"Home":row["Home"],"Away":row["Away"]})

    browser.get(url)
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    i = 1
    j = 2
    lastDate = "..."
    while (1):
        try:
            browser.find_element_by_xpath("//*[@id='Table2']/tbody/tr[" + str(i) + "]/td[" + str(j) + "]").click()
            time.sleep(2)
        except:
            if (i == 1):
                i = 2
                j = 1
                continue
            else:
                break
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        try:
            print(soup.find(class_="tdsolid").find_all("td")[2]["data-t"])
        except:
            j += 1
            continue
        while (soup.find(class_="tdsolid").find_all("td")[2]["data-t"] == lastDate):
            print(soup.find(class_="tdsolid").find_all("td")[2]["data-t"])
            time.sleep(5)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
        lastDate = soup.find(class_="tdsolid").find_all("td")[2]["data-t"]
        for x in soup.find(class_="tdsolid").find_all("td"):
            if (x.has_attr("data-t")):
                if ("Postp." not in  x.find_next_sibling().find_next_sibling().find("a").get_text() and "Abd" not in  x.find_next_sibling().find_next_sibling().find("a").get_text()):
                    curDate = datetime.date(int(x["data-t"].split()[0].split("-")[0]), int(x["data-t"].split()[0].split("-")[1]), int(x["data-t"].split()[0].split("-")[2]))
                    if (curDate > datetime.date.today()):
                        continue
                    dict["Date"].append(curDate)
                    dict["Home"].append(x.find_next_sibling().find("a").string)
                    dict["Away"].append(x.find_next_sibling().find_next_sibling().find_next_sibling().find("a").string)
                    print (x.find_next_sibling().find_next_sibling().find("a").get_text())
                    dict["home_team_reg_score"].append(x.find_next_sibling().find_next_sibling().find("a").get_text().split("-")[0])
                    dict["away_team_reg_score"].append(x.find_next_sibling().find_next_sibling().find("a").get_text().split("-")[1])
                    inpriorBool = False
                    for game in inPrior:
                        if (abs(curDate - game["Date"]).days <= 2 and x.find_next_sibling().find("a").string == game["Home"] and x.find_next_sibling().find_next_sibling().find_next_sibling().find("a").string == game["Away"]):
                            dict["includedInPrior"].append(1)
                            inpriorBool = True
                    if (not inpriorBool):
                        print (x.find_next_sibling().find("a").string, curDate)
                        dict["includedInPrior"].append(0)
        j += 1
    for key in dict:
        print (key, len(dict[key]), dict[key])
    if (len(dict["includedInPrior"]) == 0):
        nowgoalCurSeason(league)
    df = pd.DataFrame.from_dict(dict)
    df = df.sort_values(by=["Date"], ignore_index = True)
    if (not exists("./csv_data/" + league + "/current/")):
        os.makedirs("./csv_data/" + league + "/current/")
    df.to_csv("./csv_data/" + league + "/current/results.csv", index = False)

def pinnacle(league):
    if (league == "Japan1"):
        url = "https://www.pinnacle.com/en/soccer/japan-j-league/matchups#period:0"
    elif (league == "Japan2"):
        url = "https://www.pinnacle.com/en/soccer/japan-j2-league/matchups#period:0"
    elif (league == "Korea1"):
        url = "https://www.pinnacle.com/en/soccer/korea-republic-k-league-1/matchups#period:0"
    elif (league == "Norway1"):
        url = "https://www.pinnacle.com/en/soccer/norway-eliteserien/matchups#period:0"
    elif (league == "Norway2"):
        url = "https://www.pinnacle.com/en/soccer/norway-1st-division/matchups#period:0"
    elif (league == "Sweden2"):
        url = "https://www.pinnacle.com/en/soccer/sweden-superettan/matchups#period:0"
    elif (league == "Brazil1"):
        url = "https://www.pinnacle.com/en/soccer/brazil-serie-a/matchups#period:0"
    elif (league == "Brazil2"):
        url = "https://www.pinnacle.com/en/soccer/brazil-serie-b/matchups#period:0"

    A = Database(["Date","Home","Away","AH","Home AH Odds","Away AH Odds","OU","Over Odds","Under Odds"])
    driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1325x744")
    browser = webdriver.Chrome(executable_path=driver_path, options = chrome_options)
    browser.get(url)

    time.sleep(20)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find(class_="contentBlock square")
    for game in main.contents:
        try:
            fail = game.find_all("span")[13].text
        except:
            continue
        A.addCellToRow(datetime.date.today())
        if ("ERROR" in standardizeTeamName(game.find_all("span")[0].text, league)):
            print (standardizeTeamName(game.find_all("span")[0].text, league))
        if ("ERROR" in standardizeTeamName(game.find_all("span")[1].text, league)):
            print (standardizeTeamName(game.find_all("span")[1].text, league))

        A.addCellToRow(standardizeTeamName(game.find_all("span")[0].text, league))
        A.addCellToRow(standardizeTeamName(game.find_all("span")[1].text, league))
        if ("+" in game.find_all("span")[6].text):
            A.addCellToRow(float(game.find_all("span")[6].text.split("+")[1]) * -1)
        elif ("-" in game.find_all("span")[6].text):
            A.addCellToRow(float(game.find_all("span")[6].text.split("-")[1]))
        else:
            A.addCellToRow(float(game.find_all("span")[6].text))
        A.addCellToRow(float(game.find_all("span")[7].text))
        A.addCellToRow(float(game.find_all("span")[9].text))
        A.addCellToRow(float(game.find_all("span")[10].text))
        A.addCellToRow(float(game.find_all("span")[11].text))
        A.addCellToRow(float(game.find_all("span")[13].text))
        A.appendRow()
    browser.close()
    return (A.getDataFrame())

def transfermarkt(league):
    if (league == "Japan1"):
        urlRoot = "https://www.transfermarkt.com/j1-league/startseite/wettbewerb/JAP1/plus/?saison_id="
    elif (league == "Japan2"):
        urlRoot = "https://www.transfermarkt.com/j2-league/startseite/wettbewerb/JAP2/plus/?saison_id="
    elif (league == "Norway1"):
        urlRoot = "https://www.transfermarkt.com/eliteserien/startseite/wettbewerb/NO1/plus/?saison_id="
    elif (league == "Norway2"):
        urlRoot = "https://www.transfermarkt.com/obos-ligaen/startseite/wettbewerb/NO2/plus/?saison_id"
    elif (league == "Brazil1"):
        urlRoot = "https://www.transfermarkt.com/campeonato-brasileiro-serie-a/startseite/wettbewerb/BRA1/plus/?saison_id="
    elif (league == "Brazil2"):
        urlRoot = "https://www.transfermarkt.com/campeonato-brasileiro-serie-b/startseite/wettbewerb/BRA2/plus/?saison_id="
    elif (league == "Sweden2"):
        urlRoot = "https://www.transfermarkt.com/superettan/startseite/wettbewerb/SE2/plus/?saison_id="
    elif (league == "Korea1"):
        urlRoot = "https://www.transfermarkt.com/k-league-1/startseite/wettbewerb/RSK1/plus/?saison_id="



    A = Database(["Season","Team","Value"])
    driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1325x744")
    browser = webdriver.Chrome(executable_path=driver_path, options = chrome_options)
    for curSeason in [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]:
        browser.get(urlRoot + str(curSeason - 1))

        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        table = soup.find(class_="responsive-table").find("tbody")

        for row in table.find_all("tr"):
            A.addCellToRow(curSeason)
            A.addCellToRow(row.find_all("td")[1].get_text())
            A.addCellToRow(row.find_all("td")[6].get_text())
            A.appendRow()
    A.dictToCsv("./csv_data/" + league + "/transfermarkt.csv")
