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

def standardizeTeamName(a):
    b = a.lower()
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
