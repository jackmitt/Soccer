from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import date
import pandas as pd
import numpy as np
from miscFcns import oddsToDecimal

years = [2014, 2015, 2016, 2017, 2018]
gameUrls = []
for year in years:
    browser = webdriver.Chrome(executable_path='chromedriver.exe')
    browser.get("https://understat.com/league/EPL/" + str(year))
    while (1):
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        temp = soup.find(class_="calendar-prev")
        games = soup.find_all(class_="calendar-game")
        for game in games:
            gameUrls.append("https://understat.com/" + game.find(class_="match-info")["href"])
        if (temp.has_attr("disabled")):
            break
        browser.find_element_by_css_selector(".calendar-prev").click()
    browser.quit()

count = 1
dict = {"Date":[],"Home":[],"Away":[],"Home xG":[],"Away xG":[],"Home shots":[],"Away shots":[],"Home on target":[],"Away on target":[],"Home deep":[],"Away deep":[],"Home ppda":[],"Away ppda":[],"Home xPts":[],"Away xPts":[]}
for game in gameUrls:
    print (str(count) + " out of " + str(len(gameUrls)) + " games")
    count += 1
    browser = webdriver.Chrome(executable_path='chromedriver.exe')
    browser.get(game)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    dict["Date"].append(soup.find_all("li")[5].string)
    dict["Home"].append(soup.find(class_="progress-home progress-over").find(class_="progress-value").string)
    dict["Away"].append(soup.find(class_="progress-away").find(class_="progress-value").string)
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
for key in dict:
    print (key, len(dict[key]))
dfFinal = pd.DataFrame.from_dict(dict)
dfFinal.to_csv("./understatGameStats.csv")
