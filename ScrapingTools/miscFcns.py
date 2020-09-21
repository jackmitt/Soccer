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
        elif ("sheff" in b):
            return ("Sheffield")
        elif ("leeds" in b):
            return ("Leeds")
        elif ("west" in b and "ham" in b):
            return ("West Ham")
        elif ("west" in b and "brom" in b):
            return ("West Brom")
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
    elif (leagueName == "La Liga"):
        if ("malaga" in b):
            return ("Malaga")
        elif ("sevilla" in b):
            return ("Sevilla")
        elif ("granada" in b):
            return ("Granada")
        elif ("almeria" in b):
            return ("Almeria")
        elif ("eibar" in b):
            return ("Eibar")
        elif ("barcelona" in b):
            return ("Barcelona")
        elif ("celta vigo" in b):
            return ("Celta Vigo")
        elif ("levante" in b):
            return ("Levante")
        elif ("real madrid" in b):
            return ("Real Madrid")
        elif ("rayo vallecano" in b):
            return ("Rayo Vallecano")
        elif ("getafe" in b):
            return ("Getafe")
        elif ("valencia" in b):
            return ("Valencia")
        elif ("cordoba" in b):
            return ("Cordoba")
        elif ("athletic club" in b or "athletic bilbao" in b or "ath bilbao" == b):
            return ("Athletic Club")
        elif ("atletico madrid" in b or "atletico" == b or "atl. madrid" == b):
            return ("Atletico Madrid")
        elif ("espanyol" in b):
            return ("Espanyol")
        elif ("villarreal" in b):
            return ("Villarreal")
        elif ("deportivo la coruna" in b or "deportivo" == b or "dep. la coruna" == b):
            return ("Deportivo La Coruna")
        elif ("real sociedad" in b):
            return ("Real Sociedad")
        elif ("elche" in b):
            return ("Elche")
        elif ("real betis" in b or "betis" == b):
            return ("Real Betis")
        elif ("valladolid" in b):
            return ("Real Valladolid")
        elif ("osasuna" in b):
            return ("Osasuna")
        elif ("alaves" in b):
            return ("Alaves")
        elif ("mallorca" in b):
            return ("Mallorca")
        elif ("leganes" in b):
            return ("Leganes")
        elif ("sd huesca" in b or "huesca" == b):
            return ("SD Huesca")
        elif ("girona" in b):
            return ("Girona")
        elif ("las palmas" in b):
            return ("Las Palmas")
        elif ("sporting gijon" in b or "gijon" == b):
            return ("Sporting Gijon")
        return (b)
    else:
        print ("WRONG LEAGUE NAME")
        return ("error")

def monthToInt(a):
    if ("Jan" in a):
        return 1
    elif ("Feb" in a):
        return 2
    elif ("Mar" in a):
        return 3
    elif ("Apr" in a):
        return 4
    elif ("May" in a):
        return 5
    elif ("Aug" in a):
        return 8
    elif ("Sep" in a):
        return 9
    elif ("Oct" in a):
        return 10
    elif ("Nov" in a):
        return 11
    elif ("Dec" in a):
        return 12
    else:
        return -1
