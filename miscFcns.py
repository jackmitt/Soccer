import numpy as np

def oddsToDecimal(a):
    if (a[0] == "+"):
        b = int(a.split("+")[1])
    else:
        b = int(a)
    if (b < 0):
        return (np.round(((100/abs(b)) + 1), 2))
    else:
        return (np.round(((b/100) + 1), 2))

def standardizeTeamName(teamName, leagueName):
    b = teamName.lower()
    if (leagueName == "EPL"):
        if ("arsenal" in b):
            return ("Arsenal")
        elif ("leicester" in b):
            return ("Leicester")
        elif ("qpr" in b or "queens park" in b):
            return ("QPR")
        elif ("stoke" in b):
            return ("Stoke")
        elif ("west brom" in b):
            return ("West Brom")
        elif ("west ham" in b):
            return ("West Ham")
        elif ("manchester utd" in b or "manchester united" in b or "man utd" in b):
            return ("Man Utd")
        elif ("newcastle" in b):
            return ("Newcastle")
        elif ("liverpool" in b):
            return ("Liverpool")
        elif ("burnley" in b):
            return ("Burnley")
        elif ("everton" in b):
            return ("Everton")
        elif ("chelsea" in b):
            return ("Chelsea")
        elif ("crystal palace" in b):
            return ("Crystal Palace")
        elif ("southampton" in b):
            return ("Southampton")
        elif ("swansea" in b):
            return ("Swansea")
        elif ("aston" in b):
            return ("Aston Villa")
        elif ("sunderland" in b):
            return ("Sunderland")
        elif ("hull" in b):
            return ("Hull")
        elif ("tottenham" in b):
            return ("Tottenham")
        elif ("manchester city" in b or "man city" in b):
            return ("Man City")
        elif ("bournemouth" in b):
            return ("Bournemouth")
        elif ("norwich" in b):
            return ("Norwich")
        elif ("watford" in b):
            return ("Watford")
        elif ("middlesbrough" in b):
            return ("Middlesbrough")
        elif ("brighton" in b):
            return ("Brighton")
        elif ("huddersfield" in b):
            return ("Huddersfield")
        elif ("wolve" in b):
            return ("Wolverhampton")
        elif ("fulham" in b):
            return ("Fulham")
        elif ("cardiff" in b):
            return ("Cardiff")
        else:
            return (b)
    elif (leagueName == "Serie A"):
        if ("sampdoria" in b):
            return ("Sampdoria")
        elif ("udinese" in b):
            return ("Udinese")
        elif ("fiorentina" in b):
            return ("Fiorentina")
        elif ("ac milan" in b):
            return ("AC Milan")
        elif ("roma" in b):
            return ("AS Roma")
        elif ("atalanta" in b):
            return ("Atalanta")
        elif ("cagliari" in b):
            return ("Cagliari")
        elif ("catania" in b):
            return ("Catania")
        elif ("chievo" in b):
            return ("Chievo")
        elif ("torino" in b):
            return ("Torino")
        elif ("inter" in b):
            return ("Inter")
        elif ("palermo" in b):
            return ("Palermo")
        elif ("juventus" in b):
            return ("Juventus")
        elif ("bologna" in b):
            return ("Bologna")
        elif ("genoa" in b):
            return ("Genoa")
        elif ("lazio" in b):
            return ("Lazio")
        elif ("lecce" in b):
            return ("Lecce")
        elif ("napoli" in b):
            return ("Napoli")
        elif ("reggina" in b):
            return ("Reggina")
        elif ("siena" in b):
            return ("Siena")
        elif ("bari" in b):
            return ("Bari")
        elif ("livorno" in b):
            return ("Livorno")
        elif ("parma" in b):
            return ("Parma")
        elif ("spal" in b):
            return ("Spal")
        elif ("frosinone" in b):
            return ("Frosinone")
        elif ("empoli" in b):
            return ("Empoli")
        elif ("sassuolo" in b):
            return ("Sassuolo")
        elif ("verona" in b):
            return ("Verona")
        elif ("crotone" in b):
            return ("Crotone")
        elif ("benevento" in b):
            return ("Benevento")
        elif ("pescara" in b):
            return ("Pescara")
        elif ("carpi" in b):
            return ("Carpi")
        elif ("cesena" in b):
            return ("Cesena")
        elif ("brescia" in b):
            return ("Brescia")
        elif ("novara" in b):
            return ("Novara")
        return (b)
    else:
        print ("WRONG LEAGUE NAME")
        return ("error")

def monthToInt(a):
    if (a == "Jan"):
        return 1
    elif (a == "Feb"):
        return 2
    elif (a == "Mar"):
        return 3
    elif (a == "Apr"):
        return 4
    elif (a == "May"):
        return 5
    elif (a == "Aug"):
        return 8
    elif (a == "Sep"):
        return 9
    elif (a == "Oct"):
        return 10
    elif (a == "Nov"):
        return 11
    elif (a == "Dec"):
        return 12
    else:
        return -1
