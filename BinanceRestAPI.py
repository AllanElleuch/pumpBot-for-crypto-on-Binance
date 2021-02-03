import json
from binance.client import Client

with open('config-binance.json') as json_data:
  api_config = json.load(json_data)
  json_data.close()


class BinanceRestAPI:


  def __init__(self):
    self.data = []
    self.client = Client(api_config['api_key'], api_config['api_secret'])

  """
  Get balance of a crypto
  """
  def getBalance(self, symbolCrypto):
    return self.client.get_asset_balance(asset=symbolCrypto)
  """
  Get balance of all crypto in account
  """
  def getAccount(self):
    return self.client.get_account()

