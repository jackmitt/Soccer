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
    elif (league == "Austria1"):
        if ("austria vienna" in lname):
            return ("Austria Wien")
        elif ("rapid vienna" in lname):
            return ("Rapid Wien")
        elif ("sturm" in lname and "graz" in lname):
            return ("Sturm graz")
        elif ("kapfenberg" in lname):
            return ("Kapfenberg")
        elif ("admira wacker" in lname):
            return ("Trenkwalder Admira Wacker")
        elif ("mattersburg" in lname):
            return ("Mattersburg")
        elif ("wiener neustadt" in lname):
            return ("FC Magna Wiener Neustadt")
        elif ("sv gr" in lname and "dig" in lname):
            return ("SV Grodig")
        elif (" altach" in lname):
            return ("Rheindorf Altach")
        elif ("st. " in lname and "lten" in lname):
            return ("St.Polten")
        elif ("lask" == lname):
            return ("LASK Linz")
        elif ("wsg tirol" in lname):
            return ("WSG Wattens")
        elif ("austria klagenfurt" in lname):
            return ("SG Austria Klagenfurt")
        return (name)
    elif (league == "Austria2"):
        if ("lask" == lname):
            return ("LASK Linz")
        elif (" altach" in lname):
            return ("Rheindorf Altach")
        elif ("st. " in lname and "lten" in lname):
            return ("St.Polten")
        elif ("sv gr" in lname and "dig" in lname):
            return ("SV Grodig")
        elif ("mattersburg" in lname):
            return ("Mattersburg")
        elif ("wiener neustadt" in lname):
            return ("FC Magna Wiener Neustadt")
        elif ("first vienna" in lname):
            return ("First Wien 1894")
        elif ("austria lustenau" in lname):
            return ("Austria Lustenau")
        elif ("wac - st. and" in lname):
            return ("Wolfsberger AC")
        elif ("fc lustenau" == lname):
            return ("Lustenau")
        elif ("blau-weiss" in lname):
            return ("FC Blau Weiss Linz")
        elif ("kapfenberg" in lname):
            return ("Kapfenberg")
        elif ("parndorf" in lname):
            return ("Parndorf")
        elif ("austria klagenfurt" in lname):
            return ("SG Austria Klagenfurt")
        elif ("young" in lname and "austria wien" in lname):
            return ("Austria Wien (Youth)")
        elif ("wacker innsbruck ii" in lname):
            return ("FC Wacker Innsbruck Amateure")
        elif ("rapid wien ii" in lname):
            return ("Rapid Vienna (Youth)")
        elif ("lafnitz" in lname):
            return ("Lafnitz")
        elif ("grazer " in lname):
            return ("Grazer AK")
        elif (" steyr" in lname):
            return ("SK Vorwarts Steyr")
        elif ("dornbirn" in lname):
            return ("FC Dornbirn 1913")
        elif ("fc juniors o" in lname):
            return ("FC Superfund Pasching")
        return (name)
    elif (league == "Belgium2"):
        if ("lommel united" == lname):
            return ("KVSK Lommel")
        elif ("white star woluwe" in lname):
            return ("White Star Bruxelles")
        elif ("club nxt" in lname):
            return ("Club Brugge(U23)")
        elif ("royal excel mouscron" in lname):
            return ("Excelsior Mouscron")
        elif ("lierse " in lname):
            return ("Lierse")
    elif (league == "Bosnia1"):
        if ("nk jajce" in lname):
            return ("NK Metalleghe-BSI")
        elif ("sloboda tuzla" in lname):
            return ("Sloboda")
    elif (league == "Bulgaria1"):
        if ("neftochimik" in lname):
            return ("Neff supporting Simic")
        elif ("etar veliko" in lname):
            return ("Etar")
    elif (league == "Italy1"):
        if ("spal" == lname or "spal 2013" == lname):
            return ("Spal")
        elif ("ac siena" in lname):
            return ("Robur Siena S.S.D.")
    elif (league == "Italy2"):
        if ("spal" == lname or "spal 2013" == lname):
            return ("Spal")
        elif ("ac siena" in lname):
            return ("Robur Siena S.S.D.")
        elif ("ascoli " in lname):
            return ("Ascoli")
        elif ("novara " in lname):
            return ("Novara")
        elif ("ac pisa " in lname or "pisa sporting" in lname):
            return ("Pisa")
        elif ("parma calcio" in lname):
            return ("Parma")
        elif ("chievo verona" in lname):
            return ("Chievo")
        elif ("ternana " in lname):
            return ("Ternana")
        elif ("alessandria " in lname):
            return ("Alessandria")
    elif (league == "Netherlands1"):
        if ("ajax " in lname or "ajax" == lname):
            return ("AFC Ajax")
        elif ("excelsior rotterdam" in lname or "excelsior" == lname):
            return ("Excelsior SBV")
        elif ("heerenveen" == lname):
            return ("SC Heerenveen")
        elif ("cambuur" in lname):
            return ("SC Cambuur")
    elif (league == "Netherlands2"):
        if ("excelsior rotterdam" in lname):
            return ("Excelsior SBV")
        elif ("ajax amsterdam" in lname):
            return ("Jong Ajax (Youth)")
        elif ("fc twente enschede u21" in lname):
            return ("FC Twente Enschede Reserve")
        elif ("psv eindhoven u21" in lname):
            return ("Jong PSV Eindhoven (Youth)")
    elif (league == "Czech1"):
        if ("zbrojovka brno" in lname):
            return ("Brno")
        elif ("fastav zlin" in lname):
            return ("Tescoma Zlin")
    elif (league == "Czech2"):
        if ("zbrojovka brno" in lname):
            return ("Brno")
        elif ("fastav zlin" in lname):
            return ("Tescoma Zlin")
        elif ("banik most" in lname):
            return ("Most Mus")
        elif (" trinec" in lname):
            return ("Trinec")
        elif ("sellier &" in lname):
            return ("FK Graffin Vlasim")
        elif ("olympia radotin" in lname):
            return ("Olymp.Hradec Kralove")
    elif (league == "Denmark1"):
        if ("vejle boldklub" in lname):
            return ("Vejle")
        elif ("agf aarhus" in lname):
            return ("Aarhus AGF")
        elif ("aab" == lname):
            return ("Aalborg")
        elif ("viborg" in lname):
            return ("Viborg")
        elif ("silkeborg" in lname):
            return ("Silkeborg")
        elif ("randers" == lname):
            return ("Randers FC")
        elif ("copenhagen" == lname):
            return ("FC Copenhagen")
        elif (" odense" in lname):
            return ("Odense BK")
    elif (league == "Denmark2"):
        #cant find FC Hjörring equivalent
        if ("vejle boldklub" in lname):
            return ("Vejle")
        elif ("brönshöj" in lname):
            return ("Bronshoj")
        elif ("hb köge" in lname or "hb koge" == lname):
            return ("Herfolge Boldklub Koge")
        elif ("akademisk" in lname):
            return ("AB Copenhagen")
        elif ("blokhus " in lname):
            return ("Jammerbugt")
        elif ("vendsyssel" in lname):
            return ("Vendsyssel")
    elif (league == "England1"):
        if ("wolverhampton" in lname):
            return ("Wolves")
        elif ("bournemouth" in lname):
            return ("Bournemouth AFC")
        elif ("brighton" in lname and "hove albion" in lname):
            return ("Brighton Hove Albion")
    elif (league == "England2"):
        if ("wolverhampton" in lname):
            return ("Wolves")
        elif ("sunderland" in lname):
            return ("Sunderland A.F.C")
    elif (league == "England3"):
        if ("wolverhampton" in lname):
            return ("Wolves")
    elif (league == "England4"):
        if ("dagenham redbridge" in lname):
            return ("Dagenham   Redbridge")
    elif (league == "France1"):
        if ("stade rennais" in lname):
            return ("Rennes")
        elif ("stade reims" in lname):
            return ("Reims")
    elif (league == "France2"):
        if ("stade reims" in lname):
            return ("Reims")
        elif ("us orléans" in lname):
            return ("Orleans US 45")
        elif ("cs sedan" in lname):
            return ("Sedan")
    elif (league == "France3"):
        if ("us orléans" in lname):
            return ("Orleans US 45")
        elif ("cs sedan" in lname):
            return ("Sedan")
        elif ("olympique ajaccio" in lname):
            return ("Ajaccio Gfco")
        elif ("unis colmar" in lname):
            return ("Colmar")
        elif ("sporting club de lyon" == lname):
            return ("Lyon Duchere")
    elif (league == "Germany1"):
        if ("bayern munich" in lname):
            return ("Bayern Munchen")
        elif ("koln" == lname):
            return ("FC Koln")
        elif ("freiburg" in lname):
            return ("SC Freiburg")
        elif ("wolfsburg" == lname):
            return ("VfL Wolfsburg")
    elif (league == "Germany2"):
        if ("greuther furth" in lname):
            return ("Greuther Furth")
        elif ("heidenheim" == lname):
            return ("Heidenheimer")
        elif ("jahn regensburg" in lname):
            return ("Jahn Regensburg")
        elif ("darmstadt" in lname):
            return ("Darmstadt")
        elif ("st pauli" == lname):
            return ("St. Pauli")
    elif (league == "Germany3"):
        if ("ürkgücü" in lname):
            return ("Te Cu Kukuh Atta Seip")
    elif (league == "Greece1"):
        if (" veria" in lname):
            return ("Veria FC")
    elif (league == "Hungary1"):
        if ("eto fc gy" in lname):
            return ("Gyori ETO")
        elif ("paksi " in lname):
            return ("Paksi SE Honlapja")
        elif ("mtk budapest" in lname):
            return ("MTK Hungaria")
        elif ("mol vidi " in lname or "mol feh" in lname):
            return ("Fehervar Videoton")
        elif ("budafoki " in lname):
            return ("Dafuji cloth MTE")
        elif ("kisvárda" in lname):
            return ("Varda SE")
    elif (league == "Portugal1"):
        if ("desportivo aves" in lname):
            return ("Aves")
        elif ("cd nacional" in lname):
            return ("Nacional da Madeira")
        elif ("arouca" == lname):
            return ("FC Arouca")
        elif ("estoril " in lname):
            return ("Estoril")
        elif ("famalicao" in lname):
            return ("FC Famalicao")
        elif ("porto" == lname):
            return ("FC Porto")
        elif (" maritimo" in lname):
            return ("Maritimo")
        elif ("santa clara" in lname):
            return ("Santa Clara")
        elif ("braga" in lname):
            return ("Sporting Braga")
        elif ("portimonense" in lname):
            return ("Portimonense")
    elif (league == "Portugal2"):
        if ("desportivo aves" in lname):
            return ("Aves")
        elif ("cd nacional" in lname):
            return ("Nacional da Madeira")
        elif ("cadémico viseu" in lname):
            return ("Viseu")
        elif ("cd trofense" in lname):
            return ("Clube Desportivo Trofense")
        elif ("naval" in lname and "de maio" in lname):
            return ("Associacao Naval")
    elif (league == "Romania1"):
        if ("fcsb" == lname):
            return ("FC Steaua Bucuresti")
    elif (league == "Serbia1"):
        if ("red star belgrade" in lname):
            return ("Crvena Zvezda")
        elif ("javor-matis" in lname):
            return ("Habitpharm Javor")
        elif ("ofk backa" in lname):
            return ("FK Backa Backa Palanka")
    elif (league == "Slovakia1"):
        if ("pohronie" in lname):
            return ("Sokol Dolna Zdana")
    elif (league == "Slovenia1"):
        if ("nk krsko" in lname):
            return ("Krsko Posavlje")
        elif ("nk bravo" in lname):
            return ("ASK Bravo Publikum")
        elif ("tabor sezana" in lname):
            return ("Tabor Sezana")
        elif (" celje" in lname):
            return ("NK Publikum Celje")
        elif ("domzale" in lname):
            return ("Domzale")
        elif ("radomlje" in lname):
            return ("Radomlje")
        elif ("ns mura" == lname):
            return ("NK Mura 05")
        elif ("maribor" in lname):
            return ("Maribor")
    elif (league == "Spain1"):
        if ("alavés" in lname):
            return ("Alaves")
        elif ("vallodolid" in lname):
            return ("Real Valladolid")
        elif ("villarreal" == lname):
            return ("Villarreal")
        elif ("barcelona" == lname):
            return ("FC Barcelona")
        elif ("athletic club bilbao" in lname):
            return ("Athletic Bilbao")
        elif ("elche " in lname):
            return ("Elche")
    elif (league == "Spain2"):
        if ("villarreal cf" in lname):
            return ("Villarreal")
        elif ("alavés" in lname):
            return ("Alaves")
        elif ("bilbao athletic" in lname):
            return ("Athletic Bilbao B")
    elif (league == "Turkey1"):
        if ("akhisar belediyespor" in lname or "akhisarspor" == lname):
            return ("Akhisar Bld.Geng")
        elif ("osmanlispor" in lname):
            return ("Ankaraspor FK")
        elif ("erzurumspor" in lname):
            return ("Erzurum BB")
        elif ("gaziantep fk" in lname):
            return ("Gazisehir Gaziantep")
    elif (league == "Turkey2"):
        if ("akhisar belediyespor" in lname or "akhisarspor" == lname):
            return ("Akhisar Bld.Geng")
        elif ("osmanlispor" in lname):
            return ("Ankaraspor FK")
        elif ("erzurumspor" in lname):
            return ("Erzurum BB")
        elif ("gaziantep " in lname):
            return ("Gazisehir Gaziantep")
        elif ("tavsanli" in lname):
            return ("Tavsanli Belediye T.L")
        elif ("güngören" in lname):
            return ("Gungoren")
        elif ("sanliurfaspor" in lname):
            return ("S.Urfaspor")
    elif (league == "Croatia1"):
        if ("nk osijek" in lname):
            return ("ZNK Osijek")
        elif ("slaven belupo" in lname or "nk slaven" == lname):
            return ("Slaven Koprivnica")
        elif ("hnk rijeka" in lname):
            return ("Rijeka")
        elif ("istra 1961" in lname):
            return ("Istra 1961 Pula")
    elif (league == "Scotland1"):
        if (" mirren" in lname):
            return ("Saint Mirren")
        elif (" johnstone" in lname):
            return ("Saint Johnstone")
        elif ("celtic" == lname):
            return ("Celtic FC")
        elif (" midlothian" in lname):
            return ("Heart of Midlothian")
    elif (league == "Switzerland1"):
        if ("grasshopper" in lname):
            return ("Grasshopper")
        elif ("st gallen" in lname):
            return ("St. Gallen")
        elif ("zurich" == lname):
            return ("FC Zurich")
        elif ("sion" == lname):
            return ("FC Sion")
        elif ("young boys" in lname):
            return ("Young Boys")

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
    elif (league == "CROATIA FIRST FOOTBALL LEAGUE"):
        return ("Croatia1")
    elif (league == "Croatia1"):
        return ("CROATIA FIRST FOOTBALL LEAGUE")
    elif (league == "DENMARK SUPER LEAGUE"):
        return ("Denmark1")
    elif (league == "Denmark1"):
        return ("DENMARK SUPER LEAGUE")
    elif (league == "DENMARK DIVISION 1"):
        return ("Denmark2")
    elif (league == "Denmark2"):
        return ("DENMARK DIVISION 1")
    elif (league == "*ENGLISH PREMIER LEAGUE"):
        return ("England1")
    elif (league == "England1"):
        return ("*ENGLISH PREMIER LEAGUE")
    elif (league == "ENGLISH CHAMPIONSHIP"):
        return ("England2")
    elif (league == "England2"):
        return ("ENGLISH CHAMPIONSHIP")
    elif (league == "*GERMANY BUNDESLIGA"):
        return ("Germany1")
    elif (league == "Germany1"):
        return ("*GERMANY BUNDESLIGA")
    elif (league == "GERMANY BUNDESLIGA 2"):
        return ("Germany2")
    elif (league == "Germany2"):
        return ("GERMANY BUNDESLIGA 2")
    elif (league == "HOLLAND EREDIVISIE"):
        return ("Netherlands1")
    elif (league == "Netherlands1"):
        return ("HOLLAND EREDIVISIE")
    elif (league == "HOLLAND EERSTE DIVISIE"):
        return ("Netherlands2")
    elif (league == "Netherlands2"):
        return ("HOLLAND EERSTE DIVISIE")
    elif (league == "POLAND EKSTRAKLASA"):
        return ("Poland1")
    elif (league == "Poland1"):
        return ("POLAND EKSTRAKLASA")
    elif (league == "PORTUGAL PRIMEIRA LIGA"):
        return ("Portugal1")
    elif (league == "Portugal1"):
        return ("PORTUGAL PRIMEIRA LIGA")
    elif (league == "PORTUGAL LIGA 2"):
        return ("Portugal2")
    elif (league == "Portugal2"):
        return ("PORTUGAL LIGA 2")
    elif (league == "ROMANIA LIGA 1"):
        return ("Romania1")
    elif (league == "Romania1"):
        return ("ROMANIA LIGA 1")
    elif (league == "SCOTLAND PREMIERSHIP"):
        return ("Scotland1")
    elif (league == "Scotland1"):
        return ("SCOTLAND PREMIERSHIP")
    elif (league == "SLOVAKIA SUPER LIGA"):
        return ("Slovakia1")
    elif (league == "Slovakia1"):
        return ("SLOVAKIA SUPER LIGA")
    elif (league == "SLOVENIA PRVA LIGA"):
        return ("Slovenia1")
    elif (league == "Slovenia1"):
        return ("SLOVENIA PRVA LIGA")
    elif (league == "*SPAIN LA LIGA"):
        return ("Spain1")
    elif (league == "Spain1"):
        return ("*SPAIN LA LIGA")
    elif (league == "SWITZERLAND SUPER LEAGUE"):
        return ("Switzerland1")
    elif (league == "Switzerland1"):
        return ("SWITZERLAND SUPER LEAGUE")
    elif (league == "TURKEY SUPER LEAGUE"):
        return ("Turkey1")
    elif (league == "Turkey1"):
        return ("TURKEY SUPER LEAGUE")
