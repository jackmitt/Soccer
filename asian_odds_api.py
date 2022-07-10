import requests
import hashlib
import pandas
import numpy
import time
from helpers import standardizeTeamName
from helpers import convert_league

def register(url_base, key, token):
    print ("beginning to register...")
    response = requests.get(url_base + "/Register?username=jackmittapi",headers={"AOKey":key,"AOToken":token,"accept":"application/json"}).json()
    if (response["Code"] != 0):
        print ("registration failed...")
        print ("reason:", response["Result"]["TextMessage"])
        print ("exiting...")
        return (-1)
    print ("registration successful!")
    return (0)


def login():
    print ("logging into asian odds api service...")
    md5 = hashlib.md5("vnCujKMD42Pd".encode()).hexdigest()
    url = "https://webapi.asianodds88.com/AsianOddsService/Login?username=jackmittapi&password=" + md5
    response = requests.get(url,headers={"accept":"application/json"}).json()
    if (response["Code"] != 0):
        print ("login failed...")
        print ("reason:", response["Result"]["TextMessage"])
        print ("exiting...")
        return (np.nan, np.nan)
    if (register(response["Result"]["Url"],response["Result"]["Key"],response["Result"]["Token"]) != 0):
        return (np.nan, np.nan)
    print ("login successful!")
    return (response["Result"]["Url"], response["Result"]["Token"])


def logout(url_base, token):
    print ("logging out...")
    response = requests.get(url_base + "/Logout",headers={"AOToken":token,"accept":"application/json"}).json()
    if (response["Code"] != 0):
        print ("logout failed.")
        return (-1)
    print ("logout successful!")


def get_account_balance(url_base, token):
    response = requests.get(url_base + "/GetAccountSummary",headers={"AOToken":token,"accept":"application/json"}).json()
    return (response["Result"]["Credit"] + response["Result"]["Outstanding"])


def get_league_ids(url_base, token):
    league_id_map = {}

    #1 is today market, 2 is early market
    for i in ["1","2"]:
        response = requests.get(url_base + "/GetLeagues?sportsType=1&marketTypeId=" + i + "&since=1000000000000",headers={"AOToken":token,"accept":"application/json"}).json()
        for league in response["Result"]["Sports"][0]["League"]:
            league_id_map[league["LeagueName"]] = league["LeagueId"]

    return (league_id_map)


def get_best_pinnacle_lines(url_base, token, leagues):
    league_id_map = get_league_ids(url_base, token)

    league_id_string = ""
    for league in leagues:
        if (league_id_string != ""):
            league_id_string = league_id_string + ","
        league_id_string = league_id_string + str(league_id_map[league])

    matches = {}

    #1 is today market, 2 is early market
    for i in ["1","2"]:
        response = requests.get(url_base + "/GetFeeds?sportsType=1&marketTypeId=" + i + "&leagues=" + league_id_string + "&since=1000000000000&bookies=PIN",headers={"AOToken":token,"accept":"application/json"}).json()
        for x in response["Result"]["Sports"][0]["MatchGames"]:
            sum_odds = abs(2 - float(x["FullTimeHdp"]["BookieOdds"].split(";")[0].split("=")[1].split(",")[0])) + abs(2 - float(x["FullTimeHdp"]["BookieOdds"].split(";")[0].split("=")[1].split(",")[1]))
            if (x["MatchId"] not in matches):
                matches[x["MatchId"]] = {"GameId":x["GameId"],"sum_odds":sum_odds,"Home":x["HomeTeam"]["Name"],"Away":x["AwayTeam"]["Name"],"MarketTypeId":int(i),"home_odds":float(x["FullTimeHdp"]["BookieOdds"].split(";")[0].split("=")[1].split(",")[0]),"away_odds":float(x["FullTimeHdp"]["BookieOdds"].split(";")[0].split("=")[1].split(",")[1])}
                if (x["FullTimeFavoured"] == 2):
                    if ("-" in x["FullTimeHdp"]["Handicap"]):
                        matches[x["MatchId"]]["AH"] = 0 - (float(x["FullTimeHdp"]["Handicap"].split("-")[0]) + float(x["FullTimeHdp"]["Handicap"].split("-")[1])) / 2
                    else:
                        matches[x["MatchId"]]["AH"] = 0 - float(x["FullTimeHdp"]["Handicap"])
                else:
                    if ("-" in x["FullTimeHdp"]["Handicap"]):
                        matches[x["MatchId"]]["AH"] = (float(x["FullTimeHdp"]["Handicap"].split("-")[0]) + float(x["FullTimeHdp"]["Handicap"].split("-")[1])) / 2
                    else:
                        matches[x["MatchId"]]["AH"] = float(x["FullTimeHdp"]["Handicap"])
            #The lowest sum_odds is what the main line is for the match
            if (sum_odds < matches[x["MatchId"]]["sum_odds"]):
                matches[x["MatchId"]] = {"GameId":x["GameId"],"sum_odds":sum_odds,"Home":x["HomeTeam"]["Name"],"Away":x["AwayTeam"]["Name"],"MarketTypeId":int(i),"home_odds":float(x["FullTimeHdp"]["BookieOdds"].split(";")[0].split("=")[1].split(",")[0]),"away_odds":float(x["FullTimeHdp"]["BookieOdds"].split(";")[0].split("=")[1].split(",")[1])}
                if (x["FullTimeFavoured"] == 2):
                    if ("-" in x["FullTimeHdp"]["Handicap"]):
                        matches[x["MatchId"]]["AH"] = 0 - (float(x["FullTimeHdp"]["Handicap"].split("-")[0]) + float(x["FullTimeHdp"]["Handicap"].split("-")[1])) / 2
                    else:
                        matches[x["MatchId"]]["AH"] = 0 - float(x["FullTimeHdp"]["Handicap"])
                else:
                    if ("-" in x["FullTimeHdp"]["Handicap"]):
                        matches[x["MatchId"]]["AH"] = (float(x["FullTimeHdp"]["Handicap"].split("-")[0]) + float(x["FullTimeHdp"]["Handicap"].split("-")[1])) / 2
                    else:
                        matches[x["MatchId"]]["AH"] = float(x["FullTimeHdp"]["Handicap"])


    return (matches)


def get_placement_info(url_base, token, GameId, OddsName, MarketTypeId):
    request_body = {"GameId":GameId,"GameType":"H","IsFullTime":1,"MarketTypeId":MarketTypeId,"OddsName":OddsName,"SportsType":1,"Bookies":"PIN,P88,3ET,ISN","Timeout":10}
    response = requests.post(url_base + "/GetPlacementInfo", headers={"AOToken":token,"accept":"application/json"}, json=request_body).json()
    if (response["Code"] != 0):
        return ({})
    dict = {}
    for book in response["Result"]["OddsPlacementData"]:
        dict[book["Bookie"]] = {"max":book["MaximumAmount"],"min":book["MinimumAmount"],"odds":book["Odds"]}
    return (dict)


def get_current_bets(url_base, token):
    response = requests.get(url_base + "/GetBets",headers={"AOToken":token,"accept":"application/json"}).json()
    dict = {}
    for bet in response["Data"]:
        league = convert_league(bet["LeagueName"])
        dict[(standardizeTeamName(bet["HomeName"], league), standardizeTeamName(bet["AwayName"], league))] = []
        if (bet["BetType"] == "HDP Away" or float(bet["HdpOrGoal"]) == 0):
            ah = float(bet["HdpOrGoal"])
        elif (bet["BetType"] == "HDP Home"):
            ah = -float(bet["HdpOrGoal"])
        dict[(standardizeTeamName(bet["HomeName"], league), standardizeTeamName(bet["AwayName"], league))].append({"Ref":bet["BetPlacementReference"],"Bookie":bet["Bookie"],"AH":ah,"Odds":bet["Odds"],"Stake":bet["Stake"]})
    return (dict)


def place_bet(url_base, token, GameId, MarketTypeId, OddsName, Amount, BookieOdds):
    request_body = {"GameId":GameId,"GameType":"H","IsFullTime":1,"MarketTypeId":MarketTypeId,"SportsType":1,"OddsName":OddsName,"OddsFormat":"00","AcceptChangedOdds":0,"Amount":Amount,"BookieOdds":BookieOdds}
    response = requests.post(url_base + "/PlaceBet", headers={"AOToken":token,"accept":"application/json"}, json=request_body).json()
    if (response["Code"] != 0):
        return (-1)
    else:
        return (response["Result"]["BetPlacementReference"])
