import requests
import hashlib
import pandas
import numpy

def register(url_base, key, token):
    print ("beginning to register...")
    response = requests.get(url_base + "/Register?username=jackmittapi",headers={"AOKey":key,"AOToken":token",accept":"application/json"}).json()
    if (response.Code != 0):
        print ("registration failed...")
        print ("reason:", response.Result["TextMessage"])
        print ("exiting...")
        return (-1)
    print ("registration successful!")
    return (0)


def login():
    print ("logging into asian odds api service...")
    md5 = hashlib.md5("xxx".encode()).hexdigest()
    url = "https://webapi.asianodds88.com/AsianOddsService/Login?username=jackmittapi&password=" + md5
    response = requests.get(url,headers={"accept":"application/json"}).json()
    if (response.Code != 0):
        print ("login failed...")
        print ("reason:", response.Result["TextMessage"])
        print ("exiting...")
        return (np.nan, np.nan)
    if (register(response.Result["Url"],response.Result["Key"],response.Result["Token"]) != 0):
        return (np.nan, np.nan)
    print ("login successful!")
    return (response.Result["Url"], response.Result["Token"])


def logout(url_base, token):
    print ("logging out...")
    response = requests.get(url_base + "/Logout",headers={"AOToken":token",accept":"application/json"}).json()
    if (response.Code != 0):
        print ("logout failed.")
        return (-1)
    print ("logout successful!")


def get_account_balance(url_base, token):
    response = requests.get(url_base + "/GetAccountSummary",headers={"AOToken":token",accept":"application/json"}).json()
    return (response.Result["Credit"] + response.Result["Outstanding"])
