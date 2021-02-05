from binance.client import Client
import json 
import decimal
import sys
import time

api_key = "Ry1X83a4W9O8CIm530Q6lczbWyD60gj3Z7DpZ28otT5y0MiUf0sPs8HeR5l0KqjD"
api_secret = "NKq26OygNtK7phccacp9SxZWSGTtD5XkJsgJnafTLLr0nls6ZW9Bu9fW6RxO8R3o"
client = Client(api_key, api_secret)
print("Client is loaded")

def getListOfCoin():

    exchangeInfo = client.get_exchange_info() 

    targetCoinInfo = None
    #targetCoinInfo = next((x for x in exchangeInfo if x['symbols'] == symbolCrypto), None)
    #print(exchangeInfo)
    listOfCoin = set()
    for x in exchangeInfo['symbols']:
        #print(x['baseAsset'])
        listOfCoin.add(x['baseAsset'])

    print(listOfCoin)
    return listOfCoin