import json
from binance.client import Client
import logging
from Logger import getLogger

with open('config-binance.json') as json_data:
  api_config = json.load(json_data)
  json_data.close()



class BinanceRestAPI:


  def __init__(self):
    self.data = []
    self.client = Client(api_config['api_key'], api_config['api_secret'])
    self.logger = getLogger("BinanceRestApi")

  """
  Get balance of a crypto
  """
  def getBalance(self, symbolCrypto):
    balance = self.client.get_asset_balance(asset=symbolCrypto)
    self.logger.info("GET / balance: %s",balance)
    return balance
  """
  Get balance of all crypto in account
  """
  def getAccount(self):
    return self.client.get_account()

