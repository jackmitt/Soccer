import pandas as pd
import numpy as np
import scipy.stats
import os
from os.path import exists

class Database:
    def __init__(self, keys = []):
        self.df = pd.DataFrame()
        self.dict = {}
        for key in keys:
            self.dict[key] = []
        self.tempRow = []

    def getKeys(self):
        return (list(self.dict.keys()))

    def getCol(self, colName):
        return (self.dict[colName])

    def getLength(self):
        return (len(list(self.dict.keys())[0]))

    def getDict(self):
        return (self.dict)

    def getDataFrame(self):
        self.df = pd.DataFrame.from_dict(self.dict)
        return(self.df)

    def getCell(self, col, index):
        return (self.dict[col][index])

    def initDictFromCsv(self, path):
        self.dict = pd.read_csv(path, encoding = "ISO-8859-1").to_dict(orient="list")

    def addColumn(self, colName):
        self.dict[colName] = []

    def addCellToRow(self, datum):
        if (len(self.tempRow) + 1 > len(self.dict)):
            raise ValueError("The row is already full")
        else:
            self.tempRow.append(datum)

    def appendRow(self):
        if (len(self.tempRow) != len(self.dict)):
            raise ValueError("The row is not fully populated")
        else:
            for i in range(len(self.dict.keys())):
                self.dict[list(self.dict.keys())[i]].append(self.tempRow[i])
            self.tempRow = []

    def trashRow(self):
        self.tempRow = []

    def dictToCsv(self, pathName):
        self.df = pd.DataFrame.from_dict(self.dict)
        self.df = self.df.drop_duplicates()
        self.df.to_csv(pathName, index = False)

    def printRow(self):
        print(self.tempRow)

    def printDict(self):
        print(self.dict)

    def reset(self):
        self.tempRow = []
        self.dict = {}
        for key in list(self.dict.keys()):
            self.dict[key] = []

    def merge(self, B):
        for key in B.getKeys():
            if (key not in list(self.dict.keys())):
                self.dict[key] = B.getCol(key)

def standardizeTeamName(name, league):
    lname = name.lower()
    if (league == "Japan1"):
        if ("kyoto sanga" in lname):
            return ("Kyoto Sanga")
        elif ("yokohama" in lname and "marinos" in lname):
            return ("Yokohama Marinos")
        elif ("hiroshima" in lname and "sanfrecce" in lname):
            return ("Hiroshima Sanfrecce")
        elif ("nagoya grampus" in lname):
            return ("Nagoya Grampus")
        elif (" iwata" in lname):
            return ("Jubilo Iwata")
        elif ("consadole sapporo" in lname):
            return ("Consadole Sapporo")
        elif ("matsumoto yamaga" in lname):
            return ("Matsumoto Yamaga FC")
        else:
            return (name)
    elif (league == "Japan2"):
        if ("thespakusatsu" in lname):
            return ("Thespa Kusatsu")
        elif ("zweigen kanazawa" in lname):
            return ("Zweigen Kanazawa FC")
        elif ("niigata albirex" in lname):
            return ("Albirex Niigata")
        else:
            return (name)
    elif (league == "Korea1"):
        if ("jeonbuk motors" in lname):
            return ("Jeonbuk Hyundai Motors")
        elif ("suwon city" in lname):
            return ("Suwon FC")
        elif ("suwon samsung bluewings" in lname):
            return ("Suwon Samsung Bluewings")
        else:
            return (name)
    elif (league == "Norway1"):
        if ("lillestrom sk" in lname):
            return ("Lillestrom")
        elif ("sarpsborg 08" in lname):
            return ("Sarpsborg 08")
        elif ("tromso" == lname):
            return ("Tromso IL")
        elif ("fk jerv" in lname):
            return ("Jerv")
        elif ("rosenborg" in lname):
            return ("Rosenborg")
        elif ("odd bk" == lname):
            return ("Odd Grenland")
        elif ("stromsgodset" in lname):
            return ("Stromsgodset")
        elif ("molde fk" in lname):
            return ("Molde")
        elif ("viking fk" in lname):
            return ("Viking")
        elif ("aalesunds" in lname):
            return ("Aalesund FK")
        else:
            return (name)
    elif (league == "Norway2"):
        if ("fredrikstad" in lname):
            return ("Fredrikstad")
        elif ("ik start" in lname):
            return ("Start Kristiansand")
        elif ("aasane fotball" in lname):
            return ("Asane Fotball")
        elif ("stabaek if" in lname):
            return ("Stabaek")
        elif ("skeid fotball" in lname):
            return ("Skeid Oslo")
        elif ("sk brann" in lname):
            return ("Brann")
        elif ("stjordals/blink" in lname):
            return ("Stjordals Blink")
        elif ("sogndal il" in lname):
            return ("Sogndal")
        elif ("bryne fk" in lname):
            return ("Bryne")
        elif ("raufoss il" in lname):
            return ("Raufoss")
        elif ("ranheim" == lname):
            return ("Ranheim IL")
        elif ("grorud il" in lname):
            return ("Grorud")
        elif ("kongsvinger il fotball" in lname):
            return ("Kongsvinger")
        else:
            return (name)
    elif (league == "Sweden2"):
        if ("landskrona" in lname):
            return ("Landskrona BoIS")
        elif ("jonkopings sodra" in lname):
            return ("Jonkopings Sodra IF")
        elif ("osters if" in lname):
            return ("Osters IF")
        elif ("vasteras sk" in lname):
            return ("Vasteras SK FK")
        elif ("utsiktens" in lname):
            return ("Utsiktens BK")
        elif ("trelleborgs" in lname):
            return ("Trelleborgs FF")
        else:
            return (name)
    elif (league == "Brazil1"):
        if ("flamengo" in lname):
            return ("Flamengo")
        elif ("palmeiras" in lname):
            return ("Palmeiras")
        elif ("paranaense" in lname):
            return ("Atletico Paranaense")
        elif ("bragantino" in lname):
            return ("Bragantino")
        elif ("sao paulo" in lname):
            return ("Sao Paulo")
        elif ("corinthians" in lname):
            return ("Corinthians Paulista (SP)")
        elif ("fluminense" in lname):
            return ("Fluminense RJ")
        elif ("internacional rs" in lname):
            return ("Internacional RS")
        elif ("santos fc sp" in lname):
            return ("Santos")
        elif ("america fc mg" in lname):
            return ("America MG")
        elif ("juventude" in lname):
            return ("Juventude")
        elif ("cuiaba esporte" in lname):
            return ("Cuiaba")
        elif ("ceara sc" in lname):
            return ("Ceara")
        elif ("goianiense" in lname):
            return ("Atletico Clube Goianiense")
        elif ("goias ec go" in lname):
            return ("Goias")
        elif ("atletico mineiro" in lname):
            return ("Atletico Mineiro")
        elif ("botafogo" in lname):
            return ("Botafogo RJ")
        elif ("fortaleza" in lname):
            return ("Fortaleza")
        elif ("coritiba" in lname):
            return ("Coritiba PR")
        else:
            return (name)
    elif (league == "Brazil2"):
        if ("sc recife pe" in lname):
            return ("Sport Club Recife PE")
        elif ("ituano fc sp" in lname):
            return ("Ituano  SP")
        elif ("gremio novorizontino" in lname):
            return ("Gremio Novorizontin")
        elif ("brusque sc" in lname):
            return ("Brusque FC")
        elif ("cs alagoano al" in lname):
            return ("Centro Sportivo Alagoano")
        elif ("vila nova" in lname):
            return ("Vila Nova")
        elif ("tombense" in lname):
            return ("Tombense")
        elif ("ec bahia" in lname):
            return ("Bahia")
        elif ("sampaio correa" in lname):
            return ("Sampaio Correa")
        elif ("cruzeiro" in lname):
            return ("Cruzeiro (MG)")
        elif ("londrina" in lname):
            return ("Londrina PR")
        elif ("cr brasil al" in lname):
            return ("CRB AL")
        elif ("nautico pe" in lname):
            return ("Nautico (PE)")
        elif ("operario ferroviario" in lname):
            return ("Operario Ferroviario PR")
        elif ("gremio fb porto" in lname):
            return ("Gremio (RS)")
        elif ("guarani fc sp" in lname):
            return ("Guarani SP")
        elif ("criciuma" in lname):
            return ("Criciuma")
        elif ("vasco da gama" in lname):
            return ("Vasco da Gama")
        elif ("ponte preta" in lname):
            return ("Ponte Preta")
        else:
            return (name)

def grade_bets(league):
    netwin = 0
    #for league in next(os.walk("./csv_data/"))[1]:
    ahresult = []
    ouresult = []
    if (exists("./csv_data/" + league + "/current/bets.csv")):
        bets = pd.read_csv("./csv_data/" + league + "/current/bets.csv", encoding = "ISO-8859-1")
        results = pd.read_csv("./csv_data/" + league + "/current/results.csv", encoding = "ISO-8859-1")
        for index, row in bets.iterrows():
            if (row["AH Bet"] != row["AH Bet"] and row["OU Bet"] != row["OU Bet"]):
                ahresult.append(np.nan)
                ouresult.append(np.nan)
                continue
            alreadyGraded = False
            if ("AH Result" in bets.columns and row["AH Result"] == row["AH Result"]):
                ahresult.append(row["AH Result"])
                alreadyGraded = True
                if (row["OU Result"] != row["OU Result"]):
                    ouresult.append(np.nan)
            if ("OU Result" in bets.columns and row["OU Result"] == row["OU Result"]):
                ouresult.append(row["OU Result"])
                alreadyGraded = True
                if (row["AH Result"] != row["AH Result"]):
                    ahresult.append(np.nan)
            if (alreadyGraded):
                continue
            curIndex = 0
            match = False
            for i in range(len(results.index)):
                if (results.at[i, "Home"] == row["Home"] and results.at[i, "Away"] == row["Away"]):
                    curIndex = i
                    match = True
            if (not match):
                ahresult.append(np.nan)
                ouresult.append(np.nan)
                continue
            if (row["AH Bet"] == row["AH Bet"]):
                if (" +" in row["AH Bet"]):
                    if (row["Home"] == row["AH Bet"].split(" +")[0]):
                        if (".75" not in str(row["AH Bet"]) and ".25" not in str(row["AH Bet"])):
                            if (results.at[curIndex, "home_team_reg_score"] + float(row["AH Bet"].split(" +")[1]) > results.at[curIndex, "away_team_reg_score"]):
                                netwin += row["AH Bet Amount"] * (row["AH Bet Odds"] - 1)
                                ahresult.append("WW")
                            elif (results.at[curIndex, "home_team_reg_score"] + float(row["AH Bet"].split(" +")[1]) < results.at[curIndex, "away_team_reg_score"]):
                                netwin -= row["AH Bet Amount"]
                                ahresult.append("LL")
                            else:
                                ahresult.append("PP")
                        else:
                            parts = [float(row["AH Bet"].split(" +")[1]) - 0.25,float(row["AH Bet"].split(" +")[1]) + 0.25]
                            cur_result = ""
                            for part in parts:
                                if (results.at[curIndex, "home_team_reg_score"] + part > results.at[curIndex, "away_team_reg_score"]):
                                    netwin += row["AH Bet Amount"] * (row["AH Bet Odds"] - 1) / 2
                                    cur_result += "W"
                                elif (results.at[curIndex, "home_team_reg_score"] + part < results.at[curIndex, "away_team_reg_score"]):
                                    netwin -= row["AH Bet Amount"] / 2
                                    cur_result += "L"
                                else:
                                    cur_result += "P"
                            ahresult.append(cur_result)
                    else:
                        if (".75" not in str(row["AH Bet"]) and ".25" not in str(row["AH Bet"])):
                            if (results.at[curIndex, "away_team_reg_score"] + float(row["AH Bet"].split(" +")[1]) > results.at[curIndex, "home_team_reg_score"]):
                                netwin += row["AH Bet Amount"] * (row["AH Bet Odds"] - 1)
                                ahresult.append("WW")
                            elif (results.at[curIndex, "away_team_reg_score"] + float(row["AH Bet"].split(" +")[1]) < results.at[curIndex, "home_team_reg_score"]):
                                netwin -= row["AH Bet Amount"]
                                ahresult.append("LL")
                            else:
                                ahresult.append("PP")
                        else:
                            parts = [float(row["AH Bet"].split(" +")[1]) - 0.25,float(row["AH Bet"].split(" +")[1]) + 0.25]
                            cur_result = ""
                            for part in parts:
                                if (results.at[curIndex, "away_team_reg_score"] + part > results.at[curIndex, "home_team_reg_score"]):
                                    netwin += row["AH Bet Amount"] * (row["AH Bet Odds"] - 1) / 2
                                    cur_result += "W"
                                elif (results.at[curIndex, "away_team_reg_score"] + part < results.at[curIndex, "home_team_reg_score"]):
                                    netwin -= row["AH Bet Amount"] / 2
                                    cur_result += "L"
                                else:
                                    cur_result += "P"
                            ahresult.append(cur_result)
                elif (" -" in row["AH Bet"]):
                    if (row["Home"] == row["AH Bet"].split(" -")[0]):
                        if (".75" not in str(row["AH Bet"]) and ".25" not in str(row["AH Bet"])):
                            if (results.at[curIndex, "home_team_reg_score"] - float(row["AH Bet"].split(" -")[1]) > results.at[curIndex, "away_team_reg_score"]):
                                netwin += row["AH Bet Amount"] * (row["AH Bet Odds"] - 1)
                                ahresult.append("WW")
                            elif (results.at[curIndex, "home_team_reg_score"] - float(row["AH Bet"].split(" -")[1]) < results.at[curIndex, "away_team_reg_score"]):
                                netwin -= row["AH Bet Amount"]
                                ahresult.append("LL")
                            else:
                                ahresult.append("PP")
                        else:
                            parts = [float(row["AH Bet"].split(" -")[1]) - 0.25,float(row["AH Bet"].split(" -")[1]) + 0.25]
                            cur_result = ""
                            for part in parts:
                                if (results.at[curIndex, "home_team_reg_score"] - part > results.at[curIndex, "away_team_reg_score"]):
                                    netwin += row["AH Bet Amount"] * (row["AH Bet Odds"] - 1) / 2
                                    cur_result += "W"
                                elif (results.at[curIndex, "home_team_reg_score"] - part < results.at[curIndex, "away_team_reg_score"]):
                                    netwin -= row["AH Bet Amount"] / 2
                                    cur_result += "L"
                                else:
                                    cur_result += "P"
                            ahresult.append(cur_result)
                    else:
                        if (".75" not in str(row["AH Bet"]) and ".25" not in str(row["AH Bet"])):
                            if (results.at[curIndex, "away_team_reg_score"] - float(row["AH Bet"].split(" -")[1]) > results.at[curIndex, "home_team_reg_score"]):
                                netwin += row["AH Bet Amount"] * (row["AH Bet Odds"] - 1)
                                ahresult.append("WW")
                            elif (results.at[curIndex, "away_team_reg_score"] - float(row["AH Bet"].split(" -")[1]) < results.at[curIndex, "home_team_reg_score"]):
                                netwin -= row["AH Bet Amount"]
                                ahresult.append("LL")
                            else:
                                ahresult.append("PP")
                        else:
                            parts = [float(row["AH Bet"].split(" -")[1]) - 0.25,float(row["AH Bet"].split(" -")[1]) + 0.25]
                            cur_result = ""
                            for part in parts:
                                if (results.at[curIndex, "away_team_reg_score"] - part > results.at[curIndex, "home_team_reg_score"]):
                                    netwin += row["AH Bet Amount"] * (row["AH Bet Odds"] - 1) / 2
                                    cur_result += "W"
                                elif (results.at[curIndex, "away_team_reg_score"] - part < results.at[curIndex, "home_team_reg_score"]):
                                    netwin -= row["AH Bet Amount"] / 2
                                    cur_result += "L"
                                else:
                                    cur_result += "P"
                            ahresult.append(cur_result)
                else:
                    if (row["Home"] == row["AH Bet"].split(" 0")[0]):
                        if (results.at[curIndex, "home_team_reg_score"] > results.at[curIndex, "away_team_reg_score"]):
                            netwin += row["AH Bet Amount"] * (row["AH Bet Odds"] - 1)
                            ahresult.append("WW")
                        elif (results.at[curIndex, "home_team_reg_score"] < results.at[curIndex, "away_team_reg_score"]):
                            netwin -= row["AH Bet Amount"]
                            ahresult.append("LL")
                        else:
                            ahresult.append("PP")
                    else:
                        if (results.at[curIndex, "away_team_reg_score"] > results.at[curIndex, "home_team_reg_score"]):
                            netwin += row["AH Bet Amount"] * (row["AH Bet Odds"] - 1)
                            ahresult.append("WW")
                        elif (results.at[curIndex, "away_team_reg_score"] < results.at[curIndex, "home_team_reg_score"]):
                            netwin -= row["AH Bet Amount"]
                            ahresult.append("LL")
                        else:
                            ahresult.append("PP")
            else:
                ahresult.append(np.nan)
            if (row["OU Bet"] == row["OU Bet"]):
                if (row["OU Bet"] == "Over"):
                    if (".75" not in str(row["pinny_OU"]) and ".25" not in str(row["pinny_OU"])):
                        if (results.at[curIndex, "home_team_reg_score"] + results.at[curIndex, "away_team_reg_score"] > row["pinny_OU"]):
                            netwin += row["OU Bet Amount"] * (row["OU Bet Odds"] - 1)
                            ouresult.append("WW")
                        elif (results.at[curIndex, "home_team_reg_score"] + results.at[curIndex, "away_team_reg_score"] < row["pinny_OU"]):
                            netwin -= row["OU Bet Amount"]
                            ouresult.append("LL")
                        else:
                            ouresult.append("PP")
                    else:
                        parts = [row["pinny_OU"] - 0.25,row["pinny_OU"] + 0.25]
                        cur_result = ""
                        for part in parts:
                            if (results.at[curIndex, "home_team_reg_score"] + results.at[curIndex, "away_team_reg_score"] > part):
                                netwin += row["OU Bet Amount"] * (row["OU Bet Odds"] - 1) / 2
                                cur_result += "W"
                            elif (results.at[curIndex, "home_team_reg_score"] + results.at[curIndex, "away_team_reg_score"] < part):
                                netwin -= row["OU Bet Amount"] / 2
                                cur_result += "L"
                            else:
                                cur_result += "P"
                        ouresult.append(cur_result)
                else:
                    if (".75" not in str(row["pinny_OU"]) and ".25" not in str(row["pinny_OU"])):
                        if (results.at[curIndex, "home_team_reg_score"] + results.at[curIndex, "away_team_reg_score"] < row["pinny_OU"]):
                            netwin += row["OU Bet Amount"] * (row["OU Bet Odds"] - 1)
                            ouresult.append("WW")
                        elif (results.at[curIndex, "home_team_reg_score"] + results.at[curIndex, "away_team_reg_score"] > row["pinny_OU"]):
                            netwin -= row["OU Bet Amount"]
                            ouresult.append("LL")
                        else:
                            ouresult.append("PP")
                    else:
                        parts = [row["pinny_OU"] - 0.25,row["pinny_OU"] + 0.25]
                        cur_result = ""
                        for part in parts:
                            if (results.at[curIndex, "home_team_reg_score"] + results.at[curIndex, "away_team_reg_score"] < part):
                                netwin += row["OU Bet Amount"] * (row["OU Bet Odds"] - 1) / 2
                                cur_result += "W"
                            elif (results.at[curIndex, "home_team_reg_score"] + results.at[curIndex, "away_team_reg_score"] > part):
                                netwin -= row["OU Bet Amount"] / 2
                                cur_result += "L"
                            else:
                                cur_result += "P"
                        ouresult.append(cur_result)
            else:
                ouresult.append(np.nan)

        bets["AH Result"] = ahresult
        bets["OU Result"] = ouresult
        bets.to_csv("./csv_data/" + league + "/current/bets.csv", index = False)
    return (netwin)
