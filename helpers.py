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
        elif ("shimizu" in lname):
            return ("Shimizu S-Pulse")
        elif ("tokyo" == lname):
            return ("FC Tokyo")
        else:
            return (name)
    elif (league == "Japan2"):
        if ("thespakusatsu" in lname):
            return ("Thespa Kusatsu")
        elif ("zweigen kanazawa" in lname):
            return ("Zweigen Kanazawa FC")
        elif ("niigata albirex" in lname):
            return ("Albirex Niigata")
        elif ("consadole sapporo" in lname):
            return ("Consadole Sapporo")
        elif ("matsumoto yamaga" in lname):
            return ("Matsumoto Yamaga FC")
        elif (" iwata" in lname):
            return ("Jubilo Iwata")
        elif ("jef united" in lname):
            return ("JEF United Ichihara Chiba")
        elif ("mito holly" in lname):
            return ("Mito Hollyhock")
        elif ("varen nagasaki" in lname):
            return ("V-Varen Nagasaki")
        elif ("yokohama" in lname):
            return ("Yokohama FC")
        elif ("jef united" in lname):
            return ("JEF United Ichihara Chiba")
        elif ("ryukyu" in lname):
            return ("FC Ryukyu")
        else:
            return (name)
    elif (league == "Korea1"):
        if ("jeonbuk motors" in lname):
            return ("Jeonbuk Hyundai Motors")
        elif ("suwon city" in lname):
            return ("Suwon FC")
        elif ("suwon samsung bluewings" in lname):
            return ("Suwon Samsung Bluewings")
        elif ("sangju sangmu" in lname or "gimcheon sangmu" in lname):
            return ("Gimcheon Sangmu FC")
        elif ("ulsan hyundai" in lname):
            return ("Ulsan Hyundai FC")
        elif ("seongnam" in lname):
            return ("Seongnam FC")
        elif ("busan ipark" in lname):
            return ("Busan I Park")
        elif ("chunnam dragon" in lname):
            return ("Jeonnam Dragons")
        elif ("gwangju " in lname):
            return ("Gwangju Football Club")
        else:
            return (name)
    elif (league == "Norway1"):
        if ("lillestrom sk" in lname or "lillestrøm" in lname):
            return ("Lillestrom")
        elif ("sarpsborg 08" in lname):
            return ("Sarpsborg 08")
        elif ("tromso" == lname or "tromsø" in lname):
            return ("Tromso IL")
        elif ("fk jerv" in lname):
            return ("Jerv")
        elif ("rosenborg" in lname):
            return ("Rosenborg")
        elif ("odd bk" == lname or "odds bk" in lname):
            return ("Odd Grenland")
        elif ("stromsgodset" in lname or "strømsgodset" in lname):
            return ("Stromsgodset")
        elif ("molde fk" in lname):
            return ("Molde")
        elif ("viking fk" in lname or "viking stava" in lname):
            return ("Viking")
        elif ("aalesund" in lname):
            return ("Aalesund FK")
        elif ("lerenga " in lname):
            return ("Valerenga")
        elif ("sk brann" in lname):
            return ("Brann")
        elif ("haugesund" in lname):
            return ("Haugesund")
        elif ("fredrikstad" in lname):
            return ("Fredrikstad")
        elif ("stabaek if" in lname or "stabæk" in lname):
            return ("Stabaek")
        elif ("hönefoss" in lname):
            return ("Honefoss BK")
        elif ("sogndal il" in lname):
            return ("Sogndal")
        elif ("ik start" in lname):
            return ("Start Kristiansand")
        elif ("/glimt" in lname):
            return ("Bodo Glimt")
        elif ("sandefjord" in lname):
            return ("Sandefjord")
        elif ("mjøndalen" in lname):
            return ("Mjondalen IF")
        elif ("haugesund" in lname):
            return ("Haugesund")
        elif ("ham kam" in lname):
            return ("Ham-Kam")
        else:
            return (name)
    elif (league == "Norway2"):
        if ("fredrikstad" in lname):
            return ("Fredrikstad")
        elif ("ik start" in lname):
            return ("Start Kristiansand")
        elif ("aasane " in lname):
            return ("Asane Fotball")
        elif ("stabaek if" in lname or "stabæk" in lname):
            return ("Stabaek")
        elif ("skeid " in lname):
            return ("Skeid Oslo")
        elif ("sk brann" in lname):
            return ("Brann")
        elif ("stj" in lname and "rdals" in lname and "blink" in lname):
            return ("Stjordals Blink")
        elif ("sogndal" in lname):
            return ("Sogndal")
        elif ("bryne" in lname):
            return ("Bryne")
        elif ("raufoss" in lname):
            return ("Raufoss")
        elif ("ranheim" == lname):
            return ("Ranheim IL")
        elif ("grorud " in lname):
            return ("Grorud")
        elif ("kongsvinger" in lname):
            return ("Kongsvinger")
        elif ("mjøndalen" in lname):
            return ("Mjondalen IF")
        elif ("kfum" in lname and "oslo" in lname):
            return ("KFUM Oslo")
        elif ("kongsvinger " in lname):
            return ("Kongsvinger")
        elif ("kfum " in lname):
            return ("KFUM Oslo")
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
        elif ("orebro " in lname):
            return ("Orebro")
        elif ("halmstads " in lname):
            return ("Halmstads")
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
        elif ("sao paulo" in lname or "são paulo" in lname):
            return ("Sao Paulo")
        elif ("corinthians" in lname):
            return ("Corinthians Paulista (SP)")
        elif ("fluminense" in lname):
            return ("Fluminense RJ")
        elif ("internacional rs" in lname or "sport club internacional" in lname):
            return ("Internacional RS")
        elif ("santos fc" in lname):
            return ("Santos")
        elif ("america fc mg" in lname or ("américa" in lname and "(mg)" in lname)):
            return ("America MG")
        elif ("juventude" in lname):
            return ("Juventude")
        elif ("cuiaba esporte" in lname or "cuiabá" in lname):
            return ("Cuiaba")
        elif ("ceara sc" in lname):
            return ("Ceara")
        elif ("goianiense" in lname):
            return ("Atletico Clube Goianiense")
        elif ("goias ec go" in lname or "goiás" in lname):
            return ("Goias")
        elif ("atletico mineiro" in lname or "atlético mineiro" in lname):
            return ("Atletico Mineiro")
        elif ("botafogo" in lname):
            return ("Botafogo RJ")
        elif ("fortaleza" in lname):
            return ("Fortaleza")
        elif ("coritiba" in lname):
            return ("Coritiba PR")
        elif (("gremio" in lname or "grêmio" in lname) and "porto" in lname):
            return ("Gremio (RS)")
        elif ("cruzeiro" in lname):
            return ("Cruzeiro (MG)")
        elif ("vasco da gama" in lname):
            return ("Vasco da Gama")
        elif ("figueirense" in lname):
            return ("Figueirense")
        elif ("portuguesa" in lname):
            return ("Portuguesa Desportos")
        elif (" bahia" in lname):
            return ("Bahia")
        elif ("sc recife pe" in lname or "do recife" in lname):
            return ("Sport Club Recife PE")
        elif ("nautico pe" in lname or "náutico" in lname):
            return ("Nautico (PE)")
        elif ("ponte preta" in lname):
            return ("Ponte Preta")
        elif ("criciuma" in lname or "criciúma" in lname):
            return ("Criciuma")
        elif ("vitória" in lname):
            return ("Vitoria BA")
        elif ("chapecoense" in lname):
            return ("Chapecoense SC")
        elif ("avaí futebol clube (sc)" in lname):
            return ("Avai FC SC")
        elif ("joinville" in lname):
            return ("Joinville SC")
        elif ("santa cruz" in lname):
            return ("Santa Cruz PE")
        elif ("ceará" in lname):
            return ("Ceara")
        elif ("paraná" in lname):
            return ("Parana PR")
        elif ("centro sportivo alagoano" in lname):
            return ("Centro Sportivo Alagoano")
        else:
            return (name)
    elif (league == "Brazil2"):
        if ("recife pe" in lname):
            return ("Sport Club Recife PE")
        elif ("ituano " in lname):
            return ("Ituano  SP")
        elif ("gremio novorizontino" in lname):
            return ("Gremio Novorizontin")
        elif ("brusque " in lname):
            return ("Brusque FC")
        elif (" alagoano " in lname):
            return ("Centro Sportivo Alagoano")
        elif ("vila nova" in lname):
            return ("Vila Nova")
        elif ("tombense" in lname):
            return ("Tombense")
        elif (" bahia" in lname):
            return ("Bahia")
        elif ("sampaio corr" in lname):
            return ("Sampaio Correa")
        elif ("cruzeiro" in lname):
            return ("Cruzeiro (MG)")
        elif ("londrina" in lname):
            return ("Londrina PR")
        elif ("cr brasil al" in lname or "regatas brasil" in lname):
            return ("CRB AL")
        elif ("nautico " in lname):
            return ("Nautico (PE)")
        elif ("operario " in lname):
            return ("Operario Ferroviario PR")
        elif (("gremio" in lname or "grêmio" in lname) and "porto" in lname):
            return ("Gremio (RS)")
        elif ("guarani " in lname):
            return ("Guarani SP")
        elif ("criciuma" in lname or "criciúma" in lname):
            return ("Criciuma")
        elif ("vasco da gama" in lname):
            return ("Vasco da Gama")
        elif ("ponte preta" in lname):
            return ("Ponte Preta")
        elif ("chapecoense" in lname):
            return ("Chapecoense SC")
        elif ("flamengo" in lname):
            return ("Flamengo")
        elif ("palmeiras" in lname):
            return ("Palmeiras")
        elif ("paranaense" in lname):
            return ("Atletico Paranaense")
        elif ("bragantino" in lname):
            return ("Bragantino")
        elif ("sao paulo" in lname or "são paulo" in lname):
            return ("Sao Paulo")
        elif ("corinthians" in lname):
            return ("Corinthians Paulista (SP)")
        elif ("fluminense" in lname):
            return ("Fluminense RJ")
        elif ("internacional rs" in lname or "sport club internacional" in lname):
            return ("Internacional RS")
        elif ("santos fc" in lname):
            return ("Santos")
        elif ("america fc mg" in lname or ("américa" in lname and "(mg)" in lname)):
            return ("America MG")
        elif ("juventude" in lname):
            return ("Juventude")
        elif ("cuiaba esporte" in lname or "cuiabá" in lname):
            return ("Cuiaba")
        elif ("ceara sc" in lname):
            return ("Ceara")
        elif ("goianiense" in lname):
            return ("Atletico Clube Goianiense")
        elif ("goias ec go" in lname or "goiás" in lname):
            return ("Goias")
        elif ("atletico mineiro" in lname or "atlético mineiro" in lname):
            return ("Atletico Mineiro")
        elif ("botafogo" in lname):
            return ("Botafogo RJ")
        elif ("fortaleza" in lname):
            return ("Fortaleza")
        elif ("coritiba" in lname):
            return ("Coritiba PR")
        elif (("gremio" in lname or "grêmio" in lname) and "porto" in lname):
            return ("Gremio (RS)")
        elif ("cruzeiro" in lname):
            return ("Cruzeiro (MG)")
        elif ("vasco da gama" in lname):
            return ("Vasco da Gama")
        elif ("figueirense" in lname):
            return ("Figueirense")
        elif ("portuguesa" in lname):
            return ("Portuguesa Desportos")
        elif (" bahia" in lname):
            return ("Bahia")
        elif ("sc recife pe" in lname or "do recife" in lname):
            return ("Sport Club Recife PE")
        elif ("nautico pe" in lname or "náutico" in lname):
            return ("Nautico (PE)")
        elif ("ponte preta" in lname):
            return ("Ponte Preta")
        elif ("criciuma" in lname or "criciúma" in lname):
            return ("Criciuma")
        elif ("vitória" in lname):
            return ("Vitoria BA")
        elif ("chapecoense" in lname):
            return ("Chapecoense SC")
        elif ("avaí futebol clube (sc)" in lname):
            return ("Avai FC SC")
        elif ("joinville" in lname):
            return ("Joinville SC")
        elif ("santa cruz" in lname):
            return ("Santa Cruz PE")
        elif ("ceará" in lname):
            return ("Ceara")
        elif ("paraná" in lname):
            return ("Parana PR")
        elif ("centro sportivo alagoano" in lname):
            return ("Centro Sportivo Alagoano")
        elif ("barueri" in lname):
            return ("Gremio Barueri SP")
        elif ("abc " in lname and "(rn)" in lname):
            return ("ABC RN")
        elif ("américa" in lname and "(rn)" in lname):
            return ("America FC Natal RN")
        elif ("boa esporte" in lname):
            return ("Boa Esporte Clube")
        elif ("caetano" in lname):
            return ("Sao Caetano")
        elif ("guaratinguet" in lname):
            return ("Guaratingueta")
        elif ("ipatinga" in lname):
            return ("Ipatinga")
        elif ("rapiraquense" in lname):
            return ("ASA AL")
        elif ("oeste " in lname):
            return ("Oeste")
        elif ("paysandu" in lname):
            return ("SC Paysandu Para")
        elif ("icasa " in lname):
            return ("Icasa CE")
        elif ("luverdense" in lname):
            return ("Luverdense")
        elif ("macaé " in lname):
            return ("Macae")
        elif ("mogi mirim" in lname):
            return ("Mogi Mirim EC")
        elif ("grêmio esportivo brasil (rs)" in lname):
            return ("Brasil de Pelotas")
        elif ("tupi " in lname):
            return ("Tupi Juiz de Fora MG")
        elif ("são bento" in lname):
            return ("Sao Bento")
        elif ("perário ferroviário" in lname):
            return ("Operario Ferroviario PR")
        elif ("confiança " in lname):
            return ("Confianca SE")
        elif ("do remo" in lname):
            return ("Remo Belem (PA)")
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

def convert_league(league):
    if (league == "NORWAY ELITESERIEN"):
        return ("Norway1")
    elif (league == "NORWAY DIVISION 1"):
        return ("Norway2")
    elif (league == "Norway1"):
        return ("NORWAY ELITESERIEN")
    elif (league == "Norway2"):
        return ("NORWAY DIVISION 1")
    elif (league == "Japan1"):
        return ("JAPAN J1 LEAGUE")
    elif (league == "JAPAN J1 LEAGUE"):
        return ("Japan1")
    elif (league == "Japan2"):
        return ("JAPAN J2 LEAGUE")
    elif (league == "JAPAN J2 LEAGUE"):
        return ("Japan2")
    elif (league == "Korea1"):
        return ("KOREA K LEAGUE 1")
    elif (league == "KOREA K LEAGUE 1"):
        return ("Korea1")
    elif (league == "Brazil1"):
        return ("BRAZIL SERIE A")
    elif (league == "BRAZIL SERIE A"):
        return ("Brazil1")
    elif (league == "Brazil2"):
        return ("BRAZIL SERIE B")
    elif (league == "BRAZIL SERIE B"):
        return ("Brazil2")
    elif (league == "Sweden2"):
        return ("SWEDEN SUPERETTAN")
    elif (league == "SWEDEN SUPERETTAN"):
        return ("Sweden2")
